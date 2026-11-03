# Dialogue and coverage guide

The preferred style of this system: a movie, not a slideshow. Every scene is a conversation, shot the way a director covers it.

## 1. Scene structure

1. **Establishing wide shot** with all speakers visible in position (e.g. she sits left, he sits right, table between them). It fixes who is where.
2. **Coverage per speaker**, each generated *with the establishing shot attached as a reference*:
   - a **medium shot** of that character (same side of the frame, looking toward the other character),
   - a **close-up** of that character (same eyeline).
   For three speakers, repeat for each. Optionally add a medium two-shot.
3. **Cut to whoever is speaking.** For one character, alternate medium and close-up on different lines; use the wide shot for entrances, exits and group beats. Reuse images as many times as needed.
4. Next scene = new establishing shot, new coverage. Never reuse another scene's room.

Prompt checklist for coverage images: "same room, positions and lighting as the establishing shot", "turned toward <other character> off-screen on the <left/right>", the character's identity and outfit, framing (medium / tight close-up), style line.

## 2. Writing the dialogue

- 6-10 lines per scene, genuinely back and forth: questions, interruptions, reactions, pushback, a turn at the end. Not announcements.
- 8-16 words per line. Short reactions ("Ehen?", "A jet?") are good.
- Make people sound like who they are. Nigerian examples:
  - **Wealthy parents:** measured, formal English, proverbs, "my son", "Ikenna", titles, quiet authority.
  - **Poor / village parents:** warmer, more direct, Igbo or Yoruba phrasing in English, pidgin ("wetin", "dey", "na", "abeg"), blessings, scolding, "you hear me?".
  - **Young classy Lagos people:** current slang, "babe", "abeg", "sha", "my guy", fast and casual, brand and money talk.
  - **Local/village youth and workers:** pidgin-leaning English, banter, "o", "na", "wahala".
  - **Elders / chiefs:** slower, proverbs, "ehen", "my child".
  Adapt the same idea to other cultures: match region, class, age and relationship.
- Say it as it sounds: write numbers and abbreviations out; avoid tongue-twisters; avoid emojis.

## 3. Voice descriptions (reused every clip)

One sentence per character, e.g. "deep, calm, classy Nigerian-accented male voice". Put it in each video prompt so the voice stays as consistent as the model allows.

## 4. Video prompt template (one line per clip)

`<who, as in the image> says in a <voice description>: "<exact line>" Their lips move naturally in sync with the words, <small action/expression>. They finish the whole sentence, then stop speaking and hold a natural pause. The camera holds this framing with subtle natural movement. <ambience>. No music, no subtitles.`

## 5. Duration

`seconds = words / 2.3 + 0.9`, pick the smallest available clip length >= that (4, 6, 8, 10). `tools/plan_durations.py` does the math. If a generated clip's speech runs to the last frame, redo it one step longer. The stitcher trims silence after the last word.

## 6. Failures

Image-to-video filters sometimes reject stills (revealing clothes, children in the background). Retry with the other angle, or fall back to a slow push-in made with ffmpeg and keep the line as a silent shot or move the line to another shot.
