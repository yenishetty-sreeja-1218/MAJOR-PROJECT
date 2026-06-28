from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(
    prefix="/anomalies",
    tags=["Anomalies"]
)

ROOT_DIR = Path(__file__).resolve().parents[3]
ANOMALY_FILE = ROOT_DIR / "anomalies.json"


@router.get("/")
def get_anomalies():
    with open(ANOMALY_FILE, "r") as file:
        data = json.load(file)

    return data