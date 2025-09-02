import datetime
import json
import requests
from typing import Optional

from app.config import API_URL, API_BOUNDARY
from app.helpers import format_vibe_prompt, split_text_into_chunks

# Global API Headers
API_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Content-Type": f"multipart/form-data; boundary={API_BOUNDARY}",
    "Accept": "*/*",
    "Origin": "https://www.openai.fm",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i"
}

def generate_filename() -> str:
    """Generate a filename with a timestamp for the audio file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"output_{timestamp}.wav"

def send_request(text: str, voice: str, vibe_prompt: str) -> Optional[bytes]:
    """Send the request to the TTS API."""
    data = []
    for name, value in [
        ("input", text),
        ("prompt", vibe_prompt),
        ("voice", voice.lower()),
        ("vibe", "null")
    ]:
        data.append(f"--{API_BOUNDARY}")
        data.append(f'Content-Disposition: form-data; name="{name}"\r\n')
        data.append(value)
    data.append(f"--{API_BOUNDARY}--")
    body = "\r\n".join(data).encode('utf-8')

    try:
        response = requests.post(API_URL, headers=API_HEADERS, data=body)

        if response.status_code == 200 and "audio/wav" in response.headers["Content-Type"]:
            return response.content  # Return the audio content
        else:
            print(f"API returned an error: {response.text}")
            return None
    except Exception as e:
        print(f"Error during API request: {e}")
        return None

def generate_audio_from_text(text: str, voice: str, vibe: str, vibes_data: dict) -> Optional[bytes]:
    """Generate the audio from text using the TTS API."""
    vibe_prompt = format_vibe_prompt(vibe, vibes_data)
    chunks = split_text_into_chunks(text)

    combined_audio = b""
    for chunk in chunks:
        audio = send_request(chunk, voice, vibe_prompt)
        if audio:
            combined_audio += audio

    return combined_audio
