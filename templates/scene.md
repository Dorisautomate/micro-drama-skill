# EP<nn> / SC<nn>: <Title>

- Location (environment file):
- Time of day / weather:
- Characters present (character files):
- Purpose of scene:
- Emotional beat (start -> end):
- Continuity notes (props, costume, injuries):

## Conversation
Back and forth, 6-10 lines, each 8-16 words, in each speaker's real register (class, age, region).
Duration comes from `python tools/plan_durations.py` (smallest clip length that fits the line).

| # | Speaker | Line (spoken in the clip) | Thought / subtext | Delivery | Shot (image) | Clip length (s) |
|---|---------|---------------------------|-------------------|----------|--------------|-----------------|
| 1 | | | | | Speaker medium | |

## Coverage plan (generate in this order)
| Image id | Shot | Framing | References to attach | Notes (who looks where) |
|----------|------|---------|----------------------|-------------------------|
| E | Establishing wide | all speakers visible, positions fixed | character images + environment image | A on left, B on right |
| A_m | A medium | medium, same side as E | E + A image | looks toward B (off-screen right) |
| A_c | A close-up | tight | E + A image | same eyeline |
| B_m | B medium | | E + B image | |
| B_c | B close-up | | E + B image | |

Optional silent inserts (about 3 s, no narration): establishing hold, reaction, someone passing.

## Clip prompts
One per line, using the template in `references/dialogue-coverage.md` (voice description + exact line + lip sync + finish the sentence + hold a pause).
