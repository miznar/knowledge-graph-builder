import requests
from .database import get_collection
from .embeddings import embed_texts

OLLAMA_API = "http://localhost:11434/api/generate"

def generate_with_ollama(prompt: str, model: str = "gemma:2b-instruct-q4_0") -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=payload)
    response.raise_for_status()
    return response.json()["response"]


def semantic_search(query, top_k=3, model="gemma:2b-instruct-q4_0"):
    collection = get_collection()
    print(f"Total docs in collection: {collection.count()}")
    
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding], 
        n_results=top_k
    )
    print("Query:", query)
    print("Retrieved Docs:", results)

    if not results["documents"] or not results["documents"][0]:
        return {"answer": "No relevant information found.", "chunks": []}

    retrieved_chunks = results["documents"][0]
    context = "\n\n".join(retrieved_chunks)

    # Improved prompt template
    prompt = f"""
    You are a helpful assistant.
    Use the following context to answer the question as clearly and usefully as possible. 

    Guidelines:
    - Prefer the provided context, but if the connection is not exact, try to infer and explain logically. 
    - If the answer is partially in the context, expand it with helpful reasoning.
    - Do not just say "context does not provide info" if something related exists.

    Context:
    {context}

    Question: {query}

    Answer:
    """

    answer = generate_with_ollama(prompt, model=model)

    return {
        "answer": answer.strip(),
        "chunks": [
            {"chunk": doc, "score": float(score)}
            for doc, score in zip(results["documents"][0], results["distances"][0])
        ]
    }
