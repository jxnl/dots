# Word-Level Transcript Format

`scripts/prepare_edit.py` accepts a JSON array of words or an object with a `words` array.

```json
{
  "words": [
    {"word": "I", "start": 0.2, "end": 0.3},
    {"word": "have", "start": 0.31, "end": 0.48},
    {"word": "an", "start": 0.49, "end": 0.57},
    {"word": "idea.", "start": 0.58, "end": 0.82}
  ]
}
```

The helper also accepts `text` instead of `word`, and `startMs`/`endMs` instead of seconds. Word times must be ordered and non-negative.

The generated edit plan uses source-video seconds:

```json
{
  "silence_cuts": [{"start": 2.1, "end": 2.8, "enabled": true}],
  "filler_candidates": [{"word": "um", "start": 3.0, "end": 3.2, "enabled": false}],
  "manual_cuts": []
}
```

Silence cuts are proposed only between words. Filler candidates stay disabled until reviewed because a word that looks like filler can still carry tone or meaning.
