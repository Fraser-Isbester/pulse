import time
import os
from dotenv import load_dotenv

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from fastapi import FastAPI, Request, Form, HTTPException

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = FastAPI()
client = WebClient(token=SLACK_BOT_TOKEN)

@app.get("/")
async def read_resource():
    return {"status", "ok"}

@app.post('/slack/test')
async def test_command(response_url: str = Form(...), user_id: str = Form(...), channel_id: str = Form(...)):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text="Hello from your app 1! :tada:"
        )
    except SlackApiError as e:
        raise HTTPException(status_code=400, detail="Slack API Error")
    
    # return {
    #     "response_type": "in_channel",
    #     "text": "Hello from your app 2! :tada:"
    # }

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
