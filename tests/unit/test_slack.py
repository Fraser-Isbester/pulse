import pytest
from fastapi import HTTPException
from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from pulse.routers.slack import event
from pulse.services.slack import EventWrapperTypes, EventTypes

# Setup FastAPI test client
from pulse.main import app
client = TestClient(app)

@pytest.mark.asyncio
async def test_url_verification_event():
    """Test the URL verification event handler.This is a happy path."""

    url_verification_payload = {
        "type": EventWrapperTypes.URL_VERIFICATION.value,
        "challenge": "test_challenge"
    }

    with patch("pulse.routers.slack.Request") as mock_request:
        mock_request.json = AsyncMock(return_value=url_verification_payload)
        response = await event(mock_request)
        assert response == {"challenge": "test_challenge"}


@pytest.mark.asyncio
async def test_unknown_event_wrapper_type():
    """Tests that an unknown event wrapper type raises an HTTPException"""

    unknown_event_payload = {"type": "unknown_type"}
    with patch("pulse.routers.slack.Request") as mock_request:
        mock_request.json = AsyncMock(return_value=unknown_event_payload)
        with pytest.raises(HTTPException) as exc_info:
            await event(mock_request)
        assert exc_info.value.status_code == 400

@pytest.mark.asyncio
async def test_validation_error_handling():
    """Test that a validation error raises an HTTPException"""
    invalid_payload = {
        "type": EventWrapperTypes.EVENT_CALLBACK.value,
        "foo": "bar"
    }

    with patch("pulse.routers.slack.Request") as mock_request:
        mock_request.json = AsyncMock(return_value=invalid_payload)
        with pytest.raises(HTTPException) as exc_info:
            await event(mock_request)
        assert exc_info.value.status_code == 400
