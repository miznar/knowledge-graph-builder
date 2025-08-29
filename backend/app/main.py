from fastapi import FastAPI
from app.routers import pdf_router

app = FastAPI(title="PDF Ingestion API", version="1.0.0")

# Register routers
app.include_router(pdf_router.router, prefix="/pdf", tags=["PDF"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "PDF Ingestion API running"}
