"""Pick a clip duration for each spoken line so no sentence is cut off.

Usage:
    python tools/plan_durations.py "Line one." "Line two." ...
    python tools/plan_durations.py --file scene.txt          (one line of dialogue per row)
    python tools/plan_durations.py --available 4,6,8,10 ...

Rule: estimated speaking time = words / 2.3 + 0.9 seconds (breathing room before and after the line);
the clip length is the smallest available duration >= the estimate.
"""
import argparse
import math
import re
import sys


def estimate(line):
    words = len(re.findall(r"[A-Za-z0-9']+", line))
    return words, words / 2.3 + 0.9


def pick(seconds, available):
    for a in sorted(available):
        if a >= seconds:
            return a
    return max(available)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lines", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--available", default="4,6,8,10")
    args = ap.parse_args()
    lines = list(args.lines)
    if args.file:
        lines += [l.strip() for l in open(args.file, encoding="utf-8") if l.strip()]
    if not lines:
        sys.exit(__doc__)
    avail = [int(x) for x in args.available.split(",")]
    total = 0
    for i, line in enumerate(lines, 1):
        words, secs = estimate(line)
        d = pick(secs, avail)
        total += d
        note = "  (long line: consider splitting)" if words > 17 else ""
        print(f"{i:2d}. {words:2d} words ~{secs:4.1f}s -> {d}s clip  {line[:60]}{note}")
    print(f"Total clip time: {total}s")


if __name__ == "__main__":
    main()
