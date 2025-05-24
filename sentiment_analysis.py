import os
import requests
from typing import Optional

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HEADERS = {"Authorization": f"Bearer {os.environ.get('HF_API_KEY')}"}

def analyze_sentiment(text: str) -> str:
    """Analyzes text sentiment using Hugging Face API"""
    if not text.strip():
        return "neutral"
    
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": text[:512]}  # Truncate to 512 tokens
        )
        response.raise_for_status()
        return response.json()[0][0]['label'].lower()
    except Exception as e:
        print(f"Sentiment error: {e}")
        return "neutral"