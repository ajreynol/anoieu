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
convention, and a name whose explanation is a stretch means the scope has not
been decided yet.

Descriptive non-Greek names are allowed where the thing is a program rather than
an account — `anoieu_fuzz` is one — but the burden is on the name to earn it.

## Taken

| name | what it is |
| --- | --- |
| **eunoia** | the language itself — εὔνοια, *good thinking* |
| **ethos** | the proof checker |
| **logos** | the Lean development |
| **eudaimonia** | the calculus template |
| **anoieu** | the analyzer; *eunoia* read backwards |
| **dokimasia** | δοκιμασία, the scrutiny before office: what no proof step covers |
| **sapheneia** | σαφήνεια, clarity of an account: Eunoia as a language definition |
| **ynoia** | *why Eunoia*: whether the arrangement earns its machinery |
| **euthyna** | εὔθυνα, the audit at end of term: what logos's proof is made of. **Started**, in eudaimonia |
| **koine** | κοινή, *the common tongue* — the shared dialect that let people who spoke differently understand each other. The shared machinery of the reporting loop, so the protocol has one implementation rather than one per member. **Approved**, awaiting its repository; see [`proposals.md`](proposals.md) `P1` |

## Reserved, and free to take

Each was named in [`why-eunoia.md`](why-eunoia.md) because some argument there is
stated relative to its absence. None has a repository or a line of code.

| name | Greek | what it would be |
| --- | --- | --- |
| **pathos** | πάθος, the third mode of persuasion | an efficient *verified* proof checker — the one that would let the ecosystem ship what it proves rather than a second implementation |
| **hermeneia** | ἑρμηνεία, interpretation | carrying the embedded semantics into Lean's own logic, so a theorem about a proof becomes a theorem about the thing proved |
| **noesis** | νόησις, the act of understanding | the semantics and the compiler defined *in* Lean rather than compiled into it |
| **iogos** | logos, elsewhere | the same calculus and development redone in a second proof assistant, as an independence check |
| **elenchos** | ἔλεγχος, cross-examination | differential fuzzing derived from the calculus rather than written by hand — what the fuzzer here is a deliberate baseline for |

## If none of them fits

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
