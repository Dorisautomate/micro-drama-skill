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

## 7. Premium visual style (preferred look)

Modeled on popular AI drama channels (Mede Tales, Tales with Toria): polished, glossy, high-fashion. Use it in every character sheet, environment and shot prompt.
- Cast: very attractive, model-like actors, flawless radiant skin, sculpted features, groomed beards, styled hair, full glam makeup. Even "poor" characters look clean, stylish and fit (fitted tank tops, coveralls tied at the waist, tidy caps).
- Wardrobe: tailored three-piece suits and tuxedos, couture dresses, rich lace and agbada with gold embroidery, gold jewellery, designer bags.
- Sets: luxury interiors (marble, gold accents, chandeliers, floor-to-ceiling windows with a city skyline), vibrant clean villages with colourful houses and palm trees at golden hour.
- Light/colour: soft warm golden light with glow, rich saturated grading, razor-sharp 4K, shallow depth of field.

Style line to append to image prompts: "Premium glossy cinematic AI-drama look like top Nigerian romance series on YouTube: very attractive, model-like actors with flawless radiant skin, sculpted features and styled hair, high-fashion modern wardrobe with designer accessories, soft warm golden lighting with glowing highlights, luxurious polished sets, vibrant rich colour grading, razor-sharp 4K, shallow depth of field."

## 8. Practical notes

- Give every generated reference image a unique clean name right after it is made (for example `V2_SC01_E1`) so later steps can attach it by exact name; auto-generated titles repeat.
- Generate and verify the character and environment sheets first, then each scene's establishing shot, then coverage.
- Some video filters reject a close-up as "prominent people" or a still as revealing; retry with the medium shot of the same character.
