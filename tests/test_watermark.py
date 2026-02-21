from fastapi.testclient import TestClient
from app.main import app
import app.main as main_module

client = TestClient(app)

class DummyCursor:
    def execute(self, *args, **kwargs):
        pass
    def fetchone(self):
        return None
    def close(self):
        pass

class DummyConn:
    def cursor(self):
        return DummyCursor()
    def close(self):
        pass

def dummy_get_db():
    return DummyConn()

def test_get_watermark_not_found(monkeypatch):
    monkeypatch.setattr(main_module, "get_db", dummy_get_db)

    response = client.get(
        "/exports/watermark",
        headers={"X-Consumer-ID": "new-consumer"}
    )

    assert response.status_code == 404