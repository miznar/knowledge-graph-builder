from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_loader import extract_text_from_pdf

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        content = extract_text_from_pdf(file.file)
        if not content.strip():
            raise HTTPException(status_code=422, detail="No extractable text found in PDF.")
        return {"filename": file.filename, "content": content[:500]}  # limit preview
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
