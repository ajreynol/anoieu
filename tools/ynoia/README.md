# ynoia

*The name is **"why Eunoia"**, elided. It keeps the root and drops the
judgement: εὔνοια is εὖ + νοῦς, **good thinking** — and this project removes the
εὖ and asks whether the thinking is good. That is a claim somebody can disagree
with: if the arrangement is obviously right and the question idle, the name is
wrong and so is the project. It also follows the sibling convention — [anoieu](../../README.md) is
Eunoia read backwards, and this is Eunoia read as a question.*

A child project under [`docs/policy.md`](../../docs/policy.md). Started by a
human, read-only, unadvertised, and not part of what this repository ships.
Deleting this directory changes nothing anywhere else.

## The question

**Does the Eunoia ecosystem's arrangement earn its machinery — and what is it
missing?**

An SMT solver has found an answer and is asked to justify it. It can emit a Lean
proof and have Lean check it, or it can emit a proof in a fixed calculus written
in a small language, have a checker check that, and *also* compile the calculus
into a Lean development that says its rules are sound. The ecosystem chose the
second. It is more machinery, and the case for it has been made in conversation
and never written down where somebody could attack it.

So: write it down, make the strongest case against it, and see which survives.

## Goals, in order

1. **The argument, both directions.** The case for the calculus, the case for
   doing it in Lean instead, the general objections to each, and six coherent
   ways the ecosystem could be arranged — stated so that somebody who disagrees
   has something to disagree *with*. [`why-eunoia.md`](why-eunoia.md).

2. **The tools that do not exist.** Every argument above is stated relative to
   what exists today, so the cheapest way to see which arguments are about the
   *arrangement* and which are merely about its *current state* is to name the
   work that would move each one. Some of those names have since been taken up
   as real projects, which is the closest thing this project has to a result.

3. **The names.** Naming work that does not exist is most of what goal 2
   produces, so the register lives on its own page: what each reserved name was
   reserved *for*, which are taken, and how to choose one that is not there.
   [`names.md`](names.md). It is the page a brand new repository is pointed at,
   and it is deliberately short — a repository choosing its name should not have
   to read an argument about the ecosystem first.

4. **Auditing proposals.** Whether a given idea deserves a repository of its
   own is the account's general question applied to one case, with a decision
   attached — so it is answered here, against a stated standard, in
   [`proposals.md`](proposals.md). Most wants are not that question, and the
   ones that are work rather than repositories are tracked in
   [`requests.md`](requests.md) with an argument about whose tree they belong
   in. The output is an argument with a
   recommendation at the end. **It approves nothing:** a repository is a claim
   on a shared namespace and on years of somebody's attention, and the policy
   reserves that for a person. anoieu carries proposals in, because it is the
   only tool that may address a child project directly.

5. **Stretch: what would settle it.** An argument that cannot be lost is not
   worth having. The account carries what would change our minds and one
   experiment that would settle more than any further argument. Turning that into
   something somebody could actually run is the stretch goal, and it remains one.

## What this project does not do

The boundary matters more than the goals, so it is stated first.

- **It does not decide anything.** Nobody here has the authority to rearrange an
  ecosystem, and an account that reads as a decision has overstepped. The
  arrangements it describes are options laid out fairly, not a recommendation
  with the alternatives listed for form's sake.
- **It does not report defects.** Where reading the ecosystem turned up something
  actually wrong in somebody's file, that is a finding: it leaves through
  [`reporting-workflow.md`](../../docs/reports/reporting-workflow.md) with an id and a
  state, and never through here. This project's output is argument.
- **It does not speak for anoieu.** The host tool is a participant in the
  argument and an interested one — it exists because the narrow-fragment position
  is right — and the account says so rather than pretending to neutrality it
  does not have.
- **It does not commit anybody to the tools it names.** A named project with a
  paragraph attached is a description of work that would change an argument, not
  a roadmap, not an assignment, and not a claim that anybody intends to build it.
- **It does not describe the language.** What Eunoia *is*, independently of any
  checker, is a different question with a different child project.

## Status

**Now also the place proposals are audited**, which is the first thing this
project has been asked to produce for somebody else rather than for itself. Its
first audit, `P1`, was carried to a decision and a repository was approved on the
strength of it — which is a deliverable in the sense the vision means, and would
be the thing that earns this project a place there. Whether it has is not this
project's call.

**The account exists and is long.** Nothing in it has been argued with by
anybody who disagrees, which is the whole point of writing it and has not
happened yet. It has produced no deliverable and so has earned no place in
[`docs/vision.md`](../../docs/vision.md) — with one qualification: of the six projects it named, **euthyna** has since been started
as a child project of eudaimonia, and the register in
[`names.md`](names.md) is now consulted by `scripts/prompts/init_eo` when a new
repository picks a name. Whether that is this account's doing or
convergence is not something this project can establish about itself.

## Layout

| file | what it is |
| --- | --- |
| [`why-eunoia.md`](why-eunoia.md) | the account: the case, the case against, the objections, six arrangements, the projects that do not exist, and what would change our minds |
| [`names.md`](names.md) | the register of names: taken, reserved, and how to pick one. Goal 3 |
| [`proposals.md`](proposals.md) | should this become a repository? The standard, and one section per proposal. Goal 4 |
