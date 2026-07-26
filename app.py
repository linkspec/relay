from fastapi import FastAPI
from pydantic import BaseModel

from services.llm import LLMService


app = FastAPI()

llm = LLMService()


class VoiceRequest(BaseModel):
    text: str


class VoiceResponse(BaseModel):
    response: str


@app.post("/voice", response_model=VoiceResponse)
async def voice(request: VoiceRequest):
    reply = llm.chat([
        {
            "role": "user",
            "content": request.text,
        }
    ])

    return VoiceResponse(
        response=reply
    )