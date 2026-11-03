---
name: micro-drama
description: Turn a story (cast + framework) into a micro drama series where the characters themselves speak in conversational, culturally authentic dialogue. Plans every episode and scene, builds character/environment sheets, then (one episode at a time, on request) generates a wide establishing shot plus medium and close-up coverage for each scene, animates each line into a lip-synced clip with the user's own image and video models, and stitches the episode. Use when the user gives a story and wants a movie-style, dialogue-driven short video series.
---

# Micro Drama Skill

Movie-style episodes: characters talk to each other in the video itself (lip-synced speech from an image-to-video model). **No narrator, no separate voiceover.** The user brings their own image and image-to-video providers/keys; this skill never ships or stores keys.

Working folder = where the user opened the agent. Create if missing: `queue.md`, `story/`, `config/`, `series/`, and copy `templates/` and `tools/` from this skill. Read `references/dialogue-coverage.md` before planning any scene; it holds the rules summarised below.

## Step 0: Provider setup (first run only)

Read `config/providers.md` (create from `config/providers.example.md`). Needed: **image generation with reference-image input**, and **image-to-video that speaks dialogue written in the prompt with lip sync** (e.g. Google Flow Veo/Omni, other video models with native audio). Ask which services and which env var holds each key (never ask for keys in chat). Write small adapters (`tools/adapters/README.md`), or drive the provider's web UI if the user prefers a browser tool. Test with one cheap call, confirm cost with the user, and record the choices (default aspect ratio **16:9**).

## Step 1: Queue and PLAN (automatic)

Save the story as `story/<slug>.md`, add it to `queue.md`, and plan the whole series without stopping, using `templates/`:

1. `series/<slug>/bible.md`: logline, genre, tone, visual style, aspect ratio, episode length, plot arc, ending, cultural/language notes (who speaks which register).
2. `characters/<name>.md`: fixed identity prompt, wardrobe table, voice description (accent, pitch, pace, age) reused verbatim in every video prompt; plus a multi-angle sheet image.
3. `environments/<name>.md`: fixed location prompt + sheet image.
4. `episodes/EPnn/episode.md` and one `scenes/SCnn.md` per scene.

**Each scene is a real conversation**: 6-10 lines, back and forth, written the way those people actually talk (see the register guide in `references/dialogue-coverage.md`: Nigerian parents, rich vs poor, classy/young slang, village speakers, pidgin where natural). Keep each line to roughly 8-16 words. Non-speaking beats are short silent shots (about 3 s), never narration.

Each scene file also holds its **shot plan** (coverage) and the **per-line duration** chosen with `tools/plan_durations.py`.

Planning ends with a summary and the question of which episode to produce.

## Step 2: PRODUCE EPISODE (only when the user names one)

State counts and credit estimate (images, clips and the chosen duration of each clip); wait for a yes. Then, **scene by scene, in order**:

1. **Establishing shot first.** One wide shot containing every speaking character in their positions in the location (references: the character images + the environment image).
2. **Coverage from the establishing shot.** For each speaker generate a **medium shot** and a **close-up**, each using the establishing image as a reference so positions, room and lighting match (speaker looks toward where the other character sits; eyelines stay consistent). In a 3-person scene do this for all three. A medium two-shot may be added for context.
3. **One clip per line.** Animate the image that fits the line, always cutting to the speaker: alternate medium and close-up angles for the same person over the scene, reuse images freely, and use the wide shot for entrances, exits and group beats. Put the line in the video prompt verbatim with the character's voice description and "lips move in sync with the words". A silent 3 s hold on the establishing shot opens the scene when useful.
4. **Duration per clip is chosen from the line length** (see Duration rule). Never leave a line to be cut off.
5. Download clips into `episodes/EPnn/talk/SCnn_SHnn.mp4` (speaking) and `episodes/EPnn/clips/` (silent inserts); images in `episodes/EPnn/coverage/`.
6. **Stitch:** `python tools/stitch_dialogue.py series/<slug>/episodes/EPnn [--scene SC02]`. It trims each speaking clip to where the speech starts and ends, normalises loudness, and joins everything into `final/EPnn.mp4` (1920x1080).
7. Check for failures (e.g. content-filter rejections on a still): regenerate only that shot, or fall back to a slow push-in on the still with ffmpeg. Update `episode.md` and `queue.md`; ask whether to continue.

## Duration rule (important)

Estimate how long the spoken line takes and pick the clip length that fits it, **with headroom**, so no sentence is cut off:

`seconds = words / 2.3 + 0.9`, then choose the smallest available duration >= that (typically 4, 6, 8 or 10 s). Run `python tools/plan_durations.py "line one" "line two" ...` to get the table. Examples: 7 words -> 4 s; 12 words -> 8 s; 17 words -> 10 s. Prefer splitting a very long line (over about 17 words) into two shots of two speakers or two angles. Add to every dialogue prompt: "the character finishes the whole sentence, then stops speaking and holds a natural pause". Check the generated clip: if the speech runs to the very last frame, regenerate that line with the next duration up.

## Rules

- Never produce an episode the user hasn't named. Never skip ahead.
- Keys only as env var names. Never write keys anywhere.
- Characters speak; no narrator. Dialogue must be conversational and culturally true to each speaker.
- Paste identity, wardrobe and voice descriptions verbatim; keep faces consistent by always attaching the character image and the scene's establishing image.
- Generate the establishing shot before the close-ups, every scene.
- Save everything with the naming above so any agent can resume from files alone.
