from fastapi import FastAPI
from pydantic import BaseModel
import logger

from services.llm import LLMService


app = FastAPI()

llm = LLMService()


class VoiceRequest(BaseModel):
    text: str


class VoiceResponse(BaseModel):
    response: str


@app.post("/voice", response_model=VoiceResponse)
async def voice(request: VoiceRequest):
    logger.info("Received voice request")
    reply = llm.chat([
        {
            "role": "user",
            "content": request.text,
        }
    ])
    logger.info("Sending response")
    return VoiceResponse(
        response=reply
    )