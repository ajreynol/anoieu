#!/usr/bin/env python3
"""Is the human supposed to be working right now?

**The end goal of this file is one sentence spoken to a person: take a break.**
Everything else here exists to make that sentence land at the right time and to
leave a trace when the window it rests on is moved.

**It decides nothing and enforces nothing.** The human can edit the schedule,
ignore the answer, or delete this file. What it can do is say what the window
is, say whether we are inside it, and record when the window last changed --
because a window widened at one in the morning is the interesting event, and an
unrecorded one is invisible.

**Never run this in CI.** It is a fact about a clock, not about a tree: it says
something different every hour, so a build hanging off it would fail for reasons
that have nothing to do with the code. It shares that property, and that rule,
with `tools/bump_check.py`.

Exit codes, so a shell can branch on it:

    0   awake   -- inside the window, and not on a declared break
    1   sleep   -- outside the window, or on a break inside it
    2   refused -- the schedule is not one this tool will report on

**A break and a night are the same event to everything downstream**, which is
why they share an exit code: both mean *not now*. They are told apart in what
gets said, because "take a break" and "you are on one" are different sentences
to be on the receiving end of.
"""

import datetime
import json
import os
import sys
import zoneinfo

#: ## How this file decides what time it is
#:
#: **The short version: `zoneinfo` from the standard library, an IANA name in
#: the schedule, and no dependency added.** The long version is here because
#: getting a local hour right is a well-known source of quiet wrongness, and a
#: tool whose entire job is to know the hour should show its work.
#:
#: **What we use.** `zoneinfo.ZoneInfo("Area/City")` is the standard library's
#: IANA timezone support, present since Python 3.9. This repository requires
#: 3.10, so it is always there and costs nothing to depend on. The schedule may
#: name a zone; when it does, that is authoritative, and it is the right place
#: for it because the human's timezone is a fact about the human and belongs
#: in the human's file.
#:
#: **What we fall back to.** With no zone named, `datetime.now()` returns the
#: naive local time of whatever process is running -- correct on a workstation,
#: and *silently wrong* anywhere the environment says UTC, which is most
#: containers and every CI runner. That is a second, independent reason this
#: file must never run in CI: it would not merely be useless there, it would be
#: confidently incorrect. Naming a zone removes the ambiguity entirely, which is
#: why the schedule offers the field.
#:
#: **Where the zone data comes from.** `zoneinfo` reads the operating system's
#: IANA database on Linux and macOS. Windows ships none, and the documented
#: remedy is the `tzdata` package from PyPI. **We do not add it.** A dependency
#: that exists to serve one optional field of one child project's advisory tool
#: is a bad trade in a repository that pins and audits what it fetches, so a
#: missing database degrades to system local time with the reason said out loud
#: rather than raising.
#:
#: **What we deliberately did not reach for.**
#:
#: - `pytz` -- superseded by `zoneinfo` for exactly this, and its `localize()`
#:   convention is a long-standing source of off-by-an-hour bugs. There is no
#:   reason to take on a dependency to get a worse interface.
#: - `arrow`, `pendulum`, `dateutil` -- convenience layers over what the two
#:   calls below already do. Nothing here needs parsing, arithmetic across
#:   zones, or humanised deltas.
#: - `datetime.utcnow()` -- deprecated since 3.12, and it returns a *naive*
#:   value that looks like local time and is not. It is named here so that
#:   nobody reintroduces it as a tidy-up.
#: - **Network time.** No NTP, no HTTP date header. It would make an offline,
#:   instant, unfailing check into a slow one that can fail, in exchange for
#:   accuracy nobody needs: being wrong by a second does not matter here, and
#:   being wrong by an hour is a timezone question rather than a clock one.
#:
#: **Daylight saving is handled by not handling it.** The window is wall-clock
#: local time, because "I work eight to six" is a claim about what a clock on a
#: wall says. Expressed that way it stays true across a DST change for free;
#: expressed in UTC it would drift by an hour twice a year and be wrong in the
#: direction of working longer.
#:
#: **And the honest limit: this measures a window, not work.** It knows what
#: hour it is and what hours were declared. It does not know whether the human
#: worked ten hours or twenty minutes inside them, or anything at all about
#: yesterday. **The ten-hour ceiling is therefore a bound on availability and
#: not on effort**, and the policy is casual on purpose because the measurement
#: to make it strict does not exist yet. Tracking usage would mean recording
#: what somebody did and when, which is a surveillance question this project
#: has not asked and should not answer by accident.

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEDULE = os.path.join(HERE, "schedule.json")

#: The ceiling, in hours, on a working window. **Not configurable, and that is
#: the point of it.** The human sets the window; this file sets the most the
#: window may be. A limit somebody can raise from inside the session it limits
#: is not a limit, it is a suggestion with extra steps.
#:
#: **Ten is provisional and is expected to be refined.** It was chosen by the
#: maintainer rather than derived from anything, which is recorded as a
#: shortcoming in `tools/zetesis/findings.md` rather than left implied. A
#: schedule that exceeds it is **refused outright** -- not clamped to it, not
#: warned about and honoured. Clamping would silently answer a question the
#: human asked, and this file does not have the standing to do that.
MAX_HOURS = 10

#: The window used when there is no schedule on disk. It is *at* the ceiling
#: rather than under it, which is worth noticing rather than smoothing over:
#: it means the recommended state is also the most work this tool will condone.
#: Argued, not settled, in `tools/zetesis/findings.md`.
DEFAULT = {"from": "08:00", "to": "18:00"}

#: Breaks are windows *inside* the working window, declared the same way and
#: read the same way. There are none by default: a break somebody did not ask
#: for is an interruption, and this file is not in the business of those.
NO_BREAKS: list[dict] = []


def now_local(zone: str | None = None) -> datetime.datetime:
    """The current local time, in the human's zone if they named one.

    Never raises: an unknown or unavailable zone falls back to system local
    time, because a schedule with a typo in it should still get the human an
    approximately right answer rather than a traceback.
    """
    if zone:
        try:
            return datetime.datetime.now(zoneinfo.ZoneInfo(zone))
        except (zoneinfo.ZoneInfoNotFoundError, ValueError, OSError):
            pass
    return datetime.datetime.now()


#: The greeting is chosen by the hour and not by the word *wake*. Waking at
#: seven in the evening is a real thing that happens to a human whose window
#: is an evening window, and being told *good morning* then is the tell that a
#: mechanism is reciting rather than reading.
GREETINGS = ((12, "Good morning"), (18, "Good afternoon"), (24, "Good evening"))


def greeting(now: datetime.datetime | None = None, zone: str | None = None) -> str:
    """*Good morning*, *Good afternoon* or *Good evening*, per the local hour."""
    hour = (now or now_local(zone)).hour
    return next(word for edge, word in GREETINGS if hour < edge)


def _minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def load(path: str = SCHEDULE) -> dict:
    """The schedule, or the default if there is none. Never raises."""
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, ValueError):
        return {"available": dict(DEFAULT), "breaks": list(NO_BREAKS),
                "set_on": None, "source": "default"}
    win = raw.get("available") or {}
    if not win.get("from") or not win.get("to"):
        return {"available": dict(DEFAULT), "breaks": list(NO_BREAKS),
                "set_on": None, "source": "default"}
    breaks = [b for b in raw.get("breaks") or NO_BREAKS
              if b.get("from") and b.get("to")]
    return {"available": win, "breaks": breaks, "set_on": raw.get("set_on"),
            "human": raw.get("human"), "timezone": raw.get("timezone"),
            "source": "schedule.json"}


def span(win: dict) -> int:
    """The window's length in minutes, wrapping midnight if it has to.

    A window that wraps is a night shift and is allowed. A window that starts
    and ends at the same minute is twenty-four hours, not zero -- read the other
    way it would make an empty schedule mean *always working*, which is the
    failure this whole file exists against.
    """
    a, b = _minutes(win["from"]), _minutes(win["to"])
    return (b - a) % (24 * 60) or 24 * 60


def refuse(win: dict) -> str | None:
    """Why this schedule will not be reported on, or None if it is fine."""
    try:
        hours = span(win) / 60
    except (ValueError, KeyError):
        return "the window is not two times of the form HH:MM"
    if hours > MAX_HOURS:
        return (f"the window is {hours:g} hours and the ceiling is {MAX_HOURS}"
                f" -- set a window of {MAX_HOURS} hours or less")
    return None


def state(now: datetime.datetime | None = None, path: str = SCHEDULE) -> dict:
    """Where we are: `awake`, `sleep`, `break` or `refused`, and why.

    **Only `awake` means work.** The other three are one answer downstream --
    *not now* -- and callers should test for `awake` rather than against
    `sleep`. A refused schedule in particular fails **closed**: an unusable
    schedule leaves the ecosystem asleep until somebody fixes it, because the
    alternative is that writing an invalid window is the way to get an
    unlimited one.
    """
    sched = load(path)
    win = sched["available"]
    bad = refuse(win)
    if bad:
        return dict(sched, status="refused", reason=bad)

    now = now or now_local(sched.get("timezone"))
    t = now.hour * 60 + now.minute

    def holds(w):
        a, b = _minutes(w["from"]), _minutes(w["to"])
        return (a <= t < b) if a < b else (t >= a or t < b)

    stamp = now.strftime("%H:%M")
    if not holds(win):
        return dict(sched, status="sleep", now=stamp,
                    reason=f"{stamp} is outside {win['from']}-{win['to']}")
    for br in sched.get("breaks") or []:
        if holds(br):
            return dict(sched, status="break", now=stamp,
                        reason=f"{stamp} is inside the break "
                               f"{br['from']}-{br['to']}")
    return dict(sched, status="awake", now=stamp,
                reason=f"{stamp} is inside {win['from']}-{win['to']}")


def moved_during_sleep(s: dict) -> bool:
    """Was the window last changed on a day we are currently outside of?

    **The weakest useful signal, and deliberately weak.** It cannot see the hour
    a file was edited, only the date the schedule claims it was set. What it
    catches is the shape of the thing: a window recorded as set today, read
    while outside that window, is a window that may have been widened by the
    person it was meant to bind. Saying so is the whole intervention.
    """
    if s["status"] == "awake" or not s.get("set_on"):
        return False
    return s["set_on"] == datetime.date.today().isoformat()


def summary(s: dict) -> str:
    """One line, for a health table. Short enough to sit in a column."""
    if s["status"] == "refused":
        return "schedule refused"
    win = s["available"]
    return f"{s['status']} -- {s.get('now', '')} of {win['from']}-{win['to']}"


#: Every break the human declares is time this tool will not ask them to work,
#: and it is read from their file rather than proposed from here. The asymmetry
#: is deliberate: this file may say *stop* and may never say *start*.


def main(argv: list[str]) -> int:
    s = state()
    if "--health" in argv:
        print(summary(s))
        return 0

    print(f"schedule: {s['available']['from']}-{s['available']['to']}"
          f"  ({span(s['available']) / 60:g}h, ceiling {MAX_HOURS}h)"
          f"  from {s['source']}")
    if s["status"] == "refused":
        print(f"refused:  {s['reason']}")
        return 2
    print(f"now:      {s['reason']}")
    if s["status"] in ("sleep", "break"):
        print()
        # On the off chance somebody reads this far and wonders what a working
        # day is doing inside a static analyzer: in clinical use, *eunoia* names
        # a state of normal mental health. The ecosystem is named after it. So
        # this file is, strictly speaking, the only one here on topic.
        if s["status"] == "break":
            print("  You are on a break you declared. It is still on.")
        else:
            print("  Take a break. You are outside the window you set.")
        if moved_during_sleep(s):
            print("  This window was recorded as set today, and it is being read")
            print("  from outside it. If it was widened tonight, that is the")
            print("  thing it existed to stop.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
