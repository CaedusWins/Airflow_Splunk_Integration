FROM apache/airflow:2.8.3-python3.9

COPY docker/entrypoint.sh /entrypoint.sh

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dags/ /usr/local/airflow/dags/

ENTRYPOINT ["/entrypoint.sh"]