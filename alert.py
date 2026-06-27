import datetime
from email.mime.text import MIMEText
import smtplib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------
# Slack Alert
# -------------------------
def send_slack_alert(message):
    webhook_url = "YOUR_SLACK_WEBHOOK"

    try:
        requests.post(webhook_url, json={"text": message})
    except Exception as e:
        print("Slack alert failed:", e)

# -------------------------
# Email Alert
# -------------------------
def send_email_alert(message):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    try:
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = "LogSentinel Alert"
        msg["From"] = sender
        msg["To"] = receiver
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
    except Exception as e:
        print("Email failed:", e)

# -------------------------
# Main Alert Function
# -------------------------
def send_alert(severity, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alert_msg = f"[{timestamp}] [{severity}] {message}"

    print(alert_msg)

    # Save to file
    with open("alerts.log", "a", encoding="utf-8") as f:
        f.write(alert_msg + "\n")

    # CALL ALERT CHANNELS
    send_email_alert(alert_msg)

    #Slack disabled
    #send_slack_alert(alert_msg)