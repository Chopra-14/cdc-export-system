import app.exports as exports
from datetime import datetime


# ---------------- Dummy DB ----------------

class DummyCursor:
    def execute(self, *args, **kwargs):
        pass

    def fetchall(self):
        return [
            {
                "id": 1,
                "name": "Test User",
                "email": "test@test.com",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_deleted": False
            }
        ]

    def fetchone(self):
        # REQUIRED by watermark logic
        return {"last_exported_at": None}

    def close(self):
        pass


class DummyConn:
    def cursor(self, *args, **kwargs):
        return DummyCursor()

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass


def dummy_get_db():
    return DummyConn()


# ---------------- Tests ----------------

def test_run_export_full(monkeypatch):
    monkeypatch.setattr(exports, "get_db", dummy_get_db)

    exports.run_export(
        consumer_id="unit-full",
        export_type="full",
        job_id="job-1"
    )


def test_run_export_incremental(monkeypatch):
    monkeypatch.setattr(exports, "get_db", dummy_get_db)

    exports.run_export(
        consumer_id="unit-incremental",
        export_type="incremental",
        job_id="job-2"
    )


def test_run_export_delta(monkeypatch):
    monkeypatch.setattr(exports, "get_db", dummy_get_db)

    exports.run_export(
        consumer_id="unit-delta",
        export_type="delta",
        job_id="job-3"
    )


def test_run_export_failure(monkeypatch):
    def failing_db():
        raise Exception("DB FAIL")

    monkeypatch.setattr(exports, "get_db", failing_db)

    try:
        exports.run_export(
            consumer_id="fail",
            export_type="full",
            job_id="job-4"
        )
    except:
        pass