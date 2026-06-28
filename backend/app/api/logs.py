from fastapi import APIRouter
from pathlib import Path
import sys

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT_DIR))

from ingestion import load_logs

router = APIRouter(
    prefix="/logs",
    tags=["Logs"]
)


@router.get("/")
def get_logs(limit: int = 100):
    ddf = load_logs()

    pdf = ddf.head(limit)

    return pdf.to_dict(orient="records")