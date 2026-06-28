from fastapi import APIRouter
from pathlib import Path
import sys

# Add project root
ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT_DIR))

from ingestion import load_logs
from detection import detect_anomalies

router = APIRouter(
    prefix="/detect",
    tags=["Detection"]
)


@router.post("/")
def run_detection():

    ddf = load_logs()

    anomalies = detect_anomalies(ddf)

    return {
        "status": "success",
        "anomalies": anomalies
    }