#import dask.dataframe as dd
#
## Load logs
#df = dd.read_csv("logs/app_logs.csv")
#
## Convert to Dask dataframe
#ddf = df
#
## --- Detection Rules ---
#
## 1. Error Spike
#error_count = len(ddf[ddf["level"] == "ERROR"])
#if error_count > 5:
#    print(f"[HIGH] Error spike detected: {error_count} errors")
#
## 2. High Latency
#avg_latency = ddf["response_time_ms"].mean().compute()
#if avg_latency > 2000:
#    print(f"[MEDIUM] High latency detected: {avg_latency} ms")
#
## 3. Service Down (simple simulation)
#services = ddf["service"].unique().compute()
#if len(services) < 4:
#    print("[CRITICAL] Possible service outage detected")
#
#print("\n✔ Pipeline executed successfully")
#

import dask.dataframe as dd
import json
from alert import send_alert
from detection import detect_anomalies

# Load logs
ddf = dd.read_csv("app_logs.csv")

print("✔ Logs Loaded")

# Detect anomalies
anomalies = detect_anomalies(ddf)

# Alert + Store
if anomalies:
    print("\nAnomalies Detected:\n")

    for anomaly in anomalies:
        severity = anomaly["severity"]
        message = f"{anomaly['type']} → {anomaly['details']}"

        # Send alert
        send_alert(severity, message)

    # Save to JSON
    with open("anomalies.json", "w") as f:
        json.dump(anomalies, f, indent=4)

else:
    print("✔ No anomalies detected")
