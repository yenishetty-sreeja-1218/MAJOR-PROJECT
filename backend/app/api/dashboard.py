from fastapi import APIRouter
from pathlib import Path
import sys

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT_DIR))

from ingestion import load_logs, get_log_statistics

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard():
    ddf = load_logs()
    return get_log_statistics(ddf)