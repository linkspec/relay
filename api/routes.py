@app.post("/voice")
async def voice(request: VoiceRequest):

    response = assistant.handle(request.text)

    return response