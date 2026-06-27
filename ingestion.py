import dask.dataframe as dd


def load_logs(file_path="app_logs.csv"):
    """
    Load logs into a Dask DataFrame.
    """
    return dd.read_csv(file_path)


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

    stats = get_log_statistics(ddf)
    print("\n✔ Logs Loaded Successfully")
    print(ddf.head())

    print("\n✔ Log Level Count:")
    print(ddf["level"].value_counts().compute())

    print("\n✔ Service-wise Avg Response Time:")
    print(ddf.groupby("service")["response_time_ms"].mean().compute())