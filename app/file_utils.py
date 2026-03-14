import re
from io import BytesIO
from pypdf import PdfReader


def clean_extracted_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"\s+([,.;:!?])", r"\1", text)

    return text.strip()


def extract_text_from_txt(file_bytes: bytes) -> str:
    raw_text = file_bytes.decode("utf-8", errors="ignore")
    return clean_extracted_text(raw_text)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_stream = BytesIO(file_bytes)
    reader = PdfReader(pdf_stream)

    extracted_text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text.append(page_text)

    raw_text = "\n".join(extracted_text)
    return clean_extracted_text(raw_text)


def extract_text_from_file(filename: str, file_bytes: bytes) -> tuple[str, str]:
    lower_name = filename.lower()

    if lower_name.endswith(".txt"):
        return extract_text_from_txt(file_bytes), "txt"

    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes), "pdf"

    raise ValueError("Unsupported file type. Please upload a .txt or .pdf file.")