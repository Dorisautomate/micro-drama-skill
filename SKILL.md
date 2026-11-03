---
name: micro-drama
description: Turn a story (cast + framework) into a narrated, AI-generated micro drama series. Plans every episode, scene, character sheet, environment and shot, then (one episode at a time, on request) generates shot images, animates them into clips with the user's own video API, adds short voiceover lines, and stitches each episode. Use when the user gives a story and wants a micro drama, soap-opera-style short video series, or narrated AI video episodes.
---

# Micro Drama Skill

Narrated micro dramas: short vertical episodes made of AI-generated still images, animated into clips, each carrying one short voiceover line (narrator or character), stitched into a finished episode. The **user brings their own image, video and voice API keys**; this skill never ships or stores keys.

Working folder = wherever the user opened the agent. Create these next to this skill if missing: `queue.md`, `story/`, `config/`, `series/`. Copy `templates/`, `tools/` and `queue.md` from this skill folder when starting.

## Step 0: Provider setup (first run only)

Read `config/providers.md` (create from `config/providers.example.md` if absent). If any of image / video / voice is blank, run setup before anything else:

1. Ask the user, for each capability, **which service/model they use** and **the name of the environment variable holding their key** (never ask them to paste a key into chat or a file; if they paste one, tell them to put it in an env var / `.env` and don't repeat it).
   - Image generation (text-to-image; ideally with reference-image input for consistency)
   - Image-to-video (animating a still)
   - Voice / text-to-speech
   - Music (optional)
2. Ask them for the provider's API docs link or an example `curl`, or use the docs if you can fetch them. Then write a tiny adapter in `tools/adapters/` for each one, following `tools/adapters/README.md` (a CLI that takes a prompt/inputs and writes a file). Test each adapter with **one** cheap call, and confirm with the user before spending.
3. Record choices (provider, model, env var name, max clip seconds, aspect ratio, voice ids) in `config/providers.md`.

Only after all three required adapters work, proceed.

## Step 1: Queue and PLAN (automatic)

When the user supplies a story (file in `story/` or pasted into chat; save pasted stories as `story/<slug>.md` using `story/story-template.md`), add it to `queue.md` and plan the **entire series** without stopping for approval between steps. Ask only if a blocker is missing (cast, genre, ending).

Create under `series/<slug>/`:

1. `bible.md`: logline, genre, tone, themes, visual style, aspect ratio (default 9:16), episode length (default 45–90 s), narrator persona, full plot arc, ending.
2. `characters/<name>.md` per `templates/character-sheet.md`: fixed **identity prompt** (reused verbatim in every shot) and a **multi-angle camera sheet** (front, 3/4 L, 3/4 R, profile, back, close-up, full body, key expressions). Assign each speaking character a voice.
3. `environments/<name>.md` per `templates/environment-sheet.md`: fixed **location prompt** and multi-angle sheet. Every environment that appears in the series gets one.
4. `episodes/EPnn/episode.md` per `templates/episode.md`: soap-opera structure; hook, escalation, cliffhanger, recap of previous episode.
5. `episodes/EPnn/scenes/SCnn.md` per `templates/scene.md`: location, characters present, purpose, emotional beat, the lines with each character's **thought/subtext**, and the **shot list**.

**Narration format:** each shot carries one short voiceover line (max ~15 words, one breath). The speaker is either the narrator or a character in the scene. Longer dialogue is split across consecutive shots. Shot duration = voiceover length + ~0.5 s, capped at the video model's max clip length.

Keep continuity (costume, injuries, props, time of day) across scenes and episodes. When planning is done, STOP. Update `queue.md` to `planned`, summarize the series (episode titles + one line each), and ask which episode to produce.

## Step 2: PRODUCE EPISODE (only when the user names one)

Before the first paid call of the episode, state the counts (images, clips, voice lines) and wait for a yes. Then, in order:

1. **Reference sheets.** Generate any missing character-sheet and environment-sheet images used in this episode (`characters/images/`, `environments/images/`). Review them with the user if they want; later shots depend on them.
2. **Shot images.** For each shot: prompt = identity prompt(s) + location prompt + shot action + series visual style, with the matching sheet images as references → `episodes/EPnn/images/SCnn_SHnn.png`.
3. **Video clips.** Animate each image with the user's image-to-video adapter, using the shot's motion prompt → `episodes/EPnn/clips/SCnn_SHnn.mp4`.
4. **Voiceover.** Generate each shot's line with the assigned voice → `episodes/EPnn/audio/SCnn_SHnn.mp3`.
5. **Stitch.** `python tools/stitch_episode.py series/<slug>/episodes/EPnn` (needs ffmpeg) → `final/EPnn.mp4`. Optional `music.mp3` is mixed low.
6. Update `episode.md` status and `queue.md`, show the output path, ask whether to proceed to the next episode.

Repeat per episode until the series is complete; then offer a full-series cut.

## Rules

- Never produce an episode the user hasn't named; never skip ahead.
- Never write keys anywhere. Only env var **names** go in config. `.env` is gitignored.
- Paste identity and location prompts **verbatim** into every shot; never paraphrase (this is what keeps characters consistent).
- Regenerate only failed/off shots, not the whole episode.
- Save everything with the naming above so any agent can resume from files alone; the files are the state.
- If a provider call fails or is rate-limited, retry with backoff, then report which shots are missing; the next run should skip shots whose output file already exists.
