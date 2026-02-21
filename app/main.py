from fastapi import FastAPI, Header, BackgroundTasks, HTTPException
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

@app.get("/exports/watermark")
def get_watermark(x_consumer_id: str = Header(...)):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT last_exported_at FROM watermarks WHERE consumer_id=%s",
        (x_consumer_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="No watermark found")

    return {
        "consumerId": x_consumer_id,
        "lastExportedAt": row["last_exported_at"]
    }