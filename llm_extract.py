# llm_extract.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("⚠️ Hugging Face token not found. Add HF_TOKEN=... in your .env file.")

# Using a free keyphrase extraction model from Hugging Face
API_URL = "https://router.huggingface.co/hf-inference/models/ml6team/keyphrase-extraction-distilbert-inspec"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def extract_concepts_with_llm(text: str):
    """
    Extracts key phrases (concepts) from text using the Hugging Face model.
    Returns a dictionary with 'nodes' (concepts) and 'edges' (simple sequential links).
    """
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()

    # --- New, more flexible parsing ---
    keywords = []
    if isinstance(data, list):
        # Model returns a list of dicts (current API format)
        keywords = [item["word"] for item in data]
    elif isinstance(data, dict) and "error" not in data:
        # Older response format
        keywords = [item["word"] for item in data.get("0", [])]
    else:
        print("⚠️ Unexpected response structure:", data)
        return {"nodes": [], "edges": []}

    # Remove duplicates while keeping order
    seen = set()
    keywords = [k for k in keywords if not (k in seen or seen.add(k))]

    # Build simple relationships
    edges = [[keywords[i], keywords[i + 1]] for i in range(len(keywords) - 1)]

    return {"nodes": keywords, "edges": edges}
