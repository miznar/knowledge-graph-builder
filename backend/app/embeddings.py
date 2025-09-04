from sentence_transformers import SentenceTransformer

# Local open-source embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_texts(texts):
    return model.encode(texts, convert_to_numpy=True).tolist()
