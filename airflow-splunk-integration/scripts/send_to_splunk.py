import os
import psycopg2
import requests
import json

db_url = os.environ.get("DATABASE_URL")
splunk_url = os.environ.get("SPLUNK_HEC_URL")
splunk_token = os.environ.get("SPLUNK_HEC_TOKEN")

# Fetch the latest log entry
conn = psycopg2.connect(db_url)
cur = conn.cursor()
cur.execute("SELECT message, created_at FROM logs ORDER BY created_at DESC LIMIT 1")
row = cur.fetchone()
cur.close()
conn.close()

if row:
    message, created_at = row
    payload = {
        "event": {
            "message": message,
            "created_at": str(created_at)
        },
        "sourcetype": "airflow_logs"
    }
    headers = {
        "Authorization": f"Splunk {splunk_token}"
    }
    response = requests.post(splunk_url, headers=headers, data=json.dumps(payload), verify=False)
    print(f"Sent to Splunk: {response.status_code} {response.text}")
else:
    print("No log entries found.")