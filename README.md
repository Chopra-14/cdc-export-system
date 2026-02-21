# CDC Export System

A Dockerized FastAPI application implementing Change Data Capture (CDC) exports with Full, Incremental, and Delta strategies using PostgreSQL.

---

## 🏗 Architecture Overview

- FastAPI backend
- PostgreSQL database
- Docker + docker-compose
- Watermark-based CDC
- Background export jobs
- CSV export output
- Unit + API tests with 74% coverage

---

## 🚀 Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Chopra-14/cdc-export-system.git
cd cdc-export-system
```
### 2️⃣ Run with Docker
```bash
docker-compose up --build
```

## Application runs at:

http://localhost:8080
### 📡 API Endpoints
Health Check
# GET /health

## Response:

{
  "status": "ok",
  "timestamp": "..."
}
Full Export
# POST /exports/full
Header: X-Consumer-ID

Exports all non-deleted records.

Incremental Export
# POST /exports/incremental
Header: X-Consumer-ID

Exports records where:

updated_at > last_exported_at
AND is_deleted = false
Delta Export
# POST /exports/delta
Header: X-Consumer-ID

Adds an operation column:

INSERT → created_at == updated_at

UPDATE → modified rows

DELETE → is_deleted = true

Watermark
GET /exports/watermark
Header: X-Consumer-ID

Returns last exported timestamp per consumer.

### 🔁 CDC Explanation

Change Data Capture (CDC) allows systems to export only changed data instead of full datasets every time.

This system supports:

Full export (complete dataset)

Incremental export (new + updated data)

Delta export (INSERT / UPDATE / DELETE tracking)

This reduces:

Data transfer size

Processing cost

API load

### 💧 Watermark Logic

Each consumer has an independent watermark stored in the watermarks table.

# Workflow:

Fetch last_exported_at

Query rows after watermark

Write CSV

Compute MAX(updated_at)

Update watermark

Commit transaction

⚠ Watermark updates ONLY after successful export.

If export fails → rollback → watermark unchanged.

### 📁 Output Files

All CSV exports are written to:

/output

# Format:

<export_type>_<consumer_id>_<job_id>.csv
### 🧪 Testing

Run tests inside Docker:
```bash
docker-compose exec app pytest --cov=app
```

### Current coverage:

TOTAL: 90%
### 🛠 Environment Variables

See .env.example:

DATABASE_URL=
PORT=8080
### 📦 Tech Stack

FastAPI

PostgreSQL

Docker

pytest

Faker

psycopg2

### 👩‍💻 Author

Konakalla Chopra Lakshmi Sathvika 
GitHub: https://github.com/Chopra-14