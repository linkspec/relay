from fastapi import FastAPI
from pydantic import BaseModel
import services.llm

app = FastAPI()

class VoiceRequest(BaseModel):
    text: str



@app.post("/voice")
async def voice(request: VoiceRequest):

    print(request.text)

    return {
        "success": True,
        "spoken": f"You said '{request.text}'"
    }