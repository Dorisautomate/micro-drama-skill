# Provider adapters

The agent writes these on first run, for whichever services the user chose. Each is a small Python CLI (standard library `urllib`, or `requests` if installed) that reads its API key from the env var named in `config/providers.md`, makes the call (polling if the API is async), and writes the result to the output path. Exit non-zero on failure, print the provider error. Skip work if the output file already exists.

## image.py
```
python tools/adapters/image.py --prompt "<text>" [--ref path.png ...] --aspect 9:16 --out path.png
```

## video.py (image-to-video)
```
python tools/adapters/video.py --image path.png --prompt "<motion text>" --seconds 5 --aspect 9:16 --out path.mp4
```

## voice.py (text-to-speech)
```
python tools/adapters/voice.py --text "<line>" --voice <voice id> --out path.mp3
```

Rules: never hard-code keys; never log headers; retry 429/5xx with backoff; test with one cheap call before a batch.
