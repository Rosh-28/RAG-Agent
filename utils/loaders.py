from pypdf import PdfReader
import io

def load_txt(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")

def load_pdf(file_bytes: bytes) -> str:
    pdf_stream = io.BytesIO(file_bytes) 
    reader = PdfReader(pdf_stream)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text
