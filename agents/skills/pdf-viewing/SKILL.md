---
name: pdf-viewing
description: OCR PDFs with docling while tracking per-page text and rasterize PDFs to images. Use for PDF ingestion, page-aware text extraction, rendering pages to images, or inspecting PDF metadata, with outputs saved under a local project directory.
---

# Pdf Viewing

## Overview
Use this skill to OCR PDFs with docling and preserve page numbers, rasterize pages into images, or inspect PDF metadata. Always save outputs under a local project directory (default: `./.pdf-artifacts/<pdf-stem>`).

## Quick Start
1. Create a local venv in the project and install deps as dev dependencies:
   ```bash
   uv venv
   uv add --dev docling typer pymupdf
   ```
2. Run the OCR tool:
   ```bash
   uv run python scripts/pdf_tools.py ocr path/to/file.pdf --out-dir ./.pdf-artifacts/<pdf-stem>
   ```
3. Run the rasterizer:
   ```bash
   uv run python scripts/pdf_tools.py rasterize path/to/file.pdf --out-dir ./.pdf-artifacts/<pdf-stem>
   ```

## Tasks

### OCR with page tracking
- Command: `uv run python scripts/pdf_tools.py ocr <pdf-path>`
- Output (default): `./.pdf-artifacts/<pdf-stem>/ocr-pages.json` and `ocr-pages.txt`
- Behavior: Copies the input PDF into the output dir and writes per-page text with page numbers.

**Explicit flags**
- `--out-dir <dir>`: output directory (relative paths are rooted at the project root)
- `--project-root <dir>`: base path for relative output paths
- `--copy-pdf / --no-copy-pdf`: control whether the input PDF is copied into the output dir
- `--pages <ranges>`: page ranges like `1-3,5,8-10`
- `--pages-json <name>`: JSON filename for per-page text
- `--pages-text <name>`: TXT filename for per-page text
- `--manifest <name>`: manifest filename (default `manifest.json`)
- `--overwrite / --no-overwrite`: overwrite existing outputs
- `--dry-run`: show what would be written

### Rasterize to images
- Command: `uv run python scripts/pdf_tools.py rasterize <pdf-path>`
- Output (default): `./.pdf-artifacts/<pdf-stem>/images/page-0001.jpg` (etc.)
- Behavior: Renders each PDF page to an image at the requested DPI.

**Explicit flags**
- `--out-dir <dir>`: output directory (relative paths are rooted at the project root)
- `--project-root <dir>`: base path for relative output paths
- `--copy-pdf / --no-copy-pdf`: control whether the input PDF is copied into the output dir
- `--pages <ranges>`: page ranges like `1-3,5,8-10`
- `--dpi <int>`: rasterization DPI
- `--format <jpg|png|webp>`: output image format
- `--quality <1-100>`: for jpg/webp
- `--images-dir <name>`: directory for output images
- `--images-manifest <name>`: JSON manifest name with image paths
- `--manifest <name>`: manifest filename (default `manifest.json`)
- `--overwrite / --no-overwrite`: overwrite existing outputs
- `--dry-run`: show what would be written

### Inspect metadata
- Command: `uv run python scripts/pdf_tools.py inspect <pdf-path>`
- Output: writes metadata to stdout and `manifest.json` unless `--no-manifest`

### Clean artifacts
- Command: `uv run python scripts/pdf_tools.py clean <pdf-path>`
- Behavior: Removes the artifact directory for the PDF.

## Notes
- Keep outputs inside the current project by using the default output directory or a relative `--out-dir`.
- If docling requires extra OCR backends in your environment, install them before running OCR.

## Tools
- `scripts/pdf_tools.py`: Typer CLI with `ocr`, `rasterize`, `inspect`, and `clean` commands.
