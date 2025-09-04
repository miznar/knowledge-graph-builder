import chromadb
from .config import CHROMA_DB_PATH

def get_chroma_client():
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)

def get_collection(name="documents"):
    client = get_chroma_client()
    return client.get_or_create_collection(name=name)
