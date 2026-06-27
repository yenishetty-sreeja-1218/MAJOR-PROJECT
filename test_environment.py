import sys
import time
import platform
from datetime import datetime

def print_header():
    print("=" * 65)
    print("   LogSentinel — Environment Validation Report")
    print(f"   Date     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Platform : {platform.system()} {platform.release()}")
    print(f"   Python   : {platform.python_version()}")
    print("=" * 65)


def test_dask():
    print("\n[TEST 1] Dask — Log File Processing")
    print("-" * 65)

    import dask
    import dask.dataframe as dd
    import pandas as pd
    import numpy as np

    print(f"  ✔ Dask version              : {dask.__version__}")

    # Simulate a log dataset similar to log_schema.yaml
    np.random.seed(42)
    n = 10000
    services = ["payment-service", "auth-service", "search-service", "user-service"]
    levels = ["INFO", "WARNING", "ERROR", "DEBUG"]

    df = pd.DataFrame({
        "timestamp": pd.date_range("2024-02-13", periods=n, freq="s"),
        "level": np.random.choice(levels, size=n, p=[0.6, 0.2, 0.15, 0.05]),
        "service": np.random.choice(services, size=n),
        "response_time_ms": np.random.randint(50, 5000, size=n),
        "status_code": np.random.choice([200, 201, 400, 404, 500], size=n, p=[0.6, 0.1, 0.1, 0.1, 0.1]),
    })

    ddf = dd.from_pandas(df, npartitions=4)
    print(f"  ✔ Simulated log dataset     : {n} rows loaded into Dask")
    print(f"  ✔ Partitions created        : {ddf.npartitions}")

    # Test 1a: Count total ERROR logs
    error_count = len(ddf[ddf["level"] == "ERROR"])
    print(f"  ✔ ERROR logs detected       : {error_count}")
    assert error_count > 0, "Expected some ERROR logs"

    # Test 1b: Average response time per service
    avg_response = ddf.groupby("service")["response_time_ms"].mean().compute()
    print(f"  ✔ Avg response time computed per service:")
    for svc, avg in avg_response.items():
        print(f"       {svc:<25} : {round(avg, 1)} ms")
    assert len(avg_response) == 4, "Expected 4 services"

    # Test 1c: Count 500 status codes (server errors)
    server_errors = len(ddf[ddf["status_code"] == 500])
    print(f"  ✔ HTTP 500 errors found     : {server_errors}")
    assert server_errors > 0, "Expected some 500 errors"

    # Test 1d: Filter WARNING and ERROR only
    critical_logs = ddf[ddf["level"].isin(["WARNING", "ERROR"])]
    critical_count = len(critical_logs)
    print(f"  ✔ WARNING + ERROR logs      : {critical_count}")
    assert critical_count > 0

    print(f"  ✔ All Dask log processing tests passed")
    return True


def test_ray():
    print("\n[TEST 2] Ray — Distributed Anomaly Detection")
    print("-" * 65)

    import ray
    import numpy as np

    print(f"  ✔ Ray version               : {ray.__version__}")
    ray.init(ignore_reinit_error=True, logging_level="error")
    print(f"  ✔ Ray initialized successfully")

    # Test 2a: Detect error spike anomaly
    # Rule from anomaly_schema.yaml: if errors > 100 in 5 minutes -> anomaly
    @ray.remote
    def detect_error_spike(error_count, threshold=100):
        if error_count > threshold:
            return {
                "anomaly": "error_spike",
                "severity": "HIGH",
                "observed": error_count,
                "threshold": threshold,
                "detected": True
            }
        return {"detected": False}

    start = time.time()
    result = ray.get(detect_error_spike.remote(error_count=152))
    elapsed = round(time.time() - start, 4)
    assert result["detected"] == True
    assert result["severity"] == "HIGH"
    print(f"  ✔ Error spike detection     : {result['observed']} errors > threshold {result['threshold']} → {result['severity']} anomaly")

    # Test 2b: Detect high latency anomaly
    # Rule: if avg response_time_ms > 2000 -> anomaly
    @ray.remote
    def detect_high_latency(avg_ms, threshold=2000):
        if avg_ms > threshold:
            return {
                "anomaly": "high_latency",
                "severity": "MEDIUM",
                "observed_ms": avg_ms,
                "threshold_ms": threshold,
                "detected": True
            }
        return {"detected": False}

    result2 = ray.get(detect_high_latency.remote(avg_ms=3200))
    assert result2["detected"] == True
    print(f"  ✔ High latency detection    : {result2['observed_ms']}ms > threshold {result2['threshold_ms']}ms → {result2['severity']} anomaly")

    # Test 2c: Detect service down anomaly
    # Rule: if silence_minutes > 3 -> anomaly
    @ray.remote
    def detect_service_down(service_name, silence_minutes, threshold=3):
        if silence_minutes > threshold:
            return {
                "anomaly": "service_down",
                "severity": "CRITICAL",
                "service": service_name,
                "silent_for_minutes": silence_minutes,
                "detected": True
            }
        return {"detected": False}

    result3 = ray.get(detect_service_down.remote("payment-service", silence_minutes=7))
    assert result3["detected"] == True
    assert result3["severity"] == "CRITICAL"
    print(f"  ✔ Service down detection    : '{result3['service']}' silent for {result3['silent_for_minutes']} mins → {result3['severity']} anomaly")

    # Test 2d: Run all 3 detectors in parallel
    futures = [
        detect_error_spike.remote(200),
        detect_high_latency.remote(4500),
        detect_service_down.remote("auth-service", 10),
    ]
    parallel_results = ray.get(futures)
    detected_count = sum(1 for r in parallel_results if r["detected"])
    print(f"  ✔ Parallel detection run    : {detected_count}/3 anomalies detected simultaneously")
    print(f"  ✔ Ray execution time        : {elapsed}s")
    assert detected_count == 3

    ray.shutdown()
    print(f"  ✔ Ray shutdown cleanly")
    return True


def run_all():
    print_header()
    results = {}

    for name, fn in [("Dask", test_dask), ("Ray", test_ray)]:
        try:
            fn()
            results[name] = "PASSED"
        except Exception as e:
            print(f"\n  ✘ {name} test failed: {e}")
            results[name] = "FAILED"

    print("\n" + "=" * 65)
    print("   SUMMARY")
    print("-" * 65)
    for lib, status in results.items():
        symbol = "✔" if status == "PASSED" else "✘"
        print(f"  {symbol} {lib:<10} : {status}")

    all_passed = all(v == "PASSED" for v in results.values())
    print("-" * 65)
    if all_passed:
        print("  STATUS     : All tests passed.")
    else:
        print("  STATUS     : Some tests failed. Check output above.")
    print("=" * 65)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    run_all()
