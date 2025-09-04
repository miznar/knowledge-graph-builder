import requests

OLLAMA_API = "http://localhost:11434/api/generate"  # Ollama default endpoint

def generate_with_ollama(prompt: str, model: str = "gemma:2b-instruct-q4_0") -> str:
    """
    Calls the local Ollama server with a prompt and returns the generated response.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=payload)
    response.raise_for_status()
    return response.json()["response"]
