from fastapi.testclient import TestClient

from pulse.main import app  # Import your FastAPI app

client = TestClient(app)


def test_url_verification():
    response = client.post("/event", json={"type": "url_verification", "challenge": "testchallenge123"})
    assert response.status_code == 200
    assert response.json() == {"challenge": "testchallenge123"}


def test_reaction_added():
    response = client.post("/event", json={"type": "reaction_added", "event": {"type": "reaction_added"}})
    assert response.status_code == 200
    # Add assertions for your logic


def test_app_mention():
    response = client.post("/event", json={"type": "app_mention", "event": {"type": "app_mention"}})
    assert response.status_code == 200
    # Add assertions for your logic


def test_unsupported_event():
    response = client.post(
        "/event",
        json={"type": "unsupported_event", "event": {"type": "unsupported_event"}},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported slack event type"}
