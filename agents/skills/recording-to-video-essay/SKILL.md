---
name: recording-to-video-essay
description: Turn a raw talking-head recording or voiceover into a tight video essay with word-level timing, clean cuts, captions, and timed image overlays. Use when someone wants to edit a spoken recording, remove pauses and false starts, keep the speaker's words and order, add B-roll or screenshots, or use FFmpeg and Remotion to make a preview and final video.
---

# Recording to Video Essay

Clean the recording. Do not rewrite the speaker.

## Core rule

Keep the speaker's words, order, pacing, and meaning unless they ask otherwise. Remove clear false starts, repeated takes, long pauses, and filler only when the cut is safe. Never cut through a spoken word. Do not invent narration, claims, images, or transitions.

Never overwrite the source recording. Do not upload or publish a result without a separate instruction.

## Inputs

Ask only for missing inputs that block the edit: the recording, an optional finished post or outline, optional images/screenshots/B-roll, and the target shape when it matters. Use a word-level transcript from an available transcription tool. The helper accepts the simple JSON formats in [references/transcript-format.md](references/transcript-format.md). Do not put credentials or source media in the skill or repository.

## Workflow

1. Inspect the recording and supplied post. Identify the intended message, useful sections, repeated takes, and likely image moments. Preserve the spoken order by default.
2. Extract audio if the transcription tool needs it:

   ```bash
   ffmpeg -hide_banner -y -i recording.mov -vn -ac 1 -ar 16000 source-audio.wav
   ```

3. Create or obtain a transcript with word-level timestamps. Save it as `word-level-transcript.json`.
4. Build a reviewable edit plan before rendering:

   ```bash
   python3 scripts/prepare_edit.py word-level-transcript.json --output-dir output/video-essay
   ```

   The helper writes `transcript.md` and `edit-plan.json`. It proposes cuts only in gaps between words and flags common filler words for review. It does not delete spoken words automatically.
5. Review the transcript and edit plan. Correct names, punctuation, and clear transcription errors. Keep the final complete take after a clear restart. Add intentional source-time cuts to `manual_cuts`, leave uncertain cuts disabled, and preserve a small tail after one word and lead before the next.
6. Place supplied images where they support a spoken phrase. Keep a simple `overlays.json` plan:

   ```json
   [
     {
       "file": "images/example.png",
       "start_phrase": "the line where this becomes useful",
       "end_phrase": "the end of the example"
     }
   ]
   ```

   Phrase anchors survive small timing changes. Do not imply that a supplied image proves a claim it does not support.
7. Make the edit with the tools already used by the project. Use FFmpeg for cuts, timing, crop, scale, and image composition. Use Remotion when the project needs styled, timed captions or complex overlays. Use plain subtitle files when a Remotion project is not present. Keep caption text faithful to the remaining audio. Prefer readable phrases over flashing one word at a time unless the user asks for word-level captions.
8. Render a fast preview first. Inspect the opening, every cut, every overlay, caption timing, audio sync, and final spoken moment. Fix visible issues before the final render.
9. Render the final video to a new file. Verify that its duration matches the edit plan, the video plays, captions remain readable, and no source word was clipped.

## Default video prompt

> I have attached the recording, the finished post, and the images I want you to overlay. Turn the recording into a short video using the post as context. Transcribe the recording with word-level timestamps. Remove false starts, long pauses, filler, and repeated takes. Keep the remaining clips in the order I said them unless I ask otherwise. Use FFmpeg to make the cuts, find useful places to overlay the images, and use Remotion for subtitles when available. Keep my pacing and meaning. Do not rewrite what I said, reorder the story, or add effects that distract from it.

## Output

Keep the edit reviewable. Return paths for the transcript, word-level transcript, edit and overlay plans, preview, and final video. Call out unresolved cuts, missing images, or caption problems. Never claim a final render was checked if it was not played or inspected.
