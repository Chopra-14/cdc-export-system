from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_export_start():
    response = client.post(
        "/exports/full",
        headers={"X-Consumer-ID": "consumer-test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["exportType"] == "full"
    assert data["status"] == "started"
    assert "jobId" in data

def test_incremental_export_start():
    response = client.post(
        "/exports/incremental",
        headers={"X-Consumer-ID": "consumer-test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["exportType"] == "incremental"

def test_delta_export_start():
    response = client.post(
        "/exports/delta",
        headers={"X-Consumer-ID": "consumer-test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["exportType"] == "delta"