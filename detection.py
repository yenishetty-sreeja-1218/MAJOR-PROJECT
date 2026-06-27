from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(ddf):
    anomalies = []

    # -------------------------
    # Rule-Based Detection
    # -------------------------
    error_count = ddf[ddf["level"] == "ERROR"].shape[0].compute()
    if error_count > 5:
        anomalies.append({
            "type": "error_spike",
            "severity": "HIGH",
            "details": f"{error_count} errors detected"
        })

    avg_latency = ddf["response_time_ms"].mean().compute()
    if avg_latency > 2000:
        anomalies.append({
            "type": "high_latency",
            "severity": "MEDIUM",
            "details": f"{avg_latency} ms latency"
        })

    services = ddf["service"].nunique().compute()
    if services < 4:
        anomalies.append({
            "type": "service_down",
            "severity": "CRITICAL",
            "details": "Possible service outage"
        })

    # -------------------------
    # Statistical Detection (Z-score)
    # -------------------------
    mean = ddf["response_time_ms"].mean().compute()
    std = ddf["response_time_ms"].std().compute()

    if std != 0:
        z_score = (avg_latency - mean) / std
        if z_score > 2:
            anomalies.append({
                "type": "statistical_latency_anomaly",
                "severity": "HIGH",
                "details": f"Z-score: {round(z_score,2)}"
            })

    # -------------------------
    # ML Detection (Isolation Forest)
    # -------------------------
    pdf = ddf.compute()

    model = IsolationForest(contamination=0.1, random_state=42)
    pdf["anomaly"] = model.fit_predict(pdf[["response_time_ms"]])

    anomaly_count = (pdf["anomaly"] == -1).sum()

    if anomaly_count > 0:
        anomalies.append({
            "type": "ml_anomaly",
            "severity": "HIGH",
            "details": f"{anomaly_count} anomalies detected by ML"
        })

    return anomalies