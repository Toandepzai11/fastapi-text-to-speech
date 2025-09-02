import os
import uuid
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from app.helpers import load_voices, load_vibes
from app.models import AudioRequest
from app.tts import generate_audio_from_text
from app.supabase_client import supabase

app = FastAPI()

voices = load_voices()
vibes_data = load_vibes()

async def extract_text_from_file(file: UploadFile) -> str:
    content = await file.read()
    return content.decode("utf-8")

# folder which stores generated audio files (use when not using Supabase)
# AUDIO_DIR = "generated_audio_files"
# os.makedirs(AUDIO_DIR, exist_ok=True)

BUCKET = os.getenv("SUPABASE_BUCKET", "audio-files")

async def generate_and_upload_audio(text: str, voice: str, vibe: str) -> dict:
    if (voice not in voices) or (vibe and vibe not in vibes_data):
        raise HTTPException(status_code=400, detail="Invalid voice or vibe selected.")

    audio = generate_audio_from_text(text, voice, vibe or "Calm", vibes_data)
    if not audio:
        raise HTTPException(status_code=500, detail="No audio generated.")
    
    audio_filename = f"{uuid.uuid4()}.wav"
    # audio_path = os.path.join(AUDIO_DIR, audio_filename)
    try:
        # Upload to Supabase bucket
        supabase.storage.from_(BUCKET).upload(audio_filename, audio)
        # Get URL of the file to be public for an hour
        signed_url_response = supabase.storage.from_(BUCKET).create_signed_url(audio_filename, 3600)
        signed_url = signed_url_response.get("signedURL") 
        return {"filename": audio_filename, "url": signed_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

@app.post("/generate-audio-text/")
# if the client send JSON (not form fields), write the code below
# async def generate_audio(request: AudioRequest):
async def generate_audio(request: AudioRequest = Form(...)):
    return await generate_and_upload_audio(request.text, request.voice, request.vibe or "Calm")

# File upload function
@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...), voice: str = Form(...), vibe: str = Form("Calm")):
    try:
        # Extract text from the file
        if not file.filename.endswith(".txt"):
            raise HTTPException(status_code=400, detail="Only .txt files are supported for text extraction.")
        text = await extract_text_from_file(file)        
        return await generate_and_upload_audio(text, voice, vibe)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while uploading the file: {e}")