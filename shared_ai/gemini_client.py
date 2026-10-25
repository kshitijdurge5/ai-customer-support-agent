"""Optional Gemini API helper for portfolio projects.

Set GEMINI_API_KEY in the local .env file before calling generate_text().
Never commit .env or expose the key in logs, screenshots, or source control.
"""
from __future__ import annotations

import os
from typing import Optional


def generate_text(prompt: str, model: Optional[str] = None) -> str:
    """Generate text with Gemini. Requires GEMINI_API_KEY and google-genai."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Gemini API key is not configured. Add GEMINI_API_KEY to your local .env file when ready."
        )
    if not prompt or not prompt.strip():
        raise ValueError("prompt must not be empty")

    from google import genai

    client = genai.Client(api_key=api_key)
    model_name = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(model=model_name, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned no text. Check model availability and API limits.")
    return text
