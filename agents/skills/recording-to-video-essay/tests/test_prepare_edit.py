#!/usr/bin/env python3
"""Small regression checks for the public edit-plan helper."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_edit.py"
SPEC = importlib.util.spec_from_file_location("prepare_edit", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PrepareEditTest(unittest.TestCase):
    def test_silence_cut_stays_between_words(self) -> None:
        words = [
            {"word": "hello", "start": 0.0, "end": 0.4},
            {"word": "world", "start": 1.4, "end": 1.8},
        ]
        cuts = MODULE.silence_cuts(words, 0.55, 0.20, 0.12)
        self.assertEqual(len(cuts), 1)
        self.assertGreater(cuts[0]["start"], words[0]["end"])
        self.assertLess(cuts[0]["end"], words[1]["start"])

    def test_short_gap_is_kept(self) -> None:
        words = [
            {"word": "hello", "start": 0.0, "end": 0.4},
            {"word": "world", "start": 0.7, "end": 1.0},
        ]
        self.assertEqual(MODULE.silence_cuts(words, 0.55, 0.20, 0.12), [])

    def test_filler_is_flagged_but_disabled(self) -> None:
        candidate = MODULE.filler_candidates(
            [{"word": "um,", "start": 0.4, "end": 0.7}]
        )[0]
        self.assertEqual(candidate["word"], "um,")
        self.assertFalse(candidate["enabled"])

    def test_transcript_punctuation_is_compact(self) -> None:
        words = [{"word": "hello"}, {"word": ","}, {"word": "world"}, {"word": "!"}]
        self.assertEqual(MODULE.transcript_text(words), "hello, world!")


if __name__ == "__main__":
    unittest.main()
