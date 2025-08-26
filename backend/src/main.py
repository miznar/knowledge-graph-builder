from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import uvicorn
import os
import time

app = FastAPI(
    title="Knowledge Graph Builder API",
    description="🚀 Backend for document ingestion & graph building",
    version="0.1.0",
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE_MB = 50


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate extension
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported.")

    # Validate file size
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File too large. Max 50MB allowed.")
    
    # Save file
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(contents)

    # Extract text
    text = ""
    num_pages = 0
    try:
        if file.filename.endswith(".pdf"):
            doc = fitz.open(filepath)
            num_pages = doc.page_count
            for page in doc:
                text += page.get_text()
        elif file.filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

    # Metadata
    word_count = len(text.split())
    preview = text[:1000] if len(text) > 1000 else text

    # Logging
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Uploaded {file.filename} ({round(size_mb,2)} MB)")

    return {
        "filename": file.filename,
        "size_mb": round(size_mb, 2),
        "pages": num_pages if num_pages > 0 else None,
        "words": word_count,
        "preview": preview,
        "status": "success"
    }


@app.get("/")
def root():
    return {"message": "Knowledge Graph Builder API is running 🚀"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
