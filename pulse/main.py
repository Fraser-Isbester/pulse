import time
import os
from dotenv import load_dotenv

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form, HTTPException

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
from fastapi import FastAPI, Request
from pulse import chat

app = FastAPI()
client = WebClient(token=SLACK_BOT_TOKEN)

class SlackEventRequest(BaseModel):
    token: str
    challenge: str = None
    type: str
    team_id: str
    api_app_id: str
    event: dict
    event_id: str
    event_time: int

processed_events = set()

@app.get("/")
async def healthcheck():
    return {"status", "ok"}

# Used with the /test slash command, can remove later
@app.post('/slack/test')
async def test_command(response_url: str = Form(...), user_id: str = Form(...), channel_id: str = Form(...)):
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text="Hello from your app 1! :tada:"
        )
        return {"status": "accepted"}
    except SlackApiError:
        raise HTTPException(status_code=400, detail="Slack API Error")

@app.post('/slack/ask')
async def ask_command(event_request: SlackEventRequest):
    # Check if it's the challenge event
    if event_request.type == "url_verification" and event_request.challenge:
        return {"challenge": event_request.challenge}

    print("Received event: " + event_request.type + ", " + event_request.event_id)

    # Idempotency to prevent processing duplicate events from retries
    # likely a nicer way to do this (something something redis? or debounce on time)
    event_id = event_request.event_id
    if event_id in processed_events:
        print("Not processing duplicate event: " + event_id)
        return {"status": "already processed"}

    event = event_request.event
    event_type = event.get("type")

    if event_type == "reaction_added":
        reaction = event.get("reaction")

        if reaction == "eyes":
            item = event.get("item")
            channel_id = item.get("channel")
            message_ts = item.get("ts")
            processed_events.add(event_id)

            try:
                join_response = client.conversations_join(channel=channel_id)

                if join_response['ok']:
                    # fetch the content for query
                    response = client.conversations_history(
                        channel=channel_id,
                        latest=message_ts,
                        limit=1,
                        inclusive=True
                    )

                    message_content = response['messages'][0]['text'] if response['messages'] else None
                    if not message_content:
                        return {"error": "no message content"}
                    chat_response = chat()(message_content)
                    response = client.chat_postMessage(
                        channel=channel_id,
                        text=chat_response.get("result"),
                        thread_ts=message_ts
                    )
            except Exception as e:
                print(e)
                processed_events.remove(event_id)
                raise HTTPException(status_code=400, detail="error")

            return {"status": "accepted"}

    return {"status": "received"}

@app.get("/query")
async def query(q: str = None):
    if not q:
        return {"error": "missing query"}
    return chat()(q)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
