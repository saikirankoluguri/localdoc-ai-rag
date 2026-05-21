from pathlib import Path
import fitz


def extract_text_from_pdf(file_path: str) -> dict:
    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    document = fitz.open(pdf_path)

    full_text = ""

    for page_number, page in enumerate(document, start=1):
        page_text = page.get_text()
        full_text += f"\n\n--- Page {page_number} ---\n\n"
        full_text += page_text

    page_count = document.page_count
    document.close()

    extracted_dir = Path("data/extracted")
    extracted_dir.mkdir(parents=True, exist_ok=True)

    extracted_file_path = extracted_dir / f"{pdf_path.stem}.txt"
    extracted_file_path.write_text(full_text.strip(), encoding="utf-8")

    return {
        "text": full_text.strip(),
        "page_count": page_count,
        "text_length": len(full_text.strip()),
        "extracted_text_path": str(extracted_file_path),
    }