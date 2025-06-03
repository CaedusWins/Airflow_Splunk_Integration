from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2
import requests
import json
import os

def insert_log():
    conn = psycopg2.connect(
        dbname="testdb",
        user="postgres",
        password="postgres",
        host="db",
        port=5432
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO log (level, message) VALUES (%s, %s)", ("ERROR", "Airflow test log entry"))
    conn.commit()
    cur.close()
    conn.close()

def fetch_latest_log():
    conn = psycopg2.connect(
        dbname="testdb",
        user="postgres",
        password="postgres",
        host="db",
        port=5432
    )
    cur = conn.cursor()
    cur.execute("SELECT id, log_time, level, message FROM log ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {
            "id": row[0],
            "log_time": row[1].isoformat(),
            "level": row[2],
            "message": row[3]
        }
    return None

def send_to_splunk(**context):
    log = context['ti'].xcom_pull(task_ids='fetch_log')
    if not log:
        raise Exception("No log found to send to Splunk")
    splunk_url = os.environ.get("SPLUNK_HEC_URL", "https://splunk:8088/services/collector")
    splunk_token = os.environ.get("SPLUNK_HEC_TOKEN", "YOUR_SPLUNK_TOKEN")
    headers = {
        "Authorization": f"Splunk {splunk_token}"
    }
    payload = {
        "event": log,
        "sourcetype": "airflow_logs"
    }
    response = requests.post(splunk_url, headers=headers, data=json.dumps(payload), verify=False)
    response.raise_for_status()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 1),
    'retries': 0,
}

with DAG(
    'db_to_splunk_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    insert_log_task = PythonOperator(
        task_id='insert_log',
        python_callable=insert_log,
    )

    fetch_log_task = PythonOperator(
        task_id='fetch_log',
        python_callable=fetch_latest_log,
    )

    send_to_splunk_task = PythonOperator(
        task_id='send_to_splunk',
        python_callable=send_to_splunk,
        provide_context=True,
    )

    insert_log_task >> fetch_log_task >> send_to_splunk_task