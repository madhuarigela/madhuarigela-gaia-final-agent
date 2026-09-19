import os
from dotenv import load_dotenv

load_dotenv(override=True)

from smolagents import LiteLLMModel

DEFAULT_MODEL_ID = "groq/qwen/qwen3.8-27b"

def build_model():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is not configured in the Space Secrets.")
    return LiteLLMModel(
        model_id=os.getenv("MODEL_ID", DEFAULT_MODEL_ID),
        api_key=key,
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", "500")),
        temperature=float(os.getenv("MODEL_TEMPERATURE", "0.1")),
    )
