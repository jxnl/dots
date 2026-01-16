#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _resolve_out_dir(pdf_path: Path, out_dir: Optional[Path]) -> Path:
    if out_dir is None:
        out_dir = Path.cwd() / ".pdf-artifacts" / pdf_path.stem
    else:
        out_dir = Path(out_dir)
        if not out_dir.is_absolute():
            out_dir = Path.cwd() / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


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


@app.command()
def ocr(
    pdf_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o"),
    copy_pdf: bool = typer.Option(True, "--copy-pdf/--no-copy-pdf"),
    pages_json: str = typer.Option("ocr-pages.json", "--pages-json"),
    pages_text: str = typer.Option("ocr-pages.txt", "--pages-text"),
) -> None:
    """OCR a PDF with docling and save per-page text."""
    out_dir = _resolve_out_dir(pdf_path, out_dir)
    if copy_pdf:
        _copy_pdf(pdf_path, out_dir)

    try:
        from docling.document_converter import DocumentConverter
    except Exception as exc:  # pragma: no cover - runtime dependency
        typer.echo(f"Failed to import docling: {exc}", err=True)
        raise typer.Exit(code=1)

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    document = result.document

    pages = getattr(document, "pages", None)
    page_entries = []
    if pages:
        for idx, page in enumerate(pages, start=1):
            page_no = getattr(page, "page_number", idx)
            page_entries.append({"page": int(page_no), "text": _page_text(page)})
    else:
        if hasattr(document, "export_to_text"):
            text = document.export_to_text()
        else:
            text = str(document)
        page_entries.append({"page": 1, "text": text})

    json_path = out_dir / pages_json
    json_path.write_text(json.dumps(page_entries, ensure_ascii=True, indent=2))

    text_path = out_dir / pages_text
    parts = []
    for entry in page_entries:
        parts.append(f"=== Page {entry['page']} ===\n{entry['text']}")
    text_path.write_text("\n\n".join(parts), encoding="utf-8")

    typer.echo(f"Wrote {json_path}")
    typer.echo(f"Wrote {text_path}")


@app.command()
def rasterize(
    pdf_path: Path = typer.Argument(..., exists=True, dir_okay=False, readable=True),
    out_dir: Optional[Path] = typer.Option(None, "--out-dir", "-o"),
    copy_pdf: bool = typer.Option(True, "--copy-pdf/--no-copy-pdf"),
    dpi: int = typer.Option(200, "--dpi"),
    images_dir: str = typer.Option("images", "--images-dir"),
    images_manifest: str = typer.Option("images.json", "--images-manifest"),
) -> None:
    """Rasterize a PDF to JPEG images using PyMuPDF."""
    out_dir = _resolve_out_dir(pdf_path, out_dir)
    if copy_pdf:
        _copy_pdf(pdf_path, out_dir)

    try:
        import fitz  # PyMuPDF
    except Exception as exc:  # pragma: no cover - runtime dependency
        typer.echo(f"Failed to import PyMuPDF (fitz): {exc}", err=True)
        raise typer.Exit(code=1)

    images_dir_path = out_dir / images_dir
    images_dir_path.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(str(pdf_path))
    image_paths = []
    for idx in range(doc.page_count):
        page = doc.load_page(idx)
        pix = page.get_pixmap(dpi=dpi, alpha=False)
        out_path = images_dir_path / f"page-{idx + 1:04d}.jpg"
        pix.save(str(out_path))
        image_paths.append(str(out_path))

    manifest_path = out_dir / images_manifest
    manifest_path.write_text(json.dumps(image_paths, ensure_ascii=True, indent=2))

    typer.echo(f"Wrote {manifest_path}")
    typer.echo(f"Rasterized {len(image_paths)} pages to {images_dir_path}")


if __name__ == "__main__":
    app()
