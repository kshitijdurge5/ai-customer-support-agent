"""Provider-neutral LLM adapter. Requires an OpenAI-compatible endpoint and explicit config."""
import os
from openai import OpenAI

class LLMConfigError(RuntimeError):
    pass

def get_client():
    key = os.getenv("LLM_API_KEY", "").strip()
    base_url = os.getenv("LLM_BASE_URL", "").strip() or None
    if not key:
        raise LLMConfigError("Set LLM_API_KEY in your local .env file first.")
    return OpenAI(api_key=key, base_url=base_url)

def chat(messages, *, model=None, temperature=0.2):
    client = get_client()
    model_name = model or os.getenv("LLM_MODEL", "").strip()
    if not model_name:
        raise LLMConfigError("Set LLM_MODEL in your local .env file first.")
    response = client.chat.completions.create(
        model=model_name, messages=messages, temperature=temperature
    )
    return response.choices[0].message.content or ""
