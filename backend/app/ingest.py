import os
import PyPDF2
from .database import get_collection
from .embeddings import embed_texts
from .config import PDF_FOLDER

# -------- Utility to split text into chunks --------
def chunk_text(text, chunk_size=1000, overlap=100):
    """
    Splits text into chunks with some overlap for better context.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# -------- PDF Text Extraction --------
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# -------- Ingest All PDFs --------
def ingest_pdfs():
    collection = get_collection()
    for filename in os.listdir(PDF_FOLDER):
        if filename.endswith(".pdf"):
            file_path = os.path.join(PDF_FOLDER, filename)
            text = extract_text_from_pdf(file_path)
            if text.strip():
                chunks = chunk_text(text)
                embeddings = embed_texts(chunks)
                collection.add(
                    documents=chunks,
                    embeddings=embeddings,
                    ids=[f"{filename}_{i}" for i in range(len(chunks))]
                )
    return {"status": "success", "message": "PDFs ingested with chunking"}

# -------- Ingest Single PDF --------
def ingest_single_pdf(file_path):
    collection = get_collection()
    print(collection.count())
    text = extract_text_from_pdf(file_path)
    if text.strip():
        chunks = chunk_text(text)
        embeddings = embed_texts(chunks)
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"{os.path.basename(file_path)}_{i}" for i in range(len(chunks))]
        )
        return {"message": f"✅ Ingested {os.path.basename(file_path)} in {len(chunks)} chunks"}
    return {"message": "⚠️ No text found in PDF"}
