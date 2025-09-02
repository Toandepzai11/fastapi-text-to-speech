## Features
- Generate speech from text (supports multiple voices & vibes).
- Save audio as MP3.
- Upload automatically to **Supabase Storage**.
- Returns a **public streaming URL**.
- Supports both **direct text input** and **.txt file upload**.
## Installation
1. **Create a virtual environment**
```python
python -m venv venv
```
2. **Activate the virtual environment**
- Windows:  
```venv\Scripts\activate```
- Linux/MacOS:  
```source venv/bin/activate```
3. **Dependencies**
```pip install -r requirements.txt```

## Set up environment variables

Create a .env file in the root directory:
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key
SUPABASE_BUCKET=audio-files
```

## Start the API
```bash
uvicorn app.main:app --reload
```
By default, the API runs at http://127.0.0.1:8000 or http://127.0.0.1:8000/docs for docs