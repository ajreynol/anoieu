#!/usr/bin/env python3
"""Print the state of the Eunoia ecosystem: who is in it, and how they look.

No assistant and no prompting -- this is a local command that reads trees and
reports. It is the thing to run when the question is *where does everything
stand*; `prompts/global_audit` is the thing to run when the question needs
somebody to read across the answer and form a view.

    scripts/status_eo            # the table
    scripts/status_eo --verbose  # and why each policy verdict came out
    scripts/status_eo --check    # is the inventory itself still true?
    scripts/status_eo --check --online   # ... and ask each remote

Health here means **what can be established from a checkout in about a second**:
does it declare membership, does the policy check pass, is there a channel to
reach them, how long since anything moved. It deliberately does not build,
test, or read anybody's source. A row that says `ok` is a claim about form, and
a quiet row is not evidence that a tool is well -- the same caution the analyzer
carries about its own silence applies here.

Membership is a decision rather than a measurement, so the `status` column comes
from `scripts/ecosystem/ecosystem.json` and is never inferred. Where the measurement and the
recorded status disagree, the row says so; changing the file is a person's job.

`--check` is the same principle with an exit code, and it is what CI runs. Two
questions, and the second is why it exists:

**Is the inventory well formed?** Offline, and always: every entry has the fields
its status requires, every parent named by a child exists, no two ids are one
typo apart, and every repository the board addresses has a row here.

**Is it still true?** With `--online`, each entry that is somebody's own
repository has its README fetched from the remote and read for the membership
declaration, by `policy_check.declaration_in` — the same function that decides it
on a checkout. A tool recorded as a candidate that now declares membership is a
stale inventory, and so is a member that has stopped declaring. That is the
failure this was written for: three tools joined and the file did not move for
long enough that nobody could say from the file alone which of them had.

**What it cannot see** is whether a declaration is backed: that needs their whole
tree and their own CI is where it is decided. A remote that cannot be reached is
reported and not counted against anybody -- a network error is evidence about the
network.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INVENTORY = os.path.join(HERE, "ecosystem.json")
REPOS_FILE = os.environ.get("ANOIEU_REPOS_FILE",
                            os.path.join(ROOT, "scripts", "repos.local"))


#: What each status requires of an entry, beyond `what`.
#:
#: `associate` requires `vetted` and `why`, and nothing else requires either. A
#: footing that rests on our judgement rather than on their declaration carries
#: the date a person last made that judgement and what they made it about, or it
#: becomes a claim that only ever accumulates. `why` is what we vetted them
#: *as* -- why they are load-bearing for us -- and is not a second `what`.
REQUIRED = {
    "member": ("repo", "url"),
    "associate": ("repo", "url", "vetted", "why"),
    "candidate": ("repo", "url"),
    "foundation": ("repo", "url"),
    "child": ("parent",),
    # A tool outside this ecosystem that we track and are **not** proposing to
    # promote. It exists so that "how active were we this stretch" has
    # something to be compared against: our own numbers alone say nothing about
    # whether five days of commits is a lot. `why` is what it is being compared
    # for, and `vetted` is the date somebody last looked at the entry -- because
    # writing about a project that never asked to be written about should carry
    # a date the way every other claim here does.
    "outsider": ("repo", "url", "vetted", "why"),
    # The office, which `docs/laws.md` makes a footing. It asks for exactly what
    # `member` asks for because **a president is a member** -- LAW 2 binds it
    # like any other, and the office adds obligations rather than replacing
    # them. It is a separate status and not a flag on `member` because the
    # laws put it in the same table as the others, and because only one
    # repository holds it at a time, which `--check` enforces below.
    "president": ("repo", "url"),
}

#: The footings that are membership. A president is one of them: the office is
#: held *by* a member, so every count, every policy check and every question
#: asked of a member's README applies to it unchanged.
MEMBERS = ("member", "president")

#: The files the office is kept in, and the test for *limbo* -- the registry
#: recording a repository as president while its tree cannot hold the office.
#: The office moves by a person editing one line; these are carried by somebody
#: doing the work, and the gap between the two acts is the state this detects.
#: Reported against the row and never enforced: the remedy is somebody carrying
#: files, and a red build carries nothing.
PRESIDENT_FILES = {
    "docs/laws.md": "the laws, which the president maintains",
    "docs/history.md": "its account of its own term",
}

#: A footing an entry says we *intend*, in `proposed`, while its `status` stays
#: what is true today. It exists because the associate protocol is drafted and
#: not decided: recording the intention as the fact would be this file asserting
#: something nobody has agreed to, and recording nothing would lose it.
PROPOSABLE = ("associate",)

#: The statuses whose entry asserts something about a README somebody else
#: keeps, and which `--online` therefore reads. `foundation` is deliberately not
#: here: its entry is a fact about *our* arrangement, asserts nothing about their
#: tree, and asking them for anything is what that footing exists to refuse.
OWN_REPO = ("member", "president", "associate", "candidate")


# The key printed under the table. A reader who cannot decode `3 failing` in a
# `candidate` row cannot tell a disagreement from a measurement, and the table
# had been printing that distinction for months without saying it anywhere.
#
# These are a **copy**: what a footing means is decided in `docs/policy.md`, and
# what a verdict means is decided by `check()` and by the branches in `main()`
# below. So the copy is named by its ground truth and compared to it --
# `key_is_complete` in tests/run.py fails when a footing exists in `REQUIRED`
# and not here. Nothing compares the prose, which is the half that can still rot.

#: One line per footing, in the order a reader meets them. Keep the keys equal
#: to `REQUIRED`'s; the value says how to *read the column*, never what the
#: footing means in full -- that is the policy's, and is linked below.
FOOTINGS = {
    "president": "a member, and holds the office. This column is the authority "
                 "on who that is; a note says so if the tree cannot hold it",
    "member": "declared membership. Held to the policy, and checked here",
    "candidate": "has not joined. The policy is addressed to them and binds them to nothing",
    "associate": "load-bearing for us, and owes us nothing. Never checked",
    "foundation": "the ecosystem is downstream of it. Asked for nothing, ever",
    "child": "a project inside another repository, on its parent's footing",
    "outsider": "outside the ecosystem, tracked so our own numbers have something "
                "to be compared against",
}

#: Every value the `policy` column can print, and what it means.
POLICY_VALUES = (
    ("ok", "every check that applies to that tree passed"),
    ("N failing", "N of our checks failed on it"),
    ("not held", "an associate. Nothing was run, and that is the footing"),
    ("no checkout", "not on this machine, so nothing could be run"),
    ("-", "a child or a foundation: not a repository this table checks"),
)

#: Every value the `channel` column can print, and what it means.
CHANNEL_VALUES = (
    ("N for us", "N topics in it are addressed to anoieu"),
    ("yes", "they keep one, and nothing in it is for us"),
    ("none", "they keep none. Not a defect: the file is optional"),
    ("-", "a child or a foundation"),
)


def render_key() -> str:
    """The legend. Printed by `--help` and by nothing else.

    It ends with what to do about a failing row, because that is the question
    the table provokes and the one it was answering nowhere: the count is here,
    the detail is in another program, and which of the two repositories owns the
    problem depends on a column further left.

    **Not printed under the table.** It is twenty-odd fixed lines against a
    twenty-four line table, read once and never again, in a command that is run
    often -- so under the table it is the bulk of the output every time in order
    to be useful once. The table carries a one-line pointer to it instead, which
    is the part that cannot be dropped: a legend nobody is told about is not a
    legend, and *print it every run* and *do not mention it* are both wrong.
    """
    values = (tuple(FOOTINGS.items()), POLICY_VALUES, CHANNEL_VALUES)
    # One width across all three lists, so every description starts in the same
    # column. Widths computed per list read as three tables that happen to be
    # adjacent, which is what they looked like when this was first written.
    w = max(len(k) for group in values for k, _ in group) + 2

    def block(group) -> None:
        for k, why in group:
            out.append(f"             {k:<{w}}{why}")

    out = ["key"]
    out.append("  tool     its id in scripts/ecosystem/ecosystem.json -- what every prompt "
               "here calls it by")
    out.append("  status   what it owes us, and what we say about it. In full: "
               "docs/policy.md,")
    out.append("           \"The footings, and what each one costs whom\"")
    block(FOOTINGS.items())
    out.append("  policy   scripts/policy_check.py, run over that checkout by this "
               "command just now")
    block(POLICY_VALUES)
    out.append("  channel  their docs/discussion.md, which is optional and which "
               "most tools do not keep")
    block(CHANNEL_VALUES)
    out.append("  moved    days since the last commit in the checkout on this "
               "disk, not on their remote")
    out.append("  where    where that checkout is")
    out.append("")
    out.append("fixing a `N failing` row")
    out.append("  The count is all this table has. To see what failed:")
    out.append("      python3 scripts/policy_check.py --root <where>")
    out.append("  Each FAIL line names the check and what it found.")
    out.append("  Whose it is to fix depends on the status column, and the two "
               "cases are not alike.")
    out.append("    member, president  they declared they follow this, so the "
               "tree and the claim")
    out.append("                       disagree. Theirs to fix, and a note "
               "below says so by name.")
    out.append("    anything else      they never agreed to any of this. It is a "
               "measurement and")
    out.append("                       not a shortfall, nobody owes us the fix, "
               "and it is not")
    out.append("                       something to open a topic about.")
    out.append("  And where the check is wrong -- it fires on something that is "
               "not a problem,")
    out.append("  or the policy does not fit a legitimate shape of repository -- "
               "that one is")
    out.append("  ours, and it is fixed here in docs/policy.md or "
               "scripts/policy_check.py.")
    return "\n".join(out)


def git(*args, cwd=None):
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else ""


def locate(repo: str) -> str:
    """A repo id, the way every script here resolves one: the mapping file, then
    a scan of $ANOIEU_REPOS. Never a bare path -- these ids come from a file."""
    if os.path.isfile(REPOS_FILE):
        for line in open(REPOS_FILE, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) == 2 and parts[0] == repo:
                path = os.path.expanduser(parts[1].strip())
                if os.path.isdir(path):
                    return path
    for r in os.environ.get("ANOIEU_REPOS", os.path.expanduser("~")).split(":"):
        cand = os.path.join(r, repo)
        if os.path.isdir(cand):
            return cand
    return ""


def age(path: str) -> str:
    when = git("log", "-1", "--format=%cI", cwd=path)
    if not when:
        return "?"
    then = datetime.datetime.fromisoformat(when)
    days = (datetime.datetime.now(then.tzinfo) - then).days
    return "today" if days == 0 else f"{days}d"


def check(path: str) -> tuple[str, list[str]]:
    out = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "policy_check.py"),
         "--root", path], capture_output=True, text=True)
    # count the failing *checks*, not their detail lines: one check that reports
    # three things is one thing wrong, and saying "3 fail" overstates it.
    failed = [l[5:] for l in out.stdout.splitlines() if l.startswith("FAIL ")]
    detail = [l.strip() for l in out.stdout.splitlines() if l.startswith("     ")]
    return ("ok" if out.returncode == 0 else f"{len(failed)} failing"), detail


def near(a: str, b: str) -> bool:
    """Whether two ids are one edit apart, by the same rule `welcome_eo` uses."""
    out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "ecosystem", "near.py"), a, b],
                         capture_output=True, text=True)
    return out.stdout.strip() == "1"


def board_entities() -> set[str]:
    """Every repository the board addresses, from its `Entities` lines."""
    path = os.path.join(ROOT, "docs", "board.md")
    if not os.path.isfile(path):
        return set()
    out = set()
    for line in open(path, encoding="utf-8"):
        m = re.match(r"\*\*Entities:\*\* (.+)", line.strip())
        if m:
            out |= {e.strip(" `") for e in m.group(1).split(",")}
    return out


def well_formed(inv: dict) -> list[str]:
    """The inventory read as a document about itself. No network, no checkouts."""
    bad = []
    for name, e in inv.items():
        status = e.get("status", "")
        if status not in REQUIRED:
            bad.append(f"{name}: status {status or '(none)'} is not one this file defines")
            continue
        for field in REQUIRED[status] + ("what",):
            if not e.get(field):
                bad.append(f"{name}: a {status} entry needs `{field}`")
        if status == "child":
            parent = e.get("parent", "")
            if parent not in inv:
                bad.append(f"{name}: its parent `{parent}` is not in this file")
            elif inv[parent].get("status") == "child":
                bad.append(f"{name}: its parent `{parent}` is itself a child project")
        proposed = e.get("proposed", "")
        if proposed:
            if proposed not in PROPOSABLE:
                bad.append(f"{name}: `proposed` is {proposed!r}, and the only "
                           f"footing that may be proposed is {PROPOSABLE[0]!r}")
            elif proposed == status:
                bad.append(f"{name}: proposes the footing it already holds; "
                           "`proposed` records an intention, not the fact")
            else:
                # An intention nobody has read the tree for is a wish. The same
                # two fields the footing itself requires are required to propose
                # it, which is what stops `proposed` becoming a cheaper way in.
                for field in ("vetted", "why"):
                    if not e.get(field):
                        bad.append(f"{name}: proposing `{proposed}` needs `{field}`, "
                                   "the same as holding it")
        url = e.get("url", "")
        if url and not url.startswith("https://"):
            bad.append(f"{name}: `{url}` is not an https url")
    # `docs/laws.md`, LAW 3: there is a president, "one at a time". A file that
    # records two has recorded a handover that did not finish, which is the one
    # way this footing can go wrong silently -- both rows look correct alone.
    held = [k for k, v in inv.items() if v.get("status") == "president"]
    if len(held) > 1:
        bad.append("two repositories are recorded as president -- "
                   + ", ".join(sorted(held))
                   + " -- and the office is held one at a time")
    names = sorted(inv)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if near(a, b):
                bad.append(f"`{a}` and `{b}` are one character apart, which is a "
                           "typo before it is two tools")
    for entity in sorted(board_entities() - set(inv)):
        bad.append(f"docs/board.md addresses `{entity}`, which has no row here")
    return bad


def readme_of(url: str, timeout: int = 20) -> tuple[str, str]:
    """A repository's README, from its remote. Returns (text, why-not).

    Read over https rather than by cloning, because this runs on every push and
    the question is one file. Only GitHub urls can be turned into a raw one from
    here; anything else is reported as unreadable rather than guessed at.
    """
    m = re.match(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url)
    if not m:
        return "", f"{url} is not a github url this can read a file from"
    raw = f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/HEAD/README.md"
    try:
        with urllib.request.urlopen(raw, timeout=timeout) as r:  # noqa: S310
            return r.read().decode("utf-8", "replace"), ""
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "", ""          # no README is an answer, not a failure to ask
        return "", f"{raw}: HTTP {e.code}"
    except (urllib.error.URLError, OSError, ValueError) as e:
        return "", f"{raw}: {str(e)[:60]}"


def still_true(inv: dict) -> tuple[list[str], list[str]]:
    """Ask each remote whether the status recorded here is still the right one.

    Returns (failures, unreachable). Unreachable is neither: it is a fact about
    the network, and counting it as a stale inventory would make this job red for
    something nobody here can fix.
    """
    sys.path.insert(0, os.path.dirname(HERE))
    import policy_check  # noqa: PLC0415

    bad, unseen = [], []
    for name, e in inv.items():
        status = e.get("status")
        if status not in OWN_REPO:
            continue
        text, why = readme_of(e.get("url", ""))
        if why:
            unseen.append(f"{name}: {why}")
            continue
        missing = policy_check.declaration_in(text)
        declares = not missing
        if status == "candidate" and declares:
            bad.append(f"{name} declares membership on its default branch and is "
                       "recorded here as a candidate: it has joined, and this file "
                       "has not been told")
        if status in MEMBERS and not declares:
            bad.append(f"{name} is recorded here as a {status} and its README "
                       f"does not declare membership: {missing[0]}")
        if e.get("proposed") == "associate" and status != "associate":
            # Reported through the return value's second channel, which is what
            # `unreachable` uses: this is not a stale inventory. The file says we
            # intend something and it has not happened, which is exactly true.
            if policy_check.note_in(text):
                unseen.append(f"{name}: proposed as an associate and its README "
                              "carries no maintenance note -- `--protocol` is the "
                              "report, and nothing here is owed")
            continue
        if status == "associate":
            # The affiliating note is asked about first, and a tree that carries
            # one is settled: its refusal clause is what stops `declaration_in`
            # reading it as a declaration, so the two can never both be true.
            # Only a tree with no affiliating note can have joined outright.
            gone = policy_check.affiliation_in(text)
            if not gone:
                pass
            elif declares:
                bad.append(f"{name} declares full membership and is recorded here "
                           "as an associate: it has joined, and this file has not "
                           "been told")
            else:
                bad.append(f"{name} is recorded here as an associate and its "
                           f"README does not carry the affiliating note: {gone[0]}")
    return bad, unseen


def readme_for(name: str, e: dict) -> tuple[str, str]:
    """A tool's README, from its checkout if there is one and from its remote
    otherwise. Returns (text, source), where source is what to print.

    The checkout is preferred because this report is run while somebody is
    deciding something and a network round trip per tool makes it a job rather
    than a command. Which one answered is printed, because a stale checkout and
    a published README are different claims and the difference matters here.
    """
    path = locate(e.get("repo", name))
    if path:
        rel = os.path.join(path, "README.md")
        if os.path.isfile(rel):
            return open(rel, encoding="utf-8").read(), "checkout"
    text, why = readme_of(e.get("url", ""))
    return (text, "remote") if not why else ("", "unreachable")


def protocol(inv: dict) -> int:
    """`--protocol`: who would satisfy the associate protocol, in each of the
    versions of it that is still on the table.

    **It reports and it never fails.** Every repository in it is held to none of
    this, most of them have not been asked, and the protocol itself is drafted
    rather than decided -- see *The associate protocol* in `docs/policy.md`. A
    non-zero exit here would be this repository grading somebody for failing to
    comply with a rule that does not exist yet.

    Three columns, because the undecided question is *which* of them we would
    require, and a person deciding that should be able to see what each would
    cost today rather than predict it:

      note          a `How this repository is maintained` heading, with
                    something under it. The drafted protocol, and the whole of it
      affiliating   that, and a paragraph naming the ecosystem and saying the
                    repository is not held to its policy. The stronger option
      declares      a full membership declaration, which no associate needs and
                    which would mean the footing is the wrong one
    """
    sys.path.insert(0, os.path.dirname(HERE))
    import policy_check  # noqa: PLC0415

    rows = []
    for name, e in inv.items():
        status, want = e.get("status", ""), e.get("proposed", "")
        if "associate" not in (status, want):
            continue
        text, source = readme_for(name, e)
        if source == "unreachable":
            rows.append((name, status, want, "?", "?", "?", "unreachable"))
            continue
        yes = lambda missing: "no" if missing else "yes"  # noqa: E731
        rows.append((name, status, want,
                     yes(policy_check.note_in(text)),
                     yes(policy_check.affiliation_in(text)),
                     yes(policy_check.declaration_in(text)),
                     source))

    if not rows:
        print("-- nobody holds or is proposed for `associate`, so there is "
              "nothing to report")
        return 0

    w = max(len(r[0]) for r in rows) + 2
    print(f"{'tool':<{w}}{'footing':<12}{'proposed':<11}"
          f"{'note':<7}{'affiliating':<13}{'declares':<10}read from")
    for name, status, want, a, b, c, source in rows:
        print(f"{name:<{w}}{status:<12}{want or '-':<11}{a:<7}{b:<13}{c:<10}{source}")

    print()
    print("The protocol is drafted, not decided: docs/policy.md, "
          "`The associate protocol`.")
    print("Nothing here is a verdict and nothing here fails. Every tool in this "
          "table is held")
    print("to none of this repository's policy, and most of them have not been "
          "asked to be.")
    return 0


#: A health summary is a small, fixed list of **indicators**. Each is a name, a
#: value a person can read, and one of three verdicts. The set is deliberately
#: short and is expected to grow; adding one is a decision rather than a
#: convenience, because every renderer shows all of them.
#:
#: `unknown` is a verdict and not a missing value. It sits with `attention`
#: rather than with `ok`, for the same reason the bump gate has three exit codes:
#: *we asked and it is wrong* and *we could not ask* are different facts, and
#: neither is a pass.
VERDICTS = ("ok", "attention", "unknown")


def health(inv: dict | None = None) -> list[tuple[str, str, str]]:
    """The ecosystem's health, as (indicator, value, verdict).

    **Offline and cheap on purpose.** Everything here is read off this disk, so
    any surface can render it without deciding whether it can afford to. What
    costs a network call -- whether our build is green at a commit -- is
    deliberately not here: use bump_check.py when considering a new policy pin.

    Returned as data rather than printed, because several surfaces render it and
    a second implementation of the rendering is how they drift apart.
    """
    if inv is None:
        inv = {k: v for k, v in json.load(open(INVENTORY, encoding="utf-8")).items()
               if not k.startswith("_")}
    members = [k for k, v in inv.items() if v.get("status") in MEMBERS]

    passing, unknown, owed = 0, 0, 0
    for name in members:
        path = locate(inv[name].get("repo", name))
        if not path:
            unknown += 1
            continue
        verdict, _ = check(path)
        passing += 1 if verdict == "ok" else 0
        disc = os.path.join(path, "docs", "discussion.md")
        if os.path.isfile(disc):
            owed += open(disc, encoding="utf-8").read().count("**To:** anoieu")

    # Soft on purpose. The schedule mechanism is maintained by a child project,
    # and a child project may be deleted without anything else noticing -- so
    # this asks for it and carries on without it. The reference is still a
    # rule 10 break and is recorded as one in that project's charter; what it
    # is not is a dependency that takes the health summary down with it.
    sys.path.insert(0, os.path.join(ROOT, "tools", "martyria"))
    try:
        import sleep as sleep_tool  # noqa: PLC0415
        clock = sleep_tool.state()
    except Exception:  # noqa: BLE001
        sleep_tool, clock = None, None

    def verdict(ok, unsure=False):
        return "unknown" if unsure else ("ok" if ok else "attention")

    return [
        ("members", str(len(members)), "ok"),
        ("policy", f"{passing} of {len(members)} passing",
         verdict(passing == len(members), unknown > 0)),
        ("topics owed to us", str(owed), verdict(owed == 0)),
        # The one indicator that is about the runner rather than the tree, and
        # the one whose value changes without anybody committing anything. It
        # is marked `attention` outside the window because the mark is the
        # whole intervention -- see PROTO-18. It is never `unknown`: a missing
        # schedule means the default window, not an unanswerable question.
        ("hours",
         sleep_tool.summary(clock) if clock else "no schedule mechanism",
         verdict(clock and clock["status"] == "awake", clock is None)),
    ]


def render_health(rows: list[tuple[str, str, str]]) -> str:
    """One rendering, used everywhere a health summary appears."""
    w = max(len(n) for n, _, _ in rows)
    mark = {"ok": " ", "attention": "!", "unknown": "?"}
    return "\n".join(f"  {m} {n:<{w}}  {v}"
                      for n, v, k in rows for m in [mark[k]])


def audit(online: bool) -> int:
    """`--check`: the inventory as a document, and optionally as a claim.

    Named apart from `check` above, which asks the policy checker about one
    checkout. The two were briefly the same name, and the table stopped working
    for as long as that was true.
    """
    inv = json.load(open(INVENTORY, encoding="utf-8"))
    inv = {k: v for k, v in inv.items() if not k.startswith("_")}

    bad = well_formed(inv)
    for b in bad:
        print(f"FAIL {b}")
    print(f"-- the inventory is well formed: {len(bad)} failure(s), "
          f"{len(inv)} entries")

    if not online:
        print("-- whether it is still true was not asked: --online does that")
        return 1 if bad else 0

    stale, unseen = still_true(inv)
    for b in stale:
        print(f"FAIL {b}")
    for u in unseen:
        print(f"     unreachable, so unasked: {u}")
    asked = sum(1 for e in inv.values() if e.get("status") in OWN_REPO) - len(unseen)
    print(f"-- who has joined is current: {len(stale)} failure(s), {asked} asked")
    print("   One section of one README is what this reads: a declaration for a "
          "member,\n   an affiliating note for an associate. Whether their tree "
          "backs a declaration is\n   decided by their own CI, running the same "
          "checker, and is not visible from here.")
    print("   Whether an associate is still worth vetting is nobody's to decide "
          "from here\n   either: the `vetted` date says when a person last did, "
          "and it does not expire\n   on its own.")
    return 1 if bad or stale else 0


USAGE = """usage: status_eo [--verbose] [--check [--online]] [--health] [--protocol]

  (no arguments)  the table: one row per tool in scripts/ecosystem/ecosystem.json
  --verbose       ... and, per tool, which checks failed and what they found
  --check         is the inventory itself well formed? No network, no checkouts
  --check --online  ... and does each remote's README still agree with it
  --health        the one-line-per-question health report
  --protocol      where each tool proposed for `associate` stands against the
                  drafted protocol. Reports, and never fails
  --help          this, and the key below
"""


def main() -> int:
    if "--help" in sys.argv or "-h" in sys.argv or "-help" in sys.argv:
        print(USAGE)
        print(render_key())
        return 0
    if "--check" in sys.argv:
        return audit("--online" in sys.argv)
    if "--health" in sys.argv:
        print(render_health(health()))
        return 0
    if "--protocol" in sys.argv:
        inv = json.load(open(INVENTORY, encoding="utf-8"))
        return protocol({k: v for k, v in inv.items() if not k.startswith("_")})
    verbose = "--verbose" in sys.argv
    inv = json.load(open(INVENTORY, encoding="utf-8"))
    rows, notes = [], []

    for name, e in inv.items():
        if name == "_comment":
            continue
        status = e.get("status", "?")
        if status in ("child", "foundation"):
            rows.append((name, status, "-", "-", "-", e.get("parent", "")))
            continue
        path = locate(e.get("repo", name))
        if not path:
            rows.append((name, status, "no checkout", "-", "-", ""))
            continue
        # An associate is held to none of this, so nothing here runs the checker
        # over its tree. A failure count in that row would be this table
        # grading somebody who never agreed to be graded, which is the whole of
        # what the footing refuses.
        verdict, fails = ("not held", []) if status == "associate" else check(path)
        topics = ""
        disc = os.path.join(path, "docs", "discussion.md")
        if os.path.isfile(disc):
            text = open(disc, encoding="utf-8").read()
            for_us = text.count("**To:** anoieu")
            topics = f"{for_us} for us" if for_us else "yes"
        else:
            topics = "none"
        rows.append((name, status, verdict, topics, age(path), path))
        # Both notes name the disagreement and then say whose move it is.
        # They used to state the rule instead -- "this is the state the check
        # exists to catch" -- which explains the check to somebody who already
        # knows why it is there, and tells a reader arriving cold nothing they
        # can act on.
        if verdict == "ok" and status == "candidate":
            notes.append(
                f"{name} passes our checks but we still have it down as a "
                "candidate rather than a member. If it has joined since, our "
                "inventory is out of date -- ours to fix, in scripts/ecosystem/ecosystem.json")
        if verdict != "ok" and status in MEMBERS:
            # The count comes from `verdict`, which counts failing *checks*.
            # `fails` is their detail lines and there are more of them -- the
            # overstatement `check()` warns about three lines above its return.
            n_fail = verdict.split()[0]
            where_short = path.replace(os.path.expanduser("~"), "~")
            notes.append(
                f"{name} says it follows the shared policy, and {n_fail} of our "
                "checks fail on its tree. Theirs to fix, not ours. To see what: "
                f"python3 scripts/policy_check.py --root {where_short}")
        # Limbo. Said against the row rather than left for somebody to notice,
        # because it is the one state here that is supposed to be brief: while
        # it lasts nobody is keeping the laws and nothing is recording the term.
        if status == "president":
            absent = [f"`{f}` ({why})" for f, why in PRESIDENT_FILES.items()
                      if not os.path.isfile(os.path.join(path, f))]
            if absent:
                notes.append(
                    f"IN LIMBO: the registry records {name} as president and its "
                    f"tree does not carry {', '.join(absent)}. The office has "
                    "moved and the means of holding it have not. Fix it quickly "
                    "-- carry the files, or put the registry line back. Nothing "
                    "here fails a build over it")

        # A checkout whose directory is not called what the inventory calls it.
        # Said loudly because the quiet version of this cost us a member: the
        # tree was on disk as `eudiamonia`, the inventory said `eudaimonia`, and
        # the row read `no checkout` for a repository that was right there --
        # hiding its failures and eleven topics it was owed. A near-miss is
        # worse than an absence: absence is obvious and this is not.
        if path:
            want = inv[name].get("repo", name)
            got = os.path.basename(os.path.normpath(path))
            if got != want:
                notes.append(f"NAME MISMATCH: {name} is checked out as `{got}` "
                             f"and we expect `{want}`. One of the two is a typo, "
                             "and until it is fixed this row is resolved by a "
                             "hand-written line in scripts/repos.local rather "
                             "than by its name")
        if verbose and fails:
            notes.append(f"{name}: " + "; ".join(fails[:6]))

    w = max(len(r[0]) for r in rows) + 2
    print(f"{'tool':<{w}}{'status':<11}{'policy':<12}"
          f"{'channel':<10}{'moved':<8}where")
    for name, status, verdict, topics, moved, where in rows:
        short = where.replace(os.path.expanduser("~"), "~") if where else ""
        print(f"{name:<{w}}{status:<11}{verdict:<12}"
              f"{topics:<10}{moved:<8}{short}")

    # The pointer, not the key. One line, immediately under the table, because
    # the moment somebody needs the legend is the moment they are looking at a
    # column they cannot read.
    print()
    print("-- what the columns mean, and what to do about a failing row: "
          "status_eo --help")

    if notes:
        print()
        for n in notes:
            print(f"note: {n}")

    counts: dict[str, int] = {}
    for r in rows:
        counts[r[1]] = counts.get(r[1], 0) + 1
    members = [r for r in rows if r[1] in MEMBERS]
    passing = sum(1 for r in members if r[2] == "ok")
    owed = sum(int(r[3].split()[0]) for r in rows if r[3].endswith("for us"))

    #: Plurals not formed by adding an s.
    PLURAL = {"child": "children"}
    parts = ", ".join(f"{n} {PLURAL.get(k, k + 's') if n != 1 else k}"
                      for k, n in sorted(counts.items(), key=lambda kv: -kv[1]))

    # One sentence, last, after everything. A reader who wants the state of the
    # ecosystem should not have to add a column up themselves, and it is held to
    # one sentence because a summary that grows into a paragraph is a second
    # report -- and then there are two of them to keep true.
    print()
    print(f"In short: {parts}; {passing} of {len(members)} members pass their "
          f"policy check, {owed} topic{'s' if owed != 1 else ''} "
          f"{'are' if owed != 1 else 'is'} owed to us, "
          "and how good any of these tools actually are is a judgement kept in "
          "docs/report-card.md rather than in this table.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
