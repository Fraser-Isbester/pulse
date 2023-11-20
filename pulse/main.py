import time

from fastapi import FastAPI, Request

from pulse.routers import slack_v1

app = FastAPI()

# Routes
app.include_router(slack_v1, prefix="/slack/v1", tags=["slack"])


## HealthChecks & MiddleWare ##
@app.get("/")
async def healthcheck():
    return {"status", "ok"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Used with the /test slash command, can remove later
# @app.post("/slack/test")
# async def test_command(
#     response_url: str = Form(...), user_id: str = Form(...), channel_id: str = Form(...)
# ):
#     print(response_url, user_id, channel_id)

#     try:
#         response = client.chat_postMessage(
#             channel=channel_id, text="Hello from your app 1! :tada:"
#         )
#         print(response)
#         return {"status": "accepted"}
#     except SlackApiError:
#         raise HTTPException(status_code=400, detail="Slack API Error")
