"""Stitch an episode: join shot clips in order, lay dialogue audio over them.

Usage:
    python tools/stitch_episode.py series/<slug>/episodes/EP01

Expects:
    <episode>/clips/SCnn_SHnn.mp4   shot clips (sorted by filename = playback order)
    <episode>/audio/SCnn_SHnn.mp3   optional per-shot dialogue audio (same stem as its clip)
    <episode>/music.mp3             optional background music (mixed low)
Writes:
    <episode>/final/<EPnn>.mp4

Requires ffmpeg on PATH.
"""
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd):
    subprocess.run(cmd, check=True)


def main(episode_dir):
    ep = Path(episode_dir)
    clips = sorted((ep / "clips").glob("*.mp4"))
    if not clips:
        sys.exit(f"No clips found in {ep / 'clips'}")

    work = Path(tempfile.mkdtemp())
    muxed = []
    for clip in clips:
        audio = ep / "audio" / f"{clip.stem}.mp3"
        out = work / clip.name
        if audio.exists():
            # Replace the clip's audio with the dialogue; pad/trim audio to the clip's length.
            run(["ffmpeg", "-y", "-i", str(clip), "-i", str(audio),
                 "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-c:a", "aac",
                 "-af", "apad", "-shortest", str(out)])
        else:
            run(["ffmpeg", "-y", "-i", str(clip), "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                 "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-c:a", "aac",
                 "-shortest", str(out)])
        muxed.append(out)

    listing = work / "list.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in muxed))

    final_dir = ep / "final"
    final_dir.mkdir(exist_ok=True)
    final = final_dir / f"{ep.name}.mp4"
    joined = work / "joined.mp4"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
         "-c:v", "libx264", "-c:a", "aac", str(joined)])

    music = ep / "music.mp3"
    if music.exists():
        run(["ffmpeg", "-y", "-i", str(joined), "-stream_loop", "-1", "-i", str(music),
             "-filter_complex", "[1:a]volume=0.15[m];[0:a][m]amix=inputs=2:duration=first[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", str(final)])
    else:
        joined.replace(final)
    print(f"Wrote {final}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
