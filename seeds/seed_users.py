from faker import Faker
import psycopg2
import random
from datetime import datetime, timedelta
import os

fake = Faker()

DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@db:5432/mydatabase"
)

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM users")
count = cur.fetchone()[0]

if count >= 100000:
    print("Users already seeded.")
    exit()

print("Seeding users...")

records = []

for _ in range(100000):
    created_at = fake.date_time_between(start_date="-30d", end_date="now")
    updated_at = fake.date_time_between(start_date=created_at, end_date="now")

    is_deleted = random.random() < 0.01

    records.append((
        fake.name(),
        fake.unique.email(),
        created_at,
        updated_at,
        is_deleted
    ))

args = ",".join(
    cur.mogrify("(%s,%s,%s,%s,%s)", r).decode()
    for r in records
)

cur.execute(
    "INSERT INTO users(name,email,created_at,updated_at,is_deleted) VALUES " + args
)

conn.commit()
cur.close()
conn.close()

print("Seed completed.")