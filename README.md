# Green Code Analyzer for Resource-Efficient Software

A student-friendly Python project combining AST-based static heuristics, correctness-checked microbenchmarks, Python allocation tracking, and a Streamlit dashboard.

## Requirements
Python 3.10–3.12 recommended.

## Setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If PowerShell blocks activation, use Command Prompt: `.venv\Scripts\activate.bat`.

## Setup (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
Static analysis:
```bash
python -m green_analyzer.cli examples/sample_inefficient.py
python -m green_analyzer.cli examples/sample_inefficient.py --json-output reports/findings.json
```
Benchmark suite:
```bash
python run_benchmarks.py --size 1500 --repeats 5
```
Launch dashboard:
```bash
streamlit run app.py
```
Tests:
```bash
python -m unittest discover -s tests -v
```

## Structure
```text
green_code_analyzer/
├── app.py
├── run_benchmarks.py
├── requirements.txt
├── README.md
├── green_analyzer/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cli.py
│   └── benchmark.py
├── examples/
│   ├── __init__.py
│   ├── sample_inefficient.py
│   └── workloads.py
├── tests/
│   ├── test_analyzer.py
│   └── test_benchmark.py
└── reports/
```

## Rules
- **GCA001:** nested `for`/`async for` loops. This is a heuristic; nested loops are not automatically inefficient.
- **GCA002:** membership checks against a named container inside a loop. If the container is a list, repeated membership checks may be expensive. The analyzer cannot determine its runtime type.

## Metrics and limitations
- Runtime: `time.perf_counter`, median of repeated trials.
- Memory proxy: peak Python-tracked allocations via `tracemalloc`; not total process RAM.
- Correctness: benchmark outputs are compared before timing is accepted.
- Energy is **not directly measured**. Do not claim joules/kWh or verified energy savings. Describe runtime and memory-allocation changes as resource-efficiency proxies.
- Results depend on input, Python version, CPU load, and background processes. The nested-loop benchmark is quadratic; use moderate input sizes.
