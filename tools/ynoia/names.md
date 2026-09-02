# The names

A register of names the ecosystem has reserved, what each was reserved *for*,
and whether anybody has taken it. Kept here because naming a tool that does not
exist is what this project spends most of its time doing, and because a brand
new repository needs one page rather than an argument.

**Nothing here is an assignment.** A reserved name is a description somebody
wrote down, not work anybody promised. Taking one commits you to the shape of
the description or to changing it, and either is fine — what is not fine is
taking a name whose description you have not read.

## The convention

Greek, and preferably from the vocabulary the ecosystem already draws on. The
name should **describe the work** rather than decorate it, and the repository's
own README explains the etymology in a sentence somebody can disagree with. Two
tests, both cheap: a name that needs no explanation is not following the
convention, and a name whose explanation is strained means the scope has not
been decided yet.

Descriptive non-Greek names are allowed where the thing is a program rather than
an account — `anoieu_fuzz` is one — but the burden is on the name to earn it.

**And the convention has a second reason, found by breaking it.** A child
project named with an ordinary English word makes every sentence using that word
ambiguous — proper noun, or common one — and the ambiguity is not only a reading
cost. `tools/policy_check.py` decides whether a child project is an island by
grepping the tree for **the bare project name**, so a common word matches prose
about the *subject* rather than about the project, and reports an island break
that is not one. An unusual name reads unambiguously and greps unambiguously,
and those turn out to be the same property. The case is written up in
[`../martyria/README.md`](../martyria/README.md), which was named `ethics` for
about an hour.

## Taken

| name | what it is |
| --- | --- |
| **eunoia** | the language itself — εὔνοια, *good thinking* |
| **ethos** | the proof checker |
| **logos** | the **L**ean development — the initial is load-bearing, and is what makes `iogos` below a joke |
| **eudaimonia** | the calculus template |
| **anoieu** | the analyzer; *eunoia* read backwards |
| **dokimasia** | δοκιμασία, the scrutiny before office: what no proof step covers |
| **sapheneia** | σαφήνεια, clarity of an account: Eunoia as a language definition. A child project, in anoieu |
| **ynoia** | *why Eunoia*: whether the arrangement earns its machinery. A child project, in anoieu |
| **euthyna** | εὔθυνα, the audit at end of term: what logos's proof is made of. **Started**, in eudaimonia |
| **martyria** | μαρτυρία, testimony — the evidence a witness gives: the **actionable** ethics project. One situation at a time, the evidence it rests on, and a stance somebody can act on. Also the name of one entry in its register. **Started**, in anoieu |
| **zetesis** | ζήτησις, inquiry — the seeking, as against the having-found: the **general** half. What standard this ecosystem is held to, taken from work done outside, and whether our record could show we met it. It has no standard yet, which is why the name is the one it is. **Started**, in anoieu |
| **koine** | κοινή, *the common tongue* — the shared dialect that let people who spoke differently understand each other. The shared machinery of the reporting loop, so the protocol has one implementation rather than one per member. **Its own repository**, and a member; audited as [`P1`](proposals.md) |
| **workflow-launcher** | descriptive rather than Greek, and the register's own exception applies: it is a program and not an account. The first hour of a new tool's life, and a register of what this ecosystem's practice turns out to be doing. A child project, in eudaimonia |

**Names chosen outside this ecosystem are not here.** `cvc5` and `ethos-eoc` are
in [`../ecosystem.json`](../ecosystem.json) and will never be in this table: it
registers names *we* reserved, and theirs were settled by other people before any
of this existed. An entry in the inventory with no row here is a gap only when
the name was ours to choose.

## Reserved, and free to take

Each was named in [`why-eunoia.md`](why-eunoia.md) because some argument there is
stated relative to its absence. None has a repository or a line of code.

| name | Greek | what it would be |
| --- | --- | --- |
| **tekton** | τέκτων, the builder — the joiner who makes one thing out of parts | the **epoch build system**: the program behind the protocols by which a stretch is verified, announced, approved and adopted. Requested by anoieu, 2026-09-01, and the one name here whose subject already exists — the protocols are running by hand and the tool is what is missing. *Not a verb of examination, which most of this register is; `apodeixis` — ἀπόδειξις, demonstration — was the alternative considered, and would have been the better name if the thing turns out to be a prover of gates rather than an assembler of a stretch. It is **not available**: see* In use elsewhere*, below.* |
| **pathos** | πάθος, the third mode of persuasion | an efficient *verified* proof checker — the one that would let the ecosystem ship what it proves rather than a second implementation |
| **hermeneia** | ἑρμηνεία, interpretation | carrying the embedded semantics into Lean's own logic, so a theorem about a proof becomes a theorem about the thing proved |
| **noesis** | νόησις, the act of understanding | the semantics and the compiler defined *in* Lean rather than compiled into it |
| **iogos** | not Greek: `logos` with the **L** of Lean swapped for the **I** of Isabelle. The one joke in the register, and it earns its place by fixing the scope in the name | the same calculus, semantics and soundness development redone against Isabelle/HOL — an Isabelle backend for `ethos-eoc`, and logos rebuilt on it, as an independence check |
| **elenchos** | ἔλεγχος, cross-examination | differential fuzzing derived from the calculus rather than written by hand — what the fuzzer here is a deliberate baseline for |

## In use elsewhere, and claimed by nobody

Names a tree in this ecosystem is actually using, which no one has entered in
the tables above. **They are not free.** The section exists because this
register once reported a name as free when a neighbouring tree was already
using it, and a name was taken on the strength of that.

| name | where | why it is not in the tables above |
| --- | --- | --- |
| **apodeixis** | a child project in eudaimonia — the build framework driven at a calculus nobody designed it around | its authors deliberately did not claim it here, on the ground that adding a line to somebody else's register is a person's edit to make. That restraint is the reason it looked free |

| **bouleusis** | βούλευσις, deliberation about particulars — considered for the actionable half and not used, since `martyria` covers it. Free, and the argument for it is in this repository's history |

**So the register is not the whole answer to *is this name free*.** It records
what has been claimed, and a name can be in use without being claimed. Look in
the trees as well, which costs one grep.

## If none of them fits## If none of them fits

Then the work is new, which is the interesting case. Pick a word for **what the
tool does to its subject** rather than for the subject — the register above is
mostly verbs of examination, because that is mostly what these tools do — and
write the etymology down before writing any code. If the sentence explaining the
name is hard to write, the scope is what is unclear, not the vocabulary.

Add the name here when you take it, with one line, and say where it lives.
**Where it lives is part of the entry rather than decoration.** A name that
starts as a child project and later graduates into a repository of its own keeps
its entry and changes that clause, and that is the only edit graduating asks of
this page. `init_eo from-child` reads the entry and is told to report the change
as owed rather than to make it — this file is in somebody else's tree, and a
new repository does not edit it.
