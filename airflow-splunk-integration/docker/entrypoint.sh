#!/bin/bash
# filepath: c:\Dev\Airflow_Splunk_Integration\airflow-splunk-integration\docker\entrypoint.sh

airflow db init

airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin || true

if [ "$1" = "scheduler" ]; then
    exec airflow scheduler
else
    exec airflow webserver
fi