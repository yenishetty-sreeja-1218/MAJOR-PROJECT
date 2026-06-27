import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="LogSentinel Dashboard", layout="wide")

st.title("LogSentinel - SOC Monitoring Dashboard")

# -------------------------
# Load Logs
# -------------------------
try:
    df = pd.read_csv("app_logs.csv")
    st.subheader("Log Data")
    st.dataframe(df)
except:
    st.error("Log file not found")

# -------------------------
# Log Level Distribution
# -------------------------
st.subheader("Log Level Distribution")

if 'level' in df.columns:
    level_counts = df['level'].value_counts()
    st.bar_chart(level_counts)

# -------------------------
# Response Time Analysis
# -------------------------
st.subheader("Response Time per Service")

if 'service' in df.columns:
    avg_response = df.groupby('service')['response_time_ms'].mean()
    st.bar_chart(avg_response)

# -------------------------
# Load Anomalies
# -------------------------
st.subheader("Detected Anomalies")

try:
    with open("anomalies.json") as f:
        anomalies = json.load(f)

    for a in anomalies:
        st.warning(f"{a['severity']} - {a['type']} → {a['details']}")
except:
    st.info("No anomalies detected yet")

# -------------------------
# Alerts Log
# -------------------------
st.subheader("Alert History")

try:
    with open("alerts.log") as f:
        alerts = f.readlines()

    for alert in alerts[-10:]:
        st.text(alert)
except:
    st.info("No alerts yet")
