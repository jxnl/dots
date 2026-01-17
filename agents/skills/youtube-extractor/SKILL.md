---
name: youtube-extractor
description: Extract transcripts, titles, and thumbnails from YouTube videos. Use for ingesting video content, capturing captions with timestamps, or downloading video metadata.
---

# YouTube Extractor

## Overview
Use this skill to extract transcripts (with timestamps), titles, descriptions, and thumbnails from YouTube videos. Outputs are saved under a local project directory (default: `./.youtube-artifacts/<video-id>`).

## Quick Start
1. Create a local venv and install deps:
   ```bash
   uv venv
   uv add --dev yt-dlp typer
   ```
2. Extract all metadata and transcript:
   ```bash
   uv run python scripts/youtube_tools.py extract "https://youtube.com/watch?v=VIDEO_ID"
   ```
3. Get just the transcript:
   ```bash
   uv run python scripts/youtube_tools.py transcript "https://youtube.com/watch?v=VIDEO_ID"
   ```

## Tasks

### Extract all (default)
- Command: `uv run python scripts/youtube_tools.py extract <url>`
- Output: `./.youtube-artifacts/<video-id>/`
  - `metadata.json`: title, description, channel, duration, upload date
  - `transcript.json`: captions with timestamps
  - `transcript.txt`: plain text transcript
  - `thumbnail.jpg`: highest resolution thumbnail
- Behavior: Downloads all available metadata and transcript.

**Flags**
- `--out-dir <dir>`: output directory
- `--no-thumbnail`: skip thumbnail download
- `--no-transcript`: skip transcript extraction
- `--lang <code>`: preferred transcript language (default: en)
- `--overwrite / --no-overwrite`: overwrite existing outputs

### Transcript only
- Command: `uv run python scripts/youtube_tools.py transcript <url>`
- Output: `transcript.json` and `transcript.txt`
- Behavior: Extracts only captions/subtitles.

**Flags**
- `--out-dir <dir>`: output directory
- `--lang <code>`: preferred language
- `--format <json|txt|both>`: output format (default: both)

### Metadata only
- Command: `uv run python scripts/youtube_tools.py metadata <url>`
- Output: `metadata.json`
- Behavior: Extracts title, description, channel info, duration.

### Thumbnail only
- Command: `uv run python scripts/youtube_tools.py thumbnail <url>`
- Output: `thumbnail.jpg`
- Behavior: Downloads highest resolution thumbnail available.

**Flags**
- `--out-dir <dir>`: output directory
- `--quality <best|high|medium|low>`: thumbnail quality (default: best)

### Storyboard frames
- Command: `uv run python scripts/youtube_tools.py storyboard <url>`
- Output: `frames/` directory with individual timestamped JPGs + `storyboard_manifest.json`
- Behavior: Extracts YouTube's preview thumbnails (used in video scrubber) into individual frames at ~2s intervals.

**Flags**
- `--out-dir <dir>`: output directory
- `--with-transcript / -t`: also extract transcript and align each segment to its nearest frame
- `--lang <code>`: transcript language (if using --with-transcript)

## Higher quality frames with ffmpeg

Storyboard frames are low-res (~320x180). For full quality frames aligned to transcript timestamps:

1. Download video with yt-dlp:
   ```bash
   yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" -o video.mp4 <url>
   ```

2. Extract frames at specific timestamps from transcript.json:
   ```bash
   ffmpeg -ss 00:01:23 -i video.mp4 -frames:v 1 frame_83s.jpg
   ```

3. Or extract frames at regular intervals:
   ```bash
   ffmpeg -i video.mp4 -vf "fps=0.5" frames/frame_%04d.jpg  # 1 frame every 2 seconds
   ```

## Notes
- Requires network access to YouTube.
- Some videos may not have transcripts available; auto-generated captions used as fallback.
- Storyboard command requires `pillow`: `uv add --dev pillow`

## Tools
- `scripts/youtube_tools.py`: Typer CLI with `extract`, `transcript`, `metadata`, `thumbnail`, and `storyboard` commands.
