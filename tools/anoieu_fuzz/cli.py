"""The command line of the anoieu fuzzer.

    anoieu-fuzz run [--mode proof|signature] [-n N] [--signature Cpc.eo]
    anoieu-fuzz one --seed S            # print one case, run nothing
    anoieu-fuzz replay FILE             # what each checker says about a file
    anoieu-fuzz shrink FILE             # cut a case down to what still provokes it
    anoieu-fuzz checkers                # what is configured, and what is on this machine

and, once a run has found something worth keeping:

    anoieu-fuzz promote DIR             # move a reproducer into tests/fuzz/
    anoieu-fuzz report                  # every promoted finding, as diagnostics
    anoieu-fuzz verify                  # do they still do what the record says
    anoieu-fuzz explain FUZ0002         # what a code means
    anoieu-fuzz list-codes              # the four of them

`run` exits 1 when it found something, so a nightly job is one line. `report`
exits 1 when anything is promoted, which is the same convention `anoieu check`
uses and means the same thing: there are open findings.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import os
import random
import sys
import tempfile
import threading
import time

from . import __version__
from . import report as reporting
from .checkers import Checker, Outcome, from_config, load_config
from .codes import CODES
from .gen import Case, absolutize, generate, mutate, reformat, split_commands, unwrap
from .triage import Corpus, Finding, judge, shrink
from .vocab import Vocabulary, fallback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: Where a signature is looked for when none is named: the clone `tools/deps.py`
#: keeps, so a run in a checkout of this repository needs no arguments.
SIGNATURE_GUESSES = ("deps/cvc5/proofs/eo/cpc/Cpc.eo",)


def _find_signature(given: str) -> str:
    if given:
        return os.path.abspath(given)
    env = os.environ.get("CPC") or os.environ.get("ELENCHOS_SIGNATURE")
    if env:
        return os.path.abspath(env)
    for guess in SIGNATURE_GUESSES:
        path = os.path.join(ROOT, guess)
        if os.path.isfile(path):
            return path
    return ""


def _seed_files(dirs: list[str]) -> list[str]:
    out = []
    for d in dirs or []:
        if os.path.isfile(d):
            out.append(d)
            continue
        for base, _, names in os.walk(d):
            for name in sorted(names):
                if name.endswith((".eo", ".cpc", ".smt2", ".eos", ".proof")):
                    out.append(os.path.join(base, name))
    return out


class Session:
    """One configuration of the fuzzer: what to write, and who to ask."""

    def __init__(self, args) -> None:
        cfg = load_config(args.config)
        self.signature = _find_signature(args.signature or cfg.get("signature", ""))
        self.checkers: list[Checker] = from_config(cfg, args.checker)
        self.mode = args.mode
        self.timeout = args.timeout
        self.wild = args.wild
        self.depth = args.depth
        self.metamorphic = getattr(args, "metamorphic", False)
        self.reference = getattr(args, "reference", "") or cfg.get("reference", "")
        self.learn_cap = 0 if getattr(args, "no_learn", False) else getattr(args, "learn_cap", 400)
        self.note = ""

        self.extend = getattr(args, "extend", False) and bool(self.signature)
        self.voc: Vocabulary = fallback()
        if self.signature and (self.mode == "proof" or self.extend):
            from .vocab import load as load_vocab  # noqa: PLC0415

            self.voc, self.note = load_vocab(self.signature)
        elif self.mode == "proof":
            self.note = "no signature given: cases carry their own declarations"
        if self.mode == "signature":
            self.note += ("; cases extend it" if self.extend
                          else "cases stand alone on a builtin prelude")

        self.seeds: list[Case] = []      # as they stand, for the first pass
        self.mutable: list[Case] = []     # unwrapped, for the mutator to damage
        self.learned: list[Case] = []     # cases that reached somewhere new
        self.details: set[str] = set()
        self.pool: list[str] = []
        for path in _seed_files(getattr(args, "seed_corpus", []) or []):
            try:
                with open(path, errors="replace") as f:
                    text = f.read()
            except OSError:
                continue
            commands = absolutize(split_commands(text), os.path.dirname(os.path.abspath(path)))
            if not commands:
                continue
            suffix = ".eo" if path.endswith(".eo") else ".cpc"
            name = f"seed:{os.path.basename(path)}"
            self.seeds.append(Case(commands, self.mode, suffix, path, name))
            body = unwrap(commands)
            self.mutable.append(Case(body, self.mode, suffix, path, name))
            self.pool += body

    # -- one case, start to finish

    def make(self, seed: str, mutate_p: float, index: int = -1) -> Case:
        """The case for one index of a run.

        The seed corpus is checked *as it stands* first, one case per file,
        before anything is generated or damaged. It is the cheapest finding
        there is -- two checkers that already disagree about a file somebody
        committed -- and the first real disagreement this fuzzer reported came
        from exactly there, in a regression test of the checker it was about.
        """
        if 0 <= index < len(self.seeds):
            seed_case = self.seeds[index]
            return seed_case.replace(seed_case.commands)
        rng = random.Random("choose:" + seed)
        stock = self.mutable + self.learned
        if stock and rng.random() < mutate_p:
            return mutate(seed, rng.choice(stock), self.pool)
        voc = self.voc if (self.mode == "proof" or self.extend) else fallback()
        return generate(seed, self.mode, voc, wild=self.wild, depth=self.depth,
                        include=self.signature if self.extend else "")

    def ask(self, case: Case) -> list[Outcome]:
        """Every checker's answer to one case, plus -- under `--metamorphic` --
        each checker's answer to the same case laid out differently."""
        fd, path = tempfile.mkstemp(suffix=case.suffix, prefix="anoieu-fuzz-")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(case.text())
            out = [c.run(self.mode, path, self.signature, self.timeout) for c in self.checkers]
        finally:
            os.unlink(path)
        if not self.metamorphic:
            return out
        twin = reformat(case.seed, case)
        fd, path = tempfile.mkstemp(suffix=case.suffix, prefix="anoieu-fuzz-")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(twin.text())
            for checker in self.checkers:
                got = checker.run(self.mode, path, self.signature, self.timeout)
                out.append(
                    Outcome(
                        got.checker + " (reformatted)",
                        got.status,
                        got.coarse,
                        got.detail,
                        got.code,
                        got.seconds,
                    )
                )
        finally:
            os.unlink(path)
        return out

    def learn(self, case: Case, outcomes: list[Outcome]) -> bool:
        """Keep a case that made a checker say something it had not said before.

        The cheapest coverage signal available without instrumenting anything:
        a checker's diagnostic is a proxy for which path it took, and
        `checkers._portable` has already stripped the paths and numbers that
        vary between two visits to the same one. A case that produced a new
        message reached somewhere new, so it goes into the pool the mutator
        draws from and the run explores outward from it rather than starting
        over each time.

        It is a proxy and not a measurement. Two paths can share a message, one
        path can have several, and a checker that says little is a checker this
        learns little from. It costs a set of strings.
        """
        fresh = False
        for got in outcomes:
            detail = got.detail
            if not detail or got.status in ("correct", "quiet", "skipped"):
                continue
            if detail not in self.details:
                self.details.add(detail)
                fresh = True
        if fresh and len(self.learned) < self.learn_cap:
            self.learned.append(case.replace(unwrap(case.commands)))
        return fresh

    def probe(self, case: Case) -> Finding | None:
        return judge(case, self.ask(case), self.reference)


# -- the commands -------------------------------------------------------------


def cmd_run(args) -> int:
    session = Session(args)
    live = [c for c in session.checkers if c.modes.get(session.mode)]
    if not live:
        print(f"-- no checker is configured for mode {session.mode}", file=sys.stderr)
        return 2
    print(f"-- anoieu-fuzz {__version__}: {session.mode} cases against "
          f"{', '.join(c.name for c in live)}")
    for checker in live:
        where = checker.resolve(session.mode)
        print(f"   {checker.name:10} {where or '(not on PATH; set $' + (checker.env or 'PATH') + ')'}")
    if session.signature:
        print(f"   signature  {os.path.relpath(session.signature, ROOT)}")
    if len(live) > 1:
        here = any(c.name == session.reference for c in live)
        print(f"   reference  {session.reference or '(none)'}"
              + ("" if here else "  -- not among the checkers, so every disagreement "
                                 "is reported as the serious direction"))
    if session.note:
        print(f"   vocabulary {session.note}")
    runnable = [c for c in live if c.resolve(session.mode)]
    if session.mode == "proof" and len(runnable) < 2:
        print("   note       fewer than two checkers are on this machine, so nothing "
              "can be\n              compared: this run can only report a crash or a "
              "timeout. Set\n              $ETHOS and $LOGOS, or name your own in "
              "--config -- see docs/fuzzing.md")
    if session.seeds:
        print(f"   seeds      {len(session.seeds)} file(s), {len(session.pool)} commands"
              f"; the first {min(len(session.seeds), args.cases)} case(s) are those files "
              f"as they stand")

    corpus = Corpus(args.out)
    os.makedirs(args.out, exist_ok=True)
    lock = threading.Lock()
    tally: dict[str, dict[str, int]] = {}
    started = time.monotonic()
    stop = threading.Event()
    done = 0

    def one(i: int) -> None:
        nonlocal done
        if stop.is_set():
            return
        if args.time_limit and time.monotonic() - started > args.time_limit:
            stop.set()
            return
        seed = f"{args.seed}:{i}"
        case = session.make(seed, args.mutate, i)
        outcomes = session.ask(case)
        finding = judge(case, outcomes, session.reference)
        with lock:
            done += 1
            session.learn(case, outcomes)
            for o in outcomes:
                tally.setdefault(o.checker, {})
                tally[o.checker][o.status] = tally[o.checker].get(o.status, 0) + 1
            if finding is None:
                if args.verbose:
                    print(f"[{done:5}] ok")
                return
            if corpus.seen(finding.bucket):
                corpus.add(finding)
                if args.verbose:
                    print(f"[{done:5}] {finding.code} (bucket already known)")
                return
        was = len(finding.case.commands)
        spent = 0
        if not args.no_shrink:
            small, spent = shrink(finding.case, session.probe, finding.bucket,
                                  args.shrink_budget)
            again = session.probe(small)
            if again is not None and again.bucket == finding.bucket:
                finding = again
        with lock:
            if corpus.add(finding):
                now = len(finding.case.commands)
                print(f"[{done:5}] {finding.code} {finding.kind}: {finding.summary}")
                print(f"         {os.path.join(args.out, finding.bucket)}"
                      f"  ({now} command(s)"
                      + (f", shrunk from {was} in {spent} runs" if spent else "")
                      + f", seed {finding.case.seed})")
                if args.max_findings and len(corpus.new) >= args.max_findings:
                    stop.set()

    if args.jobs > 1:
        with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
            list(pool.map(one, range(args.cases)))
    else:
        for i in range(args.cases):
            one(i)
            if stop.is_set():
                break

    elapsed = time.monotonic() - started
    print(f"-- {done} case(s) in {elapsed:.0f}s; "
          f"{sum(corpus.counts.values())} finding(s) in {len(corpus.counts)} bucket(s)")
    if session.learn_cap:
        print(f"   {len(session.details)} distinct diagnostic(s) seen; "
              f"{len(session.learned)} case(s) kept as seeds for reaching a new one")
    for name in sorted(tally):
        counts = ", ".join(f"{k} {v}" for k, v in sorted(tally[name].items()))
        print(f"   {name:22} {counts}")
    if corpus.counts:
        print(f"-- cases are under {args.out}/; re-run one with "
              f"`python3 -m tools.anoieu_fuzz replay <file>`, and keep one with "
              f"`python3 -m tools.anoieu_fuzz promote {args.out}/<bucket>`")
    if args.format != "text" and corpus.new:
        keep = {f.bucket for f in corpus.new}
        records = [r for r in reporting.load(args.out) if r["bucket"] in keep]
        print(reporting.render(records, args.format))
    return 1 if corpus.new else 0


def cmd_one(args) -> int:
    session = Session(args)
    case = session.make(args.seed, args.mutate)
    sys.stdout.write(case.text())
    return 0


def cmd_replay(args) -> int:
    session = Session(args)
    with open(args.file, errors="replace") as f:
        text = f.read()
    suffix = os.path.splitext(args.file)[1] or ".cpc"
    case = Case(split_commands(text), session.mode, suffix, args.file, "replay")
    outcomes = session.ask(case)
    for o in outcomes:
        print(o.line())
    finding = judge(case, outcomes, session.reference)
    if finding is None:
        print("-- nothing to report: every checker agreed, and none fell over")
        return 0
    print(f"-- {finding.code} {finding.kind}: {finding.summary}")
    print(f"   bucket {finding.bucket}")
    return 1


def cmd_shrink(args) -> int:
    session = Session(args)
    with open(args.file, errors="replace") as f:
        text = f.read()
    suffix = os.path.splitext(args.file)[1] or ".cpc"
    case = Case(split_commands(text), session.mode, suffix, args.file, "shrink")
    finding = session.probe(case)
    if finding is None:
        print("-- this file reports nothing, so there is nothing to shrink",
              file=sys.stderr)
        return 2
    small, spent = shrink(case, session.probe, finding.bucket, args.shrink_budget)
    print(f"; {len(case.commands)} command(s) -> {len(small.commands)}, "
          f"{spent} run(s): {finding.summary}")
    sys.stdout.write(small.text())
    return 0


def cmd_promote(args) -> int:
    kept = []
    for source in args.dir:
        try:
            where = reporting.promote(source, args.corpus, owner=args.owner, note=args.note)
        except (FileNotFoundError, FileExistsError) as e:
            print(f"-- {e}", file=sys.stderr)
            return 2
        kept.append(where)
        print(f"-- promoted {os.path.relpath(where, ROOT)}")
    print(f"-- {len(kept)} reproducer(s) are now committed evidence. Run "
          f"`python3 tools/gen_open_findings.py` to give each one a row.")
    return 0


def cmd_report(args) -> int:
    records = reporting.load(args.corpus)
    if not records:
        print("-- nothing is promoted; a run writes candidates, `promote` keeps one")
        return 0
    text = reporting.render(records, args.format, color=not args.no_color)
    print(text.rstrip())
    if args.format == "text":
        print(f"-- {len(records)} promoted finding(s) in "
              f"{os.path.relpath(args.corpus or reporting.CORPUS, ROOT)}")
    return 1


def cmd_verify(args) -> int:
    """Re-run every promoted reproducer and compare against what was recorded.

    This is the fuzzer's half of "re-measuring", the slot
    `docs/reporting-policy.md` says carries the most weight: a follow-up that
    cannot reproduce the original finding is guessing. It is also how a promoted
    finding gets closed honestly -- a verdict that has moved is either a fix
    upstream or the binary having changed under us, and either way somebody
    should look rather than the row quietly staying open.

    A checker that is not on this machine is skipped and said to be skipped. A
    run comparing nothing passes vacuously, so it says how much it compared.
    """
    records = reporting.load(args.corpus)
    if not records:
        print("-- nothing is promoted, so there is nothing to verify")
        return 0
    changed = compared = 0
    for record in records:
        args.mode = record.get("mode", "proof")
        session = Session(args)
        case = Case(
            split_commands(open(record["case"], errors="replace").read()),
            session.mode,
            os.path.splitext(record["case"])[1],
            record["case"],
            "verify",
        )
        recorded = {o["checker"]: o["coarse"] for o in record.get("outcomes", [])}
        print(f"-- {record['bucket']}")
        for got in session.ask(case):
            want = recorded.get(got.checker)
            if want is None or got.coarse == "skipped":
                print(f"   {got.checker:12} not run")
                continue
            compared += 1
            if got.coarse == want:
                print(f"   {got.checker:12} ok        {got.status}")
            else:
                changed += 1
                print(f"   {got.checker:12} CHANGED   was {want}, is {got.coarse}"
                      f" ({got.status}: {got.detail[:70]})")
    print(f"-- {len(records)} reproducer(s), {compared} verdict(s) compared, "
          f"{changed} changed")
    if compared == 0:
        print("   nothing was compared: no configured checker is on this machine")
    return 1 if changed else 0


def cmd_explain(args) -> int:
    text = reporting.explain(args.code)
    if not text:
        print(f"-- no code called {args.code}; `list-codes` has the four of them",
              file=sys.stderr)
        return 2
    print(text.rstrip())
    return 0


def cmd_list_codes(args) -> int:
    for spec in CODES.values():
        print(f"{spec.code}  {spec.severity.value:8} {spec.title}")
    return 0


def cmd_checkers(args) -> int:
    cfg = load_config(args.config)
    for checker in from_config(cfg, args.checker):
        where = checker.resolve()
        print(f"{checker.name:10} {'ok ' if where else '-- '} {where or 'not found'}")
        for mode, argv in sorted(checker.modes.items()):
            print(f"           {mode:10} {' '.join(argv)}")
        if checker.env:
            print(f"           {'$' + checker.env:10} "
                  f"{os.environ.get(checker.env, '(unset)')}")
    signature = _find_signature(args.signature or cfg.get("signature", ""))
    print(f"signature  {'ok ' if signature else '-- '} {signature or 'none'}")
    return 0


# -- the parser ---------------------------------------------------------------


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--mode", choices=("proof", "signature"), default="proof",
                   help="write proofs against a fixed signature, or write signatures")
    p.add_argument("--config", default="", help="an anoieu-fuzz.json to lay over the defaults")
    p.add_argument("--checker", action="append", default=[],
                   help="run only this checker; repeatable")
    p.add_argument("--signature", default="",
                   help="the fixed signature proofs are written against "
                        "(default: $CPC, or the deps/ clone)")
    p.add_argument("--timeout", type=float, default=10.0,
                   help="seconds a checker gets per case (default 10)")
    p.add_argument("--wild", type=float, default=0.1,
                   help="how often to ignore what a type says (0..1, default 0.1)")
    p.add_argument("--depth", type=int, default=3, help="how deep a term may nest")
    p.add_argument("--extend", action="store_true",
                   help="signature mode: open each case by including the fixed "
                        "signature and write against its vocabulary, rather than "
                        "standing alone on a builtin prelude")
    p.add_argument("--reference", default="",
                   help="the checker a disagreement's direction is measured against "
                        "(default: ethos). Accepting what it refuses is the serious "
                        "direction, and is reported as an error")
    p.add_argument("--seed-corpus", action="append", default=[],
                   help="a file or directory of real cases to mutate; repeatable")
    p.add_argument("--mutate", type=float, default=0.5,
                   help="how often to mutate a seed rather than generate (default 0.5)")
    p.add_argument("--shrink-budget", type=int, default=120,
                   help="how many runs one shrink may spend (default 120)")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tools.anoieu_fuzz",
                                 description="a fuzzer for Eunoia-based proof checkers")
    ap.add_argument("--version", action="version", version=f"anoieu-fuzz {__version__}")
    sub = ap.add_subparsers(dest="command")

    r = sub.add_parser("run", help="generate cases and report what disagrees or falls over")
    _common(r)
    r.add_argument("-n", "--cases", type=int, default=200, help="how many cases")
    r.add_argument("--seed", default="0", help="the seed every case is derived from")
    r.add_argument("--jobs", type=int, default=1, help="cases to run at once")
    r.add_argument("--out", default="fuzz-findings", help="where findings are kept")
    r.add_argument("--metamorphic", action="store_true",
                   help="also compare each checker against itself on a reformatted copy")
    r.add_argument("--no-shrink", action="store_true", help="save cases as generated")
    r.add_argument("--max-findings", type=int, default=0, help="stop after this many new buckets")
    r.add_argument("--time-limit", type=float, default=0.0, help="stop after this many seconds")
    r.add_argument("-v", "--verbose", action="store_true", help="a line per case")
    r.add_argument("--no-learn", action="store_true",
                   help="do not keep a case that provoked a diagnostic never seen "
                        "before as a seed to mutate further")
    r.add_argument("--learn-cap", type=int, default=400,
                   help="how many such cases to keep (default 400)")
    r.add_argument("--format", choices=("text", "json", "github", "sarif"), default="text",
                   help="also print what was found in this shape, as diagnostics")
    r.set_defaults(fn=cmd_run)

    o = sub.add_parser("one", help="print one generated case")
    _common(o)
    o.add_argument("--seed", default="0")
    o.set_defaults(fn=cmd_one)

    p = sub.add_parser("replay", help="what each checker says about a file")
    _common(p)
    p.add_argument("file")
    p.set_defaults(fn=cmd_replay, metamorphic=False)

    s = sub.add_parser("shrink", help="cut a case down to what still provokes it")
    _common(s)
    s.add_argument("file")
    s.add_argument("--metamorphic", action="store_true")
    s.set_defaults(fn=cmd_shrink)

    pr = sub.add_parser("promote", help="move a reproducer into the committed corpus")
    pr.add_argument("dir", nargs="+", help="a bucket directory a run wrote")
    pr.add_argument("--owner", default="",
                    help="whose defect this is; defaults to the checker(s) involved")
    pr.add_argument("--note", default="", help="a line of context to keep with it")
    pr.add_argument("--corpus", default="", help="where to keep it; defaults to tests/fuzz/")
    pr.set_defaults(fn=cmd_promote)

    rp = sub.add_parser("report", help="every promoted finding, as diagnostics")
    rp.add_argument("--format", choices=("text", "json", "github", "sarif"), default="text")
    rp.add_argument("--no-color", action="store_true")
    rp.add_argument("--corpus", default="", help="defaults to tests/fuzz/")
    rp.set_defaults(fn=cmd_report)

    v = sub.add_parser("verify", help="do the promoted reproducers still do what the record says")
    _common(v)
    v.add_argument("--corpus", default="", help="defaults to tests/fuzz/")
    v.set_defaults(fn=cmd_verify, metamorphic=False)

    ex = sub.add_parser("explain", help="what a code means")
    ex.add_argument("code")
    ex.set_defaults(fn=cmd_explain)

    lc = sub.add_parser("list-codes", help="every code the fuzzer reports under")
    lc.set_defaults(fn=cmd_list_codes)

    c = sub.add_parser("checkers", help="what is configured, and what is on this machine")
    c.add_argument("--config", default="")
    c.add_argument("--checker", action="append", default=[])
    c.add_argument("--signature", default="")
    c.set_defaults(fn=cmd_checkers)

    args = ap.parse_args(argv)
    if not getattr(args, "fn", None):
        ap.print_help()
        return 2
    return args.fn(args)
