"""Application server logic for Pulse."""

import time

from fastapi import FastAPI, Request

from pulse.routers import slack_v1, confluence_v1

app = FastAPI()

# Slack Routes
app.include_router(slack_v1, prefix="/slack/v1", tags=["slack"])

# Confluence Routes
app.include_router(confluence_v1, prefix="/confluence/v1", tags=["confluence"])


## HealthChecks & MiddleWare ##
@app.get("/healthcheck")
async def healthcheck():
    """server Healthcheck endpoint."""
    return {"status", "ok"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Adds timing info to all HTTP responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
