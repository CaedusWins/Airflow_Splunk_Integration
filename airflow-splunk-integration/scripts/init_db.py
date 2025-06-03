import os
import psycopg2

db_url = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(db_url)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id SERIAL PRIMARY KEY,
        message TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    )
""")
cur.execute("INSERT INTO logs (message) VALUES (%s)", ("Sample log entry from Airflow",))
conn.commit()
cur.close()
conn.close()
print("Database initialized and sample data inserted.")