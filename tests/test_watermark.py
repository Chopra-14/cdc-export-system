from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_watermark_not_found():
    response = client.get(
        "/exports/watermark",
        headers={"X-Consumer-ID": "new-consumer"}
    )
    assert response.status_code == 404