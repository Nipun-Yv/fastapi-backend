from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from services.MapInfoBot import MapInfoBot
from services.promptsSpace import system_instruction,tools
from pydantic import BaseModel
import openai
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = openai.OpenAI(api_key=OPENAI_KEY)

# @app.post("/transcribe/")
# async def transcribe_audio(file: UploadFile = File(...)):
#     if file.content_type not in ["audio/webm", "audio/m4a", "audio/mp3"]:
#         return {"error": "Unsupported file type"}

#     audio_bytes = await file.read()
#     transcript = client.audio.transcriptions.create(
#         model="whisper-1",
#         file=(file.filename, audio_bytes, file.content_type)
#     )
#     print(transcript.text)
#     return {"transcription": transcript.text}

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    if file.content_type not in ["audio/webm", "audio/m4a", "audio/mp3"]:
        return {"error": "Unsupported file type"}

    audio_bytes = await file.read()
    audio_file = BytesIO(audio_bytes)
    audio_file.name = file.filename  # Required by the OpenAI SDK

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="en"
    )
    return {"transcription": transcript.text}

class Item(BaseModel):
    text: str

@app.post("/get-coordinates")
async def location_coordinates(item: Item):
    conversation_id = item.conversation_id or "default"
    map_bot = MapInfoBot.get_instance(
        conversation_id=conversation_id,
        tools=tools,
        instruction=system_instruction,
        model_name="gemini-2.0-flash"
    )
    
    result = await map_bot.send_message(item.text)
    print(result)
    
    if isinstance(result, str):
        return {"message": result, "result": None}
    return {"message": None, "result": result}

@app.get("/api/hello")
async def read_root():
    return {"message": 23}
