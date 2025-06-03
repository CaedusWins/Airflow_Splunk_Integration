# Airflow and Splunk Integration

This project demonstrates the integration of Apache Airflow with Splunk for logging data from a simple database. The setup includes a Directed Acyclic Graph (DAG) that initializes a database, logs data, and sends the logs to Splunk.

## Project Structure

```
airflow-splunk-integration
├── dags
│   └── simple_db_logging_dag.py
├── scripts
│   ├── init_db.py
│   └── send_to_splunk.py
├── docker
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
├── README.md
└── .env
```

## Dependencies

- Apache Airflow
- Requests (for HTTP requests to Splunk)
- Database connector (e.g., psycopg2 for PostgreSQL, pymysql for MySQL)
- Docker and Docker Compose for containerization

## Setup Instructions

1. **Create a Virtual Environment**: 
   Create a virtual environment to isolate your project dependencies.
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   Install the required Python packages using pip.
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the Docker Image**:
   Navigate to the `docker` directory and build the Docker image.
   ```bash
   cd docker
   docker build -t airflow-splunk-integration .
   ```

5. **Start the Services**:
   Use Docker Compose to start the services defined in `docker-compose.yml`.
   ```bash
   docker-compose up
   ```

6. **Access the Airflow Web Interface**:
   Open your web browser and go to `http://localhost:8080` to access the Airflow web interface. You can monitor the execution of the DAG from here.

## Environment Variables

The `.env` file contains sensitive information and configuration settings. Make sure to update the following variables:

```
DATABASE_URL=your_database_url
SPLUNK_HEC_TOKEN=your_splunk_hec_token
```

## Key Files Overview

- **`dags/simple_db_logging_dag.py`**: Contains the DAG definition for logging data and sending it to Splunk.
- **`scripts/init_db.py`**: Initializes the database and populates it with sample data.
- **`scripts/send_to_splunk.py`**: Sends log data to Splunk using the HTTP Event Collector (HEC).
- **`docker/Dockerfile`**: Builds the Docker image with all necessary dependencies.
- **`docker/docker-compose.yml`**: Defines the services for Airflow and Splunk.
- **`requirements.txt`**: Lists the Python dependencies required for the project.

This setup provides a local environment to test the integration of Airflow with Splunk for logging data from a simple database.