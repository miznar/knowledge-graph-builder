import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file using PyMuPDF (fitz).
    Returns the text as a single string.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        return f"Error while reading PDF: {e}"

    return text.strip()


# Example usage
if __name__ == "__main__":
    pdf_file = "sample.pdf"   # put your test file path here
    content = extract_text_from_pdf(pdf_file)
    print(content[:500])  # print only first 500 chars for testing
