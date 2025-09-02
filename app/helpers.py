import json
from typing import List
from app.config import VOICE_FILE, VIBE_FILE, DEFAULT_VIBE_PROMPT

def load_voices() -> List[str]:
    """Load available voices from the voices.json file."""
    try:
        with open(VOICE_FILE) as f:
            return json.load(f)["voices"]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def load_vibes() -> dict:
    """Load available vibes from the vibes.json file."""
    try:
        with open(VIBE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def format_vibe_prompt(vibe_name: str, vibes_data: dict) -> str:
    """Format vibe prompt based on selected vibe."""
    vibe_content = vibes_data.get(vibe_name)
    if vibe_content:
        return "\n\n".join(vibe_content)
    return DEFAULT_VIBE_PROMPT

def split_text_into_chunks(text: str, max_chunk_size: int = 999) -> List[str]:
    """Split the text into chunks to avoid hitting API limits (e.g., 1000 chars max)."""
    chunks = []
    for i in range(0, len(text), max_chunk_size):
        chunks.append(text[i:i + max_chunk_size])
    return chunks
