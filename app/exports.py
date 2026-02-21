import csv
import os
import logging
from datetime import datetime
from app.database import get_db

def run_export(consumer_id, export_type, job_id):
    logging.info({
        "event": "export_started",
        "jobId": job_id,
        "consumerId": consumer_id,
        "exportType": export_type
    })

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "SELECT last_exported_at FROM watermarks WHERE consumer_id=%s",
            (consumer_id,)
        )
        row = cur.fetchone()
        watermark = row["last_exported_at"] if row else None

        if export_type == "full":
            query = "SELECT * FROM users WHERE is_deleted=false"
            params = ()
        else:
            if not watermark:
                watermark = datetime(1970, 1, 1)
            query = "SELECT * FROM users WHERE updated_at>%s"
            params = (watermark,)

        cur.execute(query, params)
        rows = cur.fetchall()

        filename = f"{export_type}_{consumer_id}_{job_id}.csv"
        path = os.path.join(OUTPUT_DIR, filename)

        max_updated = watermark

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)

            if export_type == "delta":
                writer.writerow(["operation","id","name","email","created_at","updated_at","is_deleted"])
            else:
                writer.writerow(["id","name","email","created_at","updated_at","is_deleted"])

            for r in rows:
                if export_type == "delta":
                    if r["is_deleted"]:
                        op = "DELETE"
                    elif r["created_at"] == r["updated_at"]:
                        op = "INSERT"
                    else:
                        op = "UPDATE"

                    writer.writerow([op,r["id"],r["name"],r["email"],r["created_at"],r["updated_at"],r["is_deleted"]])
                else:
                    writer.writerow([r["id"],r["name"],r["email"],r["created_at"],r["updated_at"],r["is_deleted"]])

                if not max_updated or r["updated_at"] > max_updated:
                    max_updated = r["updated_at"]

        if rows and max_updated:
            cur.execute("""
                INSERT INTO watermarks(consumer_id,last_exported_at,updated_at)
                VALUES(%s,%s,NOW())
                ON CONFLICT (consumer_id)
                DO UPDATE SET last_exported_at=EXCLUDED.last_exported_at, updated_at=NOW()
            """,(consumer_id,max_updated))

        conn.commit()

        logging.info({
            "event": "export_completed",
            "jobId": job_id,
            "consumerId": consumer_id,
            "exportType": export_type,
            "rowsExported": len(rows)
        })

    except Exception as e:
        conn.rollback()
        logging.error({
            "event": "export_failed",
            "jobId": job_id,
            "consumerId": consumer_id,
            "exportType": export_type,
            "error": str(e)
        })

    finally:
        cur.close()
        conn.close()