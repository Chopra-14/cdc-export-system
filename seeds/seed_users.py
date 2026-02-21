from faker import Faker
import psycopg2
import random
from datetime import datetime, timedelta
import os

fake = Faker()

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydatabase")

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM users")
count = cur.fetchone()[0]

if count >= 100000:
    print("Users already seeded.")
    exit()

print("Seeding users...")

base_time = datetime.utcnow() - timedelta(days=30)

records = []

for i in range(100000):
    created = base_time + timedelta(seconds=random.randint(0, 2592000))
    updated = created + timedelta(seconds=random.randint(0, 86400))

    is_deleted = random.random() < 0.01

    records.append((
        fake.name(),
        fake.unique.email(),
        created,
        updated,
        is_deleted
    ))

args = ",".join(cur.mogrify("(%s,%s,%s,%s,%s)", r).decode() for r in records)

cur.execute(
    "INSERT INTO users (name,email,created_at,updated_at,is_deleted) VALUES " + args
)

conn.commit()
cur.close()
conn.close()

print("Seed completed.")