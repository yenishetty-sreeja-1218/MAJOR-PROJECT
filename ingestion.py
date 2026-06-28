from pathlib import Path
import dask.dataframe as dd

# Project root (folder containing ingestion.py)
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = BASE_DIR / "app_logs.csv"


def load_logs(file_path=None):
    """
    Load logs into a Dask DataFrame.
    """
    if file_path is None:
        file_path = DEFAULT_CSV

    return dd.read_csv(str(file_path))


def get_log_statistics(ddf):
    """
    Return basic log statistics.
    """
    return {
        "total_logs": int(ddf.shape[0].compute()),
        "log_levels": ddf["level"].value_counts().compute().to_dict(),
        "avg_response_time": (
            ddf.groupby("service")["response_time_ms"]
            .mean()
            .compute()
            .to_dict()
        )
    }


if __name__ == "__main__":
    ddf = load_logs()

    print("\n✔ Logs Loaded Successfully")
    print(ddf.head())

    print("\n✔ Log Level Count:")
    print(ddf["level"].value_counts().compute())

    print("\n✔ Service-wise Avg Response Time:")
    print(ddf.groupby("service")["response_time_ms"].mean().compute())