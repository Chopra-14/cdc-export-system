from fastapi.testclient import TestClient
from app.main import app
import app.exports as exports_module
import app.main as main_module

client = TestClient(app)

def dummy_run_export(*args, **kwargs):
    pass

def patch(monkeypatch):
    monkeypatch.setattr(exports_module, "run_export", dummy_run_export)
    monkeypatch.setattr(main_module, "run_export", dummy_run_export)

def test_full_export_start(monkeypatch):
    patch(monkeypatch)

    response = client.post(
        "/exports/full",
        headers={"X-Consumer-ID": "consumer-test"}
    )

    assert response.status_code == 200
    assert response.json()["exportType"] == "full"

def test_incremental_export_start(monkeypatch):
    patch(monkeypatch)

    response = client.post(
        "/exports/incremental",
        headers={"X-Consumer-ID": "consumer-test"}
    )

    assert response.status_code == 200
    assert response.json()["exportType"] == "incremental"

def test_delta_export_start(monkeypatch):
    patch(monkeypatch)

    response = client.post(
        "/exports/delta",
        headers={"X-Consumer-ID": "consumer-test"}
    )

    assert response.status_code == 200
    assert response.json()["exportType"] == "delta"