from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, Request
from datetime import datetime
import uuid
from app.database import get_db
from app.exports import run_export

app = FastAPI()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/exports/full")
def full_export(background_tasks: BackgroundTasks, x_consumer_id: str = Header(...)):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(run_export, x_consumer_id, "full", job_id)
    return {
        "jobId": job_id,
        "status": "started",
        "exportType": "full",
        "outputFilename": f"full_{x_consumer_id}_{job_id}.csv"
    }

@app.post("/exports/incremental")
def incremental_export(background_tasks: BackgroundTasks, x_consumer_id: str = Header(...)):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(run_export, x_consumer_id, "incremental", job_id)
    return {
        "jobId": job_id,
        "status": "started",
        "exportType": "incremental",
        "outputFilename": f"incremental_{x_consumer_id}_{job_id}.csv"
    }

@app.post("/exports/delta")
def delta_export(background_tasks: BackgroundTasks, x_consumer_id: str = Header(...)):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(run_export, x_consumer_id, "delta", job_id)
    return {
        "jobId": job_id,
        "status": "started",
        "exportType": "delta",
        "outputFilename": f"delta_{x_consumer_id}_{job_id}.csv"
    }

from fastapi import Request

@app.get("/exports/watermark")
def get_watermark(request: Request):
    consumer_id = request.headers.get("X-Consumer-ID")

    if not consumer_id:
        raise HTTPException(status_code=400, detail="X-Consumer-ID required")

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT last_exported_at FROM watermarks WHERE consumer_id=%s",
        (consumer_id,)
    )

    row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Watermark not found")

    last = row[0] if isinstance(row, tuple) else row["last_exported_at"]

    return {
        "consumerId": consumer_id,
        "lastExportedAt": last.isoformat() if last else None
    }