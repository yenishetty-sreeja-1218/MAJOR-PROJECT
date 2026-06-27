# System Architecture & Data Flow

**Project:** LogSentinel — High-Throughput Log Analytics & Anomaly Monitoring System   

---

## 1. Architecture Overview

The system is a multi-stage pipeline that collects logs from distributed services, processes them at scale using Dask, and detects anomalies using Ray's distributed computing framework. Each stage is loosely coupled so components can be scaled independently.

```
┌─────────────────────────────────┐
│          Log Sources            │
│  (Apps, Servers, Microservices) │
└────────────────┬────────────────┘
                 │  raw structured logs
                 ▼
┌─────────────────────────────────┐
│      Log Ingestion Layer        │
│   (CSV / Parquet file store)    │
└────────────────┬────────────────┘
                 │  validated & stored logs
                 ▼
┌─────────────────────────────────┐
│     Dask Processing Layer       │
│  (parallel partitioned reads,   │
│   cleaning & aggregation)       │
└────────────────┬────────────────┘
                 │  aggregated metrics
                 ▼
┌─────────────────────────────────┐
│   Anomaly Detection (Ray)       │
│  (distributed worker tasks,     │
│   threshold & pattern checks)   │
└────────────────┬────────────────┘
                 │  confirmed anomalies
                 ▼
┌─────────────────────────────────┐
│         Results Store           │
│  (structured anomaly records)   │
└────────────────┬────────────────┘
                 │  query-ready data
                 ▼
┌─────────────────────────────────┐
│      Dashboard / Alerts         │
│  (visualization & notifications)│
└─────────────────────────────────┘
```

---

## 2. How Data Flows

### Stage 1 — Log Sources
Applications and services emit structured log events. Each entry follows `log_schema.yaml` which defines required fields like `timestamp`, `level`, `service`, and `message`. Enforcing a schema at the source ensures consistency across all downstream stages.

### Stage 2 — Log Ingestion Layer
Raw logs are collected and written to a persistent file store in CSV or Parquet format. This layer decouples ingestion from processing, meaning the system can handle traffic bursts without overwhelming downstream components. Logs are validated against `log_schema.yaml` before being stored.

### Stage 3 — Dask Processing Layer
Dask reads stored log files in parallel using its partitioned DataFrame model. Instead of loading millions of rows into memory at once, Dask splits data into partitions and processes them concurrently across CPU cores. This stage handles cleaning, type casting, and aggregation such as error rates and average response times per service.

### Stage 4 — Anomaly Detection (Ray)
Aggregated metrics from Dask are passed to Ray, which distributes detection tasks across multiple workers. Each worker applies detection rules defined in `anomaly_schema.yaml` — checking for error spikes, high latency, service downtime, repeated failures, and abnormal traffic. Ray's distributed model reduces detection latency significantly.

### Stage 5 — Results Store
Confirmed anomalies are persisted with full context: type, severity, observed vs expected values, affected service, and timestamp. This store is the source of truth for all reporting.

### Stage 6 — Dashboard / Alerts
The final stage reads from the Results Store and presents anomalies visually. High and critical severity events trigger real-time alerts to operations teams.

---

## 3. Key Design Decisions

**Why Dask?**  
Pandas cannot handle datasets larger than available RAM. Dask extends the Pandas API to process data lazily in partitions, making it ideal for high-volume log analytics where files can reach gigabytes.

**Why Ray?**  
Anomaly detection across millions of metrics requires parallelism beyond a single process. Ray distributes Python functions across CPU cores or a cluster, making detection fast and horizontally scalable.

**Why YAML Schemas?**  
`log_schema.yaml` and `anomaly_schema.yaml` act as contracts between pipeline stages. Any component producing or consuming data must follow these schemas, eliminating ambiguity and simplifying debugging.

---

## 4. Schema to Pipeline Mapping

| Schema File | Purpose | Used By |
|---|---|---|
| `log_schema.yaml` | Structure of raw log entries | Ingestion, Dask Processing |
| `anomaly_schema.yaml` | Structure of detected anomalies | Ray Detection, Results Store, Dashboard |

---

## 5. Technology Stack

| Component | Technology | Reason |
|---|---|---|
| Large-scale log processing | Dask | Out-of-core parallel DataFrame processing |
| Distributed anomaly detection | Ray | Scalable distributed task execution |
| Schema definition | YAML | Human-readable, language-agnostic contracts |
| Raw log storage | CSV / Parquet | Simple, portable, widely supported |
