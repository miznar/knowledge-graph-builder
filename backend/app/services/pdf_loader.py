import PyPDF2
from io import BytesIO

def extract_text_from_pdf(file_obj) -> str:
    """
    Extracts text from PDF using PyPDF2.
    :param file_obj: Uploaded PDF file object
    :return: Extracted text as string
    """
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_obj)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        raise RuntimeError(f"PDF extraction failed: {e}")
    return text
