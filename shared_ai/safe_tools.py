"""Minimal allowlisted tools; never execute arbitrary model-generated Python or shell."""
from datetime import datetime, timezone

def current_utc_time():
    return datetime.now(timezone.utc).isoformat()

def count_words(text: str) -> int:
    return len(text.split())

ALLOWED_TOOLS = {"count_words": count_words, "current_utc_time": current_utc_time}

def call_tool(name: str, arguments: dict):
    if name not in ALLOWED_TOOLS:
        raise ValueError(f"Tool not allowed: {name}")
    if name == "count_words":
        text = arguments.get("text")
        if not isinstance(text, str) or len(text) > 20000:
            raise ValueError("text must be a string up to 20,000 characters")
        return ALLOWED_TOOLS[name](text)
    if arguments:
        raise ValueError("This tool accepts no arguments")
    return ALLOWED_TOOLS[name]()
