import pytest
from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from pulse.routers.slack import event
from pulse.services.slack import EventWrapperTypes

# Setup FastAPI test client
from pulse.main import app
client = TestClient(app)

# Sample payloads for testing
url_verification_payload = {
    "type": EventWrapperTypes.URL_VERIFICATION.value,
    "challenge": "test_challenge"
}

@pytest.mark.asyncio
async def test_url_verification_event():
    # Mocking the Request object to return the URL verification payload
    with patch("pulse.routers.slack.Request") as mock_request:
        mock_request.json = AsyncMock(return_value=url_verification_payload)
        response = await event(mock_request)
        assert response == {"challenge": "test_challenge"}
