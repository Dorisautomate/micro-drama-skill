"""Pick a clip duration for each spoken line so no sentence is cut off, and flag repeated words.

Usage:
    python tools/plan_durations.py "Line one." "Line two." ...
    python tools/plan_durations.py --file scene.txt          (one line of dialogue per row)
    python tools/plan_durations.py --available 4,6,8,10 --wps 1.7 --pad 1.0 ...

Rule (v2, from real results: the video model speaks with expression, about 1.7 words per second):
    estimated speaking time = words / 1.7 + 1.0 seconds (one second of breathing room)
    clip length = smallest available duration >= the estimate.
If a generated clip still has speech running to its last frame, redo that line one step longer (up to 10 s).
Lines over about 17 words should be split between speakers or shots.

Also warns when a content word repeats inside one line (the model tends to say repeated words twice).
"""
import argparse
import re
import sys
from collections import Counter

STOP = {"the", "a", "an", "and", "or", "to", "of", "in", "on", "i", "you", "he", "she", "it", "we", "is", "am", "are",
        "my", "me", "your", "his", "her", "for", "with", "that", "this", "but", "not", "do", "does", "so", "at", "be"}


def words_of(line):
    return re.findall(r"[A-Za-z0-9']+", line)


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
    ap.add_argument("--wps", type=float, default=1.7)
    ap.add_argument("--pad", type=float, default=1.0)
    args = ap.parse_args()
    lines = list(args.lines)
    if args.file:
        lines += [l.strip() for l in open(args.file, encoding="utf-8") if l.strip()]
    if not lines:
        sys.exit(__doc__)
    avail = [int(x) for x in args.available.split(",")]
    total = 0
    for i, line in enumerate(lines, 1):
        ws = words_of(line)
        secs = len(ws) / args.wps + args.pad
        d = pick(secs, avail)
        total += d
        notes = []
        if len(ws) > 17:
            notes.append("long: split")
        rep = [w for w, c in Counter(x.lower() for x in ws).items() if c > 1 and w not in STOP]
        if rep:
            notes.append("repeats: " + ",".join(rep))
        print(f"{i:2d}. {len(ws):2d} words ~{secs:4.1f}s -> {d:2d}s  {line[:58]}  {'; '.join(notes)}")
    print(f"Total clip time: {total}s")


if __name__ == "__main__":
    main()
