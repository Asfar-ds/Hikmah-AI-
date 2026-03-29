
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import shutil
from starlette.responses import FileResponse

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

router = APIRouter()

class TextToSpeechRequest(BaseModel):
    text: str

@router.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Transcribes audio to text using OpenAI's Whisper model.
    """
    if not file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an audio file.")

    # Use a temporary file to store the uploaded audio
    file_path = f"temp_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return {"transcription": transcription.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/text-to-speech")
async def text_to_speech(request: TextToSpeechRequest):
    """
    Synthesizes speech from text using OpenAI's TTS model.
    """
    speech_file_path = "speech.mp3"
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=request.text
        )

        response.stream_to_file(speech_file_path)

        return FileResponse(speech_file_path, media_type="audio/mpeg", filename="speech.mp3")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Note: The speech.mp3 file is not automatically cleaned up after sending.
    # For a production application, you might want to implement a cleanup mechanism.
