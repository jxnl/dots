---
name: pdf-viewing
description: OCR PDFs with docling while tracking per-page text and rasterize PDFs to JPEG images. Use for PDF ingestion, page-aware text extraction, or rendering pages to images, with outputs saved under a local project directory.
---

# Pdf Viewing

## Overview
Use this skill to OCR PDFs with docling and preserve page numbers, or rasterize PDF pages into JPEGs for visual inspection. Always save outputs under a local project directory (default: `./.pdf-artifacts/<pdf-stem>`).

## Quick Start
1. Create a local venv in the project and install deps:
   ```bash
   uv venv
   uv pip install docling typer pymupdf
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
- `--out-dir <dir>`: output directory (relative paths are rooted at the current project)
- `--copy-pdf / --no-copy-pdf`: control whether the input PDF is copied into the output dir
- `--pages-json <name>`: JSON filename for per-page text
- `--pages-text <name>`: TXT filename for per-page text

### Rasterize to JPEG
- Command: `uv run python scripts/pdf_tools.py rasterize <pdf-path>`
- Output (default): `./.pdf-artifacts/<pdf-stem>/images/page-0001.jpg` (etc.)
- Behavior: Renders each PDF page to a JPEG at the requested DPI.

**Explicit flags**
- `--out-dir <dir>`: output directory (relative paths are rooted at the current project)
- `--copy-pdf / --no-copy-pdf`: control whether the input PDF is copied into the output dir
- `--dpi <int>`: rasterization DPI
- `--images-dir <name>`: directory for output JPEGs
- `--images-manifest <name>`: JSON manifest name with image paths

## Notes
- Keep outputs inside the current project by using the default output directory or a relative `--out-dir`.
- If docling requires extra OCR backends in your environment, install them before running OCR.

## Tools
- `scripts/pdf_tools.py`: Typer CLI with `ocr` and `rasterize` commands.
