from pydantic import BaseModel
from typing import Optional

class AudioRequest(BaseModel):
    text: str
    voice: str
    vibe: Optional[str] = None  # Optional vibe parameter
