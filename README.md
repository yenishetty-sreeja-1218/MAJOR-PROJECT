**LogSentinel — High-Throughput Log Analytics & Anomaly Monitoring System**  

---

## What This Project Does
LogSentinel is a system that collects logs from applications and automatically finds problems. Logs are structured entries that apps write when something happens. This milestone lays the foundation by defining what logs look like, what problems to detect, how the system is designed, and setting up the tools needed to build it.

--- 

## Summary

### Log Schema 
Defined the structure of log entries in `schemas/log_schema.yaml`. Includes all fields, which are required, and 3 examples of different log types (INFO, WARNING, ERROR).

### Anomaly Schema
Defined 5 types of anomalies to detect in `schemas/anomaly_schema.yaml`. Each anomaly includes a name, description, severity, and how to detect it.

### System Diagram 
Drew the system architecture and data flow diagrams using draw.io. Written explanation of how data moves through each stage is in `docs/architecture.md`.

### Setup 
Installed Dask and Ray together. Setup script, requirements, and passing tests are all in `environment/` and `tests/`.

---

## How to Run
```bash
cd environment
bash setup.sh
```


## Project Overview
LogSentinel is a distributed log monitoring system that processes application logs, detects anomalies, generates alerts, and visualizes insights through a dashboard.

The system is designed to simulate a real-world SIEM (Security Information and Event Management) pipeline.

---

## Key Features

- Log ingestion using CSV
- Distributed processing using Dask
- Rule-based anomaly detection
- Statistical detection (Z-score)
- Machine Learning detection (Isolation Forest)
- Email alerting system
- Streamlit dashboard visualization

---

## Technologies Used

- Python
- Dask (distributed processing)
- Pandas / NumPy
- Scikit-learn (Isolation Forest)
- Streamlit (dashboard)
- SMTP (email alerts)

---

## Anomaly Detection Techniques

### 1. Rule-Based Detection
- Error spike detection
- Service failure detection

### 2. Statistical Detection
- Z-score based latency anomaly

### 3. Machine Learning
- Isolation Forest for outlier detection

---

## Alert System

- Console alerts
- File logging (`alerts.log`)
- Email notifications using SMTP

---

## Dashboard

Streamlit dashboard provides:
- Log visualization
- Log level distribution
- Response time analysis
- Detected anomalies
- Alert history

---

## How to Run

### Step 1 — Activate Environment
```bash
.\venv\Scripts\Activate

### Step 2 — Run Pipeline
```bash
python pipeline.py

### Step 3 — Run Dashboard
```bash
streamlit run dashboard.py

## Security
Sensitive credentials such as email passwords are stored in a `.env` file and are not included in the repository.

## License
This project is licensed under the MIT License.
