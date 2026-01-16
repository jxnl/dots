#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

import typer

app = typer.Typer(add_completion=False, no_args_is_help=True)
TOOL_VERSION = "1.0"


@dataclass(frozen=True)
class OutputPaths:
    out_dir: Path
    manifest_path: Path


def _project_root(project_root: Optional[Path]) -> Path:
    if project_root is None:
        return Path.cwd()
    root = Path(project_root)
    if not root.is_absolute():
        root = Path.cwd() / root
    return root


def _resolve_out_dir(pdf_path: Path, out_dir: Optional[Path], project_root: Optional[Path]) -> Path:
    root = _project_root(project_root)
    if out_dir is None:
        out_dir = root / ".pdf-artifacts" / pdf_path.stem
    else:
        out_dir = Path(out_dir)
        if not out_dir.is_absolute():
            out_dir = root / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _output_paths(pdf_path: Path, out_dir: Optional[Path], project_root: Optional[Path], manifest: str) -> OutputPaths:
    resolved = _resolve_out_dir(pdf_path, out_dir, project_root)
    return OutputPaths(out_dir=resolved, manifest_path=resolved / manifest)


def _copy_pdf(pdf_path: Path, out_dir: Path) -> Path:
    dest = out_dir / pdf_path.name
    if pdf_path.resolve() != dest.resolve():
        shutil.copy2(pdf_path, dest)
    return dest


def _page_text(page: object) -> str:
    for attr in ("text", "content", "markdown", "md"):
        if hasattr(page, attr):
            value = getattr(page, attr)
            if callable(value):
                try:
                    value = value()
                except TypeError:
                    pass
            if isinstance(value, str):
                return value
    return str(page)


def _parse_ranges(ranges: Optional[str]) -> Optional[set[int]]:
    if not ranges:
        return None
    pages: set[int] = set()
    parts = [part.strip() for part in ranges.split(",") if part.strip()]
    for part in parts:
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                start, end = end, start
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return pages


def _ensure_overwrite(paths: Iterable[Path], overwrite: bool) -> None:
    if overwrite:
        return
    for path in paths:
        if path.exists():
            typer.echo(f"Refusing to overwrite existing file: {path}", err=True)
            raise typer.Exit(code=1)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest_base(pdf_path: Path, copied_path: Optional[Path]) -> dict:
    return {
        "tool": "pdf-viewing",
        "tool_version": TOOL_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_path": str(pdf_path),
        "input_sha256": _sha256(pdf_path),
        "input_size_bytes": pdf_path.stat().st_size,
        "copied_path": str(copied_path) if copied_path else None,
    }


def _write_manifest(path: Path, payload: dict, overwrite: bool, dry_run: bool) -> None:
    if dry_run:
        typer.echo(f"[dry-run] Would write manifest: {path}")
        return
    _ensure_overwrite([path], overwrite)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2))
    typer.echo(f"Wrote {path}")


def _select_pages(pages: Optional[set[int]], total: int) -> list[int]:
    if pages is None:
        return list(range(1, total + 1))
    return sorted(p for p in pages if 1 <= p <= total)


@app.command()
def ocr(
    pdf_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o"),
    project_root: Optional[Path] = typer.Option(None, "--project-root"),
    copy_pdf: bool = typer.Option(True, "--copy-pdf/--no-copy-pdf"),
    pages: Optional[str] = typer.Option(None, "--pages"),
    pages_json: str = typer.Option("ocr-pages.json", "--pages-json"),
    pages_text: str = typer.Option("ocr-pages.txt", "--pages-text"),
    manifest: str = typer.Option("manifest.json", "--manifest"),
    overwrite: bool = typer.Option(False, "--overwrite/--no-overwrite"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """OCR a PDF with docling and save per-page text."""
    outputs = _output_paths(pdf_path, out_dir, project_root, manifest)
    copied_path = _copy_pdf(pdf_path, outputs.out_dir) if copy_pdf else None

    try:
        from docling.document_converter import DocumentConverter
    except Exception as exc:  # pragma: no cover - runtime dependency
        typer.echo(f"Failed to import docling: {exc}", err=True)
        raise typer.Exit(code=1)

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    document = result.document

    selected_pages = _parse_ranges(pages)
    page_entries = []
    page_numbers = []

    doc_pages = getattr(document, "pages", None)
    if doc_pages:
        total = len(doc_pages)
        want = _select_pages(selected_pages, total)
        for idx, page in enumerate(doc_pages, start=1):
            if idx not in want:
                continue
            page_no = getattr(page, "page_number", idx)
            page_entries.append({"page": int(page_no), "text": _page_text(page)})
            page_numbers.append(int(page_no))
    else:
        if selected_pages and selected_pages != {1}:
            typer.echo("Page filtering is unavailable without per-page output from docling.", err=True)
        if hasattr(document, "export_to_text"):
            text = document.export_to_text()
        else:
            text = str(document)
        page_entries.append({"page": 1, "text": text})
        page_numbers.append(1)

    json_path = outputs.out_dir / pages_json
    text_path = outputs.out_dir / pages_text

    if dry_run:
        typer.echo(f"[dry-run] Would write {json_path}")
        typer.echo(f"[dry-run] Would write {text_path}")
    else:
        _ensure_overwrite([json_path, text_path], overwrite)
        json_path.write_text(json.dumps(page_entries, ensure_ascii=True, indent=2))
        parts = []
        for entry in page_entries:
            parts.append(f"=== Page {entry['page']} ===\n{entry['text']}")
        text_path.write_text("\n\n".join(parts), encoding="utf-8")
        typer.echo(f"Wrote {json_path}")
        typer.echo(f"Wrote {text_path}")

    manifest_payload = _manifest_base(pdf_path, copied_path)
    manifest_payload.update(
        {
            "command": "ocr",
            "pages": page_numbers,
            "ocr_json": str(json_path),
            "ocr_text": str(text_path),
        }
    )
    _write_manifest(outputs.manifest_path, manifest_payload, overwrite, dry_run)


@app.command()
def rasterize(
    pdf_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o"),
    project_root: Optional[Path] = typer.Option(None, "--project-root"),
    copy_pdf: bool = typer.Option(True, "--copy-pdf/--no-copy-pdf"),
    pages: Optional[str] = typer.Option(None, "--pages"),
    dpi: int = typer.Option(200, "--dpi"),
    image_format: str = typer.Option("jpg", "--format"),
    quality: int = typer.Option(85, "--quality"),
    images_dir: str = typer.Option("images", "--images-dir"),
    images_manifest: str = typer.Option("images.json", "--images-manifest"),
    manifest: str = typer.Option("manifest.json", "--manifest"),
    overwrite: bool = typer.Option(False, "--overwrite/--no-overwrite"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Rasterize a PDF to images using PyMuPDF."""
    outputs = _output_paths(pdf_path, out_dir, project_root, manifest)
    copied_path = _copy_pdf(pdf_path, outputs.out_dir) if copy_pdf else None

    try:
        import fitz  # PyMuPDF
    except Exception as exc:  # pragma: no cover - runtime dependency
        typer.echo(f"Failed to import PyMuPDF (fitz): {exc}", err=True)
        raise typer.Exit(code=1)

    images_dir_path = outputs.out_dir / images_dir
    if not dry_run:
        images_dir_path.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    want = _select_pages(_parse_ranges(pages), doc.page_count)
    image_paths = []
    for page_no in want:
        page = doc.load_page(page_no - 1)
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        out_path = images_dir_path / f"page-{page_no:04d}.{image_format}"
        image_paths.append(str(out_path))
        if dry_run:
            continue
        if not overwrite and out_path.exists():
            typer.echo(f"Refusing to overwrite existing file: {out_path}", err=True)
            raise typer.Exit(code=1)
        if image_format in {"jpg", "jpeg", "webp"}:
            pix.save(str(out_path), output=image_format, quality=quality)
        else:
            pix.save(str(out_path), output=image_format)

    manifest_path = outputs.out_dir / images_manifest
    if dry_run:
        typer.echo(f"[dry-run] Would write {manifest_path}")
    else:
        _ensure_overwrite([manifest_path], overwrite)
        manifest_path.write_text(json.dumps(image_paths, ensure_ascii=True, indent=2))
        typer.echo(f"Wrote {manifest_path}")
        typer.echo(f"Rasterized {len(image_paths)} pages to {images_dir_path}")

    manifest_payload = _manifest_base(pdf_path, copied_path)
    manifest_payload.update(
        {
            "command": "rasterize",
            "pages": want,
            "dpi": dpi,
            "format": image_format,
            "quality": quality,
            "images_dir": str(images_dir_path),
            "images_manifest": str(manifest_path),
        }
    )
    _write_manifest(outputs.manifest_path, manifest_payload, overwrite, dry_run)


@app.command()
def inspect(
    pdf_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o"),
    project_root: Optional[Path] = typer.Option(None, "--project-root"),
    manifest: str = typer.Option("manifest.json", "--manifest"),
    no_manifest: bool = typer.Option(False, "--no-manifest"),
    overwrite: bool = typer.Option(False, "--overwrite/--no-overwrite"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Inspect PDF metadata and page info."""
    outputs = _output_paths(pdf_path, out_dir, project_root, manifest)

    try:
        import fitz  # PyMuPDF
    except Exception as exc:  # pragma: no cover - runtime dependency
        typer.echo(f"Failed to import PyMuPDF (fitz): {exc}", err=True)
        raise typer.Exit(code=1)

    doc = fitz.open(str(pdf_path))
    page_count = doc.page_count
    sizes = []
    for idx in range(min(3, page_count)):
        rect = doc.load_page(idx).rect
        sizes.append({"page": idx + 1, "width": rect.width, "height": rect.height})

    payload = _manifest_base(pdf_path, None)
    payload.update(
        {
            "command": "inspect",
            "page_count": page_count,
            "page_sizes": sizes,
            "metadata": doc.metadata,
        }
    )

    typer.echo(json.dumps(payload, ensure_ascii=True, indent=2))
    if no_manifest:
        return
    _write_manifest(outputs.manifest_path, payload, overwrite, dry_run)


@app.command()
def clean(
    pdf_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o"),
    project_root: Optional[Path] = typer.Option(None, "--project-root"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Remove the artifacts directory for a PDF."""
    resolved = _resolve_out_dir(pdf_path, out_dir, project_root)
    if dry_run:
        typer.echo(f"[dry-run] Would remove {resolved}")
        return
    if resolved.exists():
        shutil.rmtree(resolved)
        typer.echo(f"Removed {resolved}")
    else:
        typer.echo(f"No artifacts found at {resolved}")


if __name__ == "__main__":
    app()
