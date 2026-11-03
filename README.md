# Micro Drama Skill

An agent skill that turns a story into a narrated AI micro drama series, planned in full, produced one episode at a time.

**Bring your own API keys.** You choose the image, image-to-video and voice services; the agent configures adapters for them on first run. No keys are stored in this repo.

## Use it

Give any coding agent (Claude Code, Codex, Gemini CLI, Cursor, ...) this prompt:

> Use the micro-drama skill from https://github.com/Dorisautomate/micro-drama-skill. Read its SKILL.md and follow it. Here is my story: ...

For Claude Code you can also install it as a skill:

```bash
git clone https://github.com/Dorisautomate/micro-drama-skill ~/.claude/skills/micro-drama
```

## What happens

1. **Setup:** agent asks which image / video / voice services you use and which env vars hold your keys, then writes small adapters in `tools/adapters/`.
2. **Plan:** from your story it plans the whole series: episodes, scenes, thoughts behind each line, shots, multi-angle character sheets, environment sheets.
3. **Produce:** you name an episode. It generates shot images, animates them, adds a short voiceover per shot, and stitches the episode with ffmpeg. Then it asks about the next episode.

## Requirements

- An agent that can read files, run commands and call HTTP APIs
- Python 3 and [ffmpeg](https://ffmpeg.org/) on PATH
- API keys for your chosen image, image-to-video and voice services, set as environment variables (see `.env.example`)

## Layout

```
SKILL.md          The skill (agents read this first)
templates/        Formats for characters, environments, episodes, scenes/shots
tools/            stitch_episode.py + adapters/ guide
config/           providers.example.md (copy to providers.md)
story/            story-template.md
queue.md          Micro drama queue
```
