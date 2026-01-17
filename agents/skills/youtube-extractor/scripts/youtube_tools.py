#!/usr/bin/env python3
"""YouTube video extraction tool for transcripts, metadata, and thumbnails."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path
from typing import Any

import typer

app = typer.Typer(help="Extract transcripts, titles, and thumbnails from YouTube videos.")


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def get_output_dir(out_dir: Path | None, video_id: str) -> Path:
    """Get or create output directory."""
    if out_dir:
        path = out_dir
    else:
        path = Path(".youtube-artifacts") / video_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def fetch_metadata(video_id: str) -> dict[str, Any]:
    """Fetch video metadata using yt-dlp."""
    import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)

    return {
        "video_id": video_id,
        "title": info.get("title"),
        "description": info.get("description"),
        "channel": info.get("channel"),
        "channel_id": info.get("channel_id"),
        "uploader": info.get("uploader"),
        "upload_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "duration_string": info.get("duration_string"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "tags": info.get("tags", []),
        "categories": info.get("categories", []),
        "thumbnail_url": info.get("thumbnail"),
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }


def fetch_transcript(video_id: str, lang: str = "en") -> list[dict[str, Any]]:
    """Fetch transcript/captions using yt-dlp."""
    import yt_dlp

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": [lang, "en"],
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)

    subtitles = info.get("subtitles", {})
    auto_captions = info.get("automatic_captions", {})

    # Prefer manual subtitles, fall back to auto-generated
    captions = subtitles.get(lang) or subtitles.get("en") or auto_captions.get(lang) or auto_captions.get("en")

    if not captions:
        return []

    # Find json3 format or fall back to first available
    caption_url = None
    for cap in captions:
        if cap.get("ext") == "json3":
            caption_url = cap.get("url")
            break
    if not caption_url and captions:
        caption_url = captions[0].get("url")

    if not caption_url:
        return []

    # Fetch and parse captions
    with urllib.request.urlopen(caption_url) as response:
        data = json.loads(response.read().decode("utf-8"))

    transcript = []
    for event in data.get("events", []):
        if "segs" not in event:
            continue
        text = "".join(seg.get("utf8", "") for seg in event["segs"]).strip()
        if text:
            start_ms = event.get("tStartMs", 0)
            duration_ms = event.get("dDurationMs", 0)
            transcript.append({
                "text": text,
                "start": start_ms / 1000,
                "duration": duration_ms / 1000,
            })

    return transcript


def fetch_storyboard_info(video_id: str) -> dict[str, Any] | None:
    """Fetch storyboard format info using yt-dlp."""
    import yt_dlp

    ydl_opts = {"quiet": True, "no_warnings": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)

    # Find best storyboard (sb0 = highest res, sb3 = lowest)
    for fmt_id in ["sb0", "sb1", "sb2", "sb3"]:
        for f in info.get("formats", []):
            if f.get("format_id") == fmt_id:
                return f
    return None


def extract_storyboard_frames(
    video_id: str,
    out_dir: Path,
    interval: float | None = None,
) -> list[dict[str, Any]]:
    """Download storyboard sprites and extract individual frames.

    Returns list of frame info dicts with path and timestamp.
    """
    from io import BytesIO
    from PIL import Image

    storyboard = fetch_storyboard_info(video_id)
    if not storyboard:
        return []

    frames_dir = out_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    fps = storyboard["fps"]
    frame_duration = 1 / fps
    cols = storyboard["columns"]
    rows = storyboard["rows"]
    thumb_w = storyboard["width"]
    thumb_h = storyboard["height"]
    headers = storyboard.get("http_headers", {})

    frames = []
    frame_idx = 0

    for fragment in storyboard.get("fragments", []):
        url = fragment["url"]
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            img_data = response.read()

        sprite = Image.open(BytesIO(img_data))
        sprite_w, sprite_h = sprite.size

        for row in range(rows):
            for col in range(cols):
                left = col * thumb_w
                top = row * thumb_h
                right = left + thumb_w
                bottom = top + thumb_h

                if right > sprite_w or bottom > sprite_h:
                    continue

                timestamp = frame_idx * frame_duration

                # Skip frames if interval specified
                if interval and frame_idx > 0:
                    if timestamp % interval >= frame_duration:
                        frame_idx += 1
                        continue

                thumb = sprite.crop((left, top, right, bottom))
                mins = int(timestamp // 60)
                secs = int(timestamp % 60)

                filename = f"frame_{frame_idx:03d}_{mins:02d}m{secs:02d}s.jpg"
                filepath = frames_dir / filename
                thumb.save(filepath, "JPEG", quality=90)

                frames.append({
                    "index": frame_idx,
                    "timestamp": timestamp,
                    "timestamp_str": f"{mins:02d}:{secs:02d}",
                    "path": str(filepath),
                })
                frame_idx += 1

    return frames


def download_thumbnail(video_id: str, out_path: Path, quality: str = "best") -> Path | None:
    """Download video thumbnail."""
    quality_urls = {
        "best": [
            f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            f"https://img.youtube.com/vi/{video_id}/sddefault.jpg",
            f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        ],
        "high": [f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"],
        "medium": [f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"],
        "low": [f"https://img.youtube.com/vi/{video_id}/default.jpg"],
    }

    urls = quality_urls.get(quality, quality_urls["best"])

    for url in urls:
        try:
            with urllib.request.urlopen(url) as response:
                # Check if we got a valid image (not the placeholder)
                data = response.read()
                if len(data) > 1000:  # Valid thumbnails are larger
                    out_path.write_bytes(data)
                    return out_path
        except Exception:
            continue

    return None


@app.command()
def extract(
    url: str = typer.Argument(..., help="YouTube video URL or ID"),
    out_dir: Path | None = typer.Option(None, "--out-dir", "-o", help="Output directory"),
    no_thumbnail: bool = typer.Option(False, "--no-thumbnail", help="Skip thumbnail download"),
    no_transcript: bool = typer.Option(False, "--no-transcript", help="Skip transcript extraction"),
    lang: str = typer.Option("en", "--lang", "-l", help="Preferred transcript language"),
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing files"),
) -> None:
    """Extract all metadata, transcript, and thumbnail from a YouTube video."""
    video_id = extract_video_id(url)
    output = get_output_dir(out_dir, video_id)

    typer.echo(f"Extracting video: {video_id}")
    typer.echo(f"Output directory: {output}")

    # Metadata
    metadata_path = output / "metadata.json"
    if overwrite or not metadata_path.exists():
        typer.echo("Fetching metadata...")
        metadata = fetch_metadata(video_id)
        metadata_path.write_text(json.dumps(metadata, indent=2))
        typer.echo(f"  Title: {metadata['title']}")
    else:
        typer.echo("Metadata already exists, skipping.")

    # Transcript
    if not no_transcript:
        transcript_json = output / "transcript.json"
        transcript_txt = output / "transcript.txt"
        if overwrite or not transcript_json.exists():
            typer.echo(f"Fetching transcript (lang={lang})...")
            transcript = fetch_transcript(video_id, lang)
            if transcript:
                transcript_json.write_text(json.dumps(transcript, indent=2))
                plain_text = "\n".join(entry["text"] for entry in transcript)
                transcript_txt.write_text(plain_text)
                typer.echo(f"  Transcript: {len(transcript)} segments")
            else:
                typer.echo("  No transcript available.")
        else:
            typer.echo("Transcript already exists, skipping.")

    # Thumbnail
    if not no_thumbnail:
        thumbnail_path = output / "thumbnail.jpg"
        if overwrite or not thumbnail_path.exists():
            typer.echo("Downloading thumbnail...")
            result = download_thumbnail(video_id, thumbnail_path)
            if result:
                typer.echo(f"  Saved: {thumbnail_path}")
            else:
                typer.echo("  Could not download thumbnail.")
        else:
            typer.echo("Thumbnail already exists, skipping.")

    typer.echo(f"Done. Files saved to: {output}")


@app.command()
def transcript(
    url: str = typer.Argument(..., help="YouTube video URL or ID"),
    out_dir: Path | None = typer.Option(None, "--out-dir", "-o", help="Output directory"),
    lang: str = typer.Option("en", "--lang", "-l", help="Preferred language"),
    format: str = typer.Option("both", "--format", "-f", help="Output format: json, txt, or both"),
) -> None:
    """Extract only the transcript from a YouTube video."""
    video_id = extract_video_id(url)
    output = get_output_dir(out_dir, video_id)

    typer.echo(f"Fetching transcript for: {video_id}")
    transcript_data = fetch_transcript(video_id, lang)

    if not transcript_data:
        typer.echo("No transcript available for this video.")
        raise typer.Exit(1)

    if format in ("json", "both"):
        path = output / "transcript.json"
        path.write_text(json.dumps(transcript_data, indent=2))
        typer.echo(f"Saved: {path}")

    if format in ("txt", "both"):
        path = output / "transcript.txt"
        plain_text = "\n".join(entry["text"] for entry in transcript_data)
        path.write_text(plain_text)
        typer.echo(f"Saved: {path}")

    typer.echo(f"Extracted {len(transcript_data)} segments.")


@app.command()
def metadata(
    url: str = typer.Argument(..., help="YouTube video URL or ID"),
    out_dir: Path | None = typer.Option(None, "--out-dir", "-o", help="Output directory"),
) -> None:
    """Extract only metadata from a YouTube video."""
    video_id = extract_video_id(url)
    output = get_output_dir(out_dir, video_id)

    typer.echo(f"Fetching metadata for: {video_id}")
    data = fetch_metadata(video_id)

    path = output / "metadata.json"
    path.write_text(json.dumps(data, indent=2))

    typer.echo(f"Title: {data['title']}")
    typer.echo(f"Channel: {data['channel']}")
    typer.echo(f"Duration: {data['duration_string']}")
    typer.echo(f"Saved: {path}")


@app.command()
def thumbnail(
    url: str = typer.Argument(..., help="YouTube video URL or ID"),
    out_dir: Path | None = typer.Option(None, "--out-dir", "-o", help="Output directory"),
    quality: str = typer.Option("best", "--quality", "-q", help="Quality: best, high, medium, low"),
) -> None:
    """Download only the thumbnail from a YouTube video."""
    video_id = extract_video_id(url)
    output = get_output_dir(out_dir, video_id)

    typer.echo(f"Downloading thumbnail for: {video_id}")
    path = output / "thumbnail.jpg"
    result = download_thumbnail(video_id, path, quality)

    if result:
        typer.echo(f"Saved: {path}")
    else:
        typer.echo("Could not download thumbnail.")
        raise typer.Exit(1)


@app.command()
def storyboard(
    url: str = typer.Argument(..., help="YouTube video URL or ID"),
    out_dir: Path | None = typer.Option(None, "--out-dir", "-o", help="Output directory"),
    with_transcript: bool = typer.Option(False, "--with-transcript", "-t", help="Also extract transcript and create aligned manifest"),
    lang: str = typer.Option("en", "--lang", "-l", help="Transcript language (if --with-transcript)"),
) -> None:
    """Extract timestamped thumbnail frames from YouTube's storyboard sprites.

    Downloads the preview thumbnails YouTube uses for the video scrubber and
    splits them into individual frames with timestamps. Useful for:

    - Visual summaries of video content
    - Matching transcript segments to visual context
    - Creating thumbnail galleries for navigation
    - AI/ML training data with time-aligned frames
    """
    video_id = extract_video_id(url)
    output = get_output_dir(out_dir, video_id)

    typer.echo(f"Extracting storyboard for: {video_id}")

    frames = extract_storyboard_frames(video_id, output)
    if not frames:
        typer.echo("No storyboard available for this video.")
        raise typer.Exit(1)

    typer.echo(f"Extracted {len(frames)} frames to {output}/frames/")

    # Save frames manifest
    manifest = {"video_id": video_id, "frame_count": len(frames), "frames": frames}

    if with_transcript:
        typer.echo(f"Fetching transcript (lang={lang})...")
        transcript = fetch_transcript(video_id, lang)

        if transcript:
            # Align transcript segments with nearest frames
            for seg in transcript:
                seg_time = seg["start"]
                nearest = min(frames, key=lambda f: abs(f["timestamp"] - seg_time))
                seg["nearest_frame"] = nearest["index"]
                seg["nearest_frame_path"] = nearest["path"]

            manifest["transcript"] = transcript
            typer.echo(f"Aligned {len(transcript)} transcript segments with frames.")
        else:
            typer.echo("No transcript available.")

    manifest_path = output / "storyboard_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    typer.echo(f"Saved manifest: {manifest_path}")


def main() -> int:
    app()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
