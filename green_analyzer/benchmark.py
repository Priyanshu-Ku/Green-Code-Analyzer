import statistics
import time
import tracemalloc


def measure_call(fn, args=(), repeats=5):
    if repeats < 1:
        raise ValueError("repeats must be at least 1")
    durations, peaks = [], []
    for _ in range(repeats):
        tracemalloc.start()
        start = time.perf_counter()
        result = fn(*args)
        elapsed = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        _ = result
        durations.append(elapsed)
        peaks.append(peak)
    return {
        "median_seconds": statistics.median(durations),
        "min_seconds": min(durations),
        "max_seconds": max(durations),
        "median_peak_bytes": float(statistics.median(peaks)),
    }


def compare_functions(baseline, optimized, args=(), repeats=5, label="workload"):
    equivalent = baseline(*args) == optimized(*args)
    result = {"workload": label, "outputs_equivalent": equivalent, "baseline": None,
              "optimized": None, "speedup": None, "runtime_reduction_percent": None,
              "peak_memory_reduction_percent": None}
    if not equivalent:
        result["error"] = "Outputs differ; performance comparison was not accepted."
        return result
    b, o = measure_call(baseline, args, repeats), measure_call(optimized, args, repeats)
    bt, ot = b["median_seconds"], o["median_seconds"]
    bm, om = b["median_peak_bytes"], o["median_peak_bytes"]
    result.update(baseline=b, optimized=o,
                  speedup=bt / ot if ot > 0 else None,
                  runtime_reduction_percent=(bt - ot) / bt * 100 if bt > 0 else None,
                  peak_memory_reduction_percent=(bm - om) / bm * 100 if bm > 0 else None)
    return result
