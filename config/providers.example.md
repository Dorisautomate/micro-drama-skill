# Providers (copy to config/providers.md)

Only env var NAMES go here, never the keys themselves.

## Image generation
- Provider / model:
- API key env var:
- Reference-image input supported (yes/no):
- Adapter: tools/adapters/image.py

## Image-to-video
- Provider / model:
- API key env var:
- Max clip length (s):
- Adapter: tools/adapters/video.py

## Voice (optional: speech normally comes from the video model itself)
- Provider / model:
- API key env var:
- Per-character voice descriptions live in each character file
- Character voices: (Character → voice id)
- Adapter: tools/adapters/voice.py

## Music (optional)
- Provider or file:

## Output
- Resolution / aspect ratio: 1920x1080 (16:9)
- FPS: 24
