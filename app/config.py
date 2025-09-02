import os

# Path to voices and vibes data files
VOICE_FILE = "voices.json"
VIBE_FILE = "vibes.json"

# URL for the TTS API
API_URL = "https://www.openai.fm/api/generate"
API_BOUNDARY = "----WebKitFormBoundary12345"

# Default vibe prompt for fallback
DEFAULT_VIBE_PROMPT = """Voice Affect: Calm, composed, and reassuring; project quiet authority and confidence.
Tone: Sincere, empathetic, and gently authoritative—express genuine apology while conveying competence.
Pacing: Steady and moderate; unhurried enough to communicate care, yet efficient enough to demonstrate professionalism.
Emotion: Genuine empathy and understanding; speak with warmth, especially during apologies ("I'm very sorry for any disruption...").
Pronunciation: Clear and precise, emphasizing key reassurances ("smoothly," "quickly," "promptly") to reinforce confidence.
Pauses: Brief pauses after offering assistance or requesting details, highlighting willingness to listen and support."""
