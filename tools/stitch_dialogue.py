"""Stitch an episode whose characters speak in the video clips themselves (no narration).

Usage:
    python tools/stitch_dialogue.py series/<slug>/episodes/EP01 [--scene SC02] [--hold 3.0] [--lead 0.3] [--tail 0.45]

Per shot (sorted by SCnn_SHnn name) the script uses:
    <episode>/talk/<shot>.mp4   a clip where a character speaks (preferred)
    <episode>/clips/<shot>.mp4  otherwise a silent/ambient clip (first --hold seconds are used)

Talking clips are trimmed to the speech: from --lead seconds before the first word to --tail seconds after the last
word (found with ffmpeg silencedetect), so each shot lasts as long as its line. Everything is scaled to 1920x1080 at
24 fps, loudness-normalised, and joined into <episode>/final/<EPnn>.mp4. Requires ffmpeg and ffprobe on PATH.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def duration(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
              capture_output=True, text=True).stdout.strip()
    return float(out)


def has_audio(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type",
               "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    return bool(out)


def speech_span(path, total):
    """Return (start, end) of audible speech in seconds, or None if there is none."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "silencedetect=noise=-36dB:d=0.25",
                        "-vn", "-f", "null", "-"], capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    start = 0.0
    if starts and starts[0] <= 0.05 and ends:
        start = ends[0]
    end = total
    if starts and (len(starts) > len(ends) or (ends and (starts[-1] > ends[-1] or abs(ends[-1] - total) < 0.1))):
        end = starts[-1]
    if end - start < 0.3:
        return None
    return start, end


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--hold", type=float, default=3.0)
    ap.add_argument("--lead", type=float, default=0.3)
    ap.add_argument("--tail", type=float, default=0.45)
    ap.add_argument("--scene", help="only stitch one scene, e.g. SC02 (writes final/EPnn_SC02.mp4)")
    args = ap.parse_args()

    ep = Path(args.episode)
    names = sorted({p.stem for p in list((ep / "clips").glob("SC*_SH*.mp4")) + list((ep / "talk").glob("SC*_SH*.mp4"))})
    if args.scene:
        names = [n for n in names if n.startswith(args.scene + "_")]
    if not names:
        sys.exit("No clips found")

    work = Path(tempfile.mkdtemp())
    parts = []
    for name in names:
        talk = ep / "talk" / f"{name}.mp4"
        if talk.exists():
            total = duration(talk)
            span = speech_span(talk, total)
            if span:
                ss = max(0.0, span[0] - args.lead)
                to = min(total, span[1] + args.tail)
            else:
                ss, to = 0.0, min(total, args.hold)
            src, kind = talk, f"talk {span[0]:.2f}-{span[1]:.2f}s" if span else "talk (no speech found)"
        else:
            src = ep / "clips" / f"{name}.mp4"
            ss, to, kind = 0.0, min(duration(src), args.hold), "ambient"
        length = to - ss
        out = work / f"{name}.mp4"
        vf = "fps=24,scale=1920:1080:flags=lanczos,setsar=1"
        af = f"atrim={ss:.3f}:{to:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={max(0, length - 0.08):.3f}:d=0.08,aresample=44100"
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", str(src)]
        if has_audio(src):
            cmd += ["-filter_complex", f"[0:v]trim={ss:.3f}:{to:.3f},setpts=PTS-STARTPTS,{vf}[v];[0:a]{af},pan=stereo|c0=c0|c1=c0[a]"]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex",
                    f"[0:v]trim={ss:.3f}:{to:.3f},setpts=PTS-STARTPTS,{vf}[v]", "-map", "[v]", "-map", "1:a",
                    "-t", f"{length:.3f}"]
        if has_audio(src):
            cmd += ["-map", "[v]", "-map", "[a]"]
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-ar", "44100", "-ac", "2", str(out)]
        run(cmd)
        parts.append(out)
        print(f"{name}: {kind} -> {length:.2f}s")

    listing = work / "list.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts))
    joined = work / "joined.mp4"
    run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(joined)])
    final_dir = ep / "final"
    final_dir.mkdir(exist_ok=True)
    final = final_dir / (f"{ep.name}_{args.scene}.mp4" if args.scene else f"{ep.name}.mp4")
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(joined), "-c:v", "copy",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-ar", "44100", str(final)])
    print(f"Wrote {final} ({duration(final):.1f}s)")


if __name__ == "__main__":
    main()
