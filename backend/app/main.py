from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .ingest import ingest_pdfs
from .search import semantic_search
from .schemas import QueryRequest
from fastapi import UploadFile, File
import os
from .config import PDF_FOLDER
from .ingest import ingest_single_pdf

from .knowledge_graph import build_knowledge_graph
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
import spacy
nlp = spacy.load("en_core_web_sm")

#  Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    # Ensure the folder exists
    os.makedirs(PDF_FOLDER, exist_ok=True)

    file_path = os.path.join(PDF_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1. Ingest PDF into vector DB (your RAG pipeline)
    ingest_result = ingest_single_pdf(file_path)

    # 2. Generate Knowledge Graph (call from separate file)
    graph_path = build_knowledge_graph(file_path)  # returns HTML file path

    return {
        "message": "PDF ingested and knowledge graph generated successfully",
        "ingestion": ingest_result,
        "knowledge_graph": graph_path
    }
from fastapi.responses import FileResponse

import os

@app.get("/graph")
async def get_graph():
    graph_path = os.path.join("app", "static", "graphs", "graph.html")
    return FileResponse(graph_path, media_type="text/html")


@app.post("/search")
def search(request: QueryRequest):
    return semantic_search(request.query, request.top_k)

@app.get("/knowledge-graph")
def generate_graph():
    return build_knowledge_graph()