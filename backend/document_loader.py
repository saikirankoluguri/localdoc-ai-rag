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

    return {
        "text": full_text.strip(),
        "page_count": page_count,
        "text_length": len(full_text.strip()),
    }