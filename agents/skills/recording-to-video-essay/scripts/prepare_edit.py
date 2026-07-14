#!/usr/bin/env python3
"""Build a safe, reviewable edit plan from a word-level transcript."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FILLERS = {"ah", "er", "erm", "hmm", "uh", "uhm", "um", "umm"}


def seconds(item: dict[str, Any], key: str, millis_key: str) -> float:
    if key in item:
        return float(item[key])
    if millis_key in item:
        return float(item[millis_key]) / 1000
    raise ValueError(f"Word is missing {key} or {millis_key}: {item!r}")


def load_words(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    raw_words = value.get("words") if isinstance(value, dict) else value
    if not isinstance(raw_words, list) or not raw_words:
        raise ValueError("Transcript must contain a non-empty words array")

    words: list[dict[str, Any]] = []
    previous_start = -1.0
    for index, item in enumerate(raw_words):
        if not isinstance(item, dict):
            raise ValueError(f"Word {index} is not an object")
        text = str(item.get("word", item.get("text", ""))).strip()
        start = seconds(item, "start", "startMs")
        end = seconds(item, "end", "endMs")
        if not text:
            raise ValueError(f"Word {index} has no text")
        if start < 0 or end < start or start < previous_start:
            raise ValueError(f"Word {index} has invalid or unordered timestamps")
        words.append({"word": text, "start": start, "end": end})
        previous_start = start
    return words


def transcript_text(words: list[dict[str, Any]]) -> str:
    text = " ".join(str(item["word"]) for item in words)
    return re.sub(r"\s+([,.;:!?])", r"\1", text).strip()


def silence_cuts(
    words: list[dict[str, Any]], minimum_gap: float, word_tail: float, word_lead: float
) -> list[dict[str, Any]]:
    cuts: list[dict[str, Any]] = []
    for left, right in zip(words, words[1:]):
        gap_start = float(left["end"])
        gap_end = float(right["start"])
        if gap_end - gap_start < minimum_gap:
            continue
        start = gap_start + word_tail
        end = gap_end - word_lead
        if end <= start:
            continue
        cuts.append(
            {
                "start": round(start, 6),
                "end": round(end, 6),
                "gap_start": round(gap_start, 6),
                "gap_end": round(gap_end, 6),
                "enabled": True,
            }
        )
    return cuts


def filler_candidates(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for item in words:
        normalized = re.sub(r"[^a-z]", "", str(item["word"]).lower())
        if normalized in FILLERS:
            candidates.append(
                {
                    "word": item["word"],
                    "start": round(float(item["start"]), 6),
                    "end": round(float(item["end"]), 6),
                    "enabled": False,
                }
            )
    return candidates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", type=Path, help="Word-level transcript JSON")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--minimum-gap", type=float, default=0.55)
    parser.add_argument("--word-tail", type=float, default=0.20)
    parser.add_argument("--word-lead", type=float, default=0.12)
    args = parser.parse_args()

    if min(args.minimum_gap, args.word_tail, args.word_lead) < 0:
        raise SystemExit("Timing values must be non-negative")
    words = load_words(args.transcript.expanduser().resolve())
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = {
        "version": 1,
        "source_transcript": str(args.transcript.expanduser().resolve()),
        "word_count": len(words),
        "silence_cuts": silence_cuts(words, args.minimum_gap, args.word_tail, args.word_lead),
        "filler_candidates": filler_candidates(words),
        "manual_cuts": [],
    }
    (output_dir / "edit-plan.json").write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (output_dir / "transcript.md").write_text(
        "# Transcript\n\n" + transcript_text(words) + "\n", encoding="utf-8"
    )
    print(f"Wrote {output_dir / 'transcript.md'}")
    print(f"Wrote {output_dir / 'edit-plan.json'}")


if __name__ == "__main__":
    main()
