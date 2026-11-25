#!/usr/bin/env python3
"""Two Lines to Your Past Self — make.fun entry (program/v1).

Writes exactly two lines to /output/entry.txt:
  line 1 — a warning to the writer's past self about one specific moment,
           in a single sentence;
  line 2 — one sentence on why that moment mattered and what changed
           because of it.

Gate: /output/entry.txt must be UTF-8 text of 1-280 characters.
This entry is 214 characters (including the newline between the lines
and the trailing newline), two lines, one sentence each.
"""

import os
import stat

LINES = [
    "Don't say yes to the overtime shift at the warehouse on Christmas Eve 2019.",
    "Because missing your daughter's first Christmas taught you that no paycheck replaces a moment, and you have never worked a holiday since.",
]

TEXT = "\n".join(LINES) + "\n"


def validate(text: str) -> None:
    """Gate self-check: fail loudly (non-zero exit) if the output text
    would fail the competition gate — exactly 2 lines, each exactly one
    sentence, total 1-280 chars, UTF-8, not whitespace-only."""
    problems = []
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("output is not valid UTF-8")
    if not (1 <= len(text) <= 280):
        problems.append(f"output is {len(text)} chars, must be 1-280")
    if not text.strip():
        problems.append("output is whitespace-only")
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 2:
        problems.append(f"output has {len(lines)} lines, must be exactly 2")
    for i, line in enumerate(lines, 1):
        terminators = sum(line.count(c) for c in ".!?")
        if terminators != 1 or not line.rstrip().endswith((".", "!", "?")):
            problems.append(f"line {i} is not exactly one sentence: {line!r}")
    if problems:
        raise SystemExit("GATE SELF-CHECK FAILED: " + "; ".join(problems))


def main() -> None:
    validate(TEXT)
    os.umask(0o022)
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.txt"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEXT)
    # The grader collects outputs as another user: leave the file
    # readable by everyone (0644), not just its owner.
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
