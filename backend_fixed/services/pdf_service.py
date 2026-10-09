import pymupdf


def extract_text_from_pdf(filepath: str) -> str:
    """Extract text from a PDF file using PyMuPDF.

    Returns the extracted text string, or raises an exception on failure.
    """
    doc = None
    try:
        doc = pymupdf.open(filepath)
        pages_text = []
        for page in doc:
            pages_text.append(page.get_text())
        full_text = "\n".join(pages_text).strip()
        return full_text
    finally:
        if doc is not None:
            doc.close()