import json
import pandas as pd
import streamlit as st
from green_analyzer.analyzer import analyze_source, findings_as_dicts
from run_benchmarks import run_suite

st.set_page_config(page_title="Green Code Analyzer", layout="wide")
st.title("Green Code Analyzer")
st.caption("AST heuristics • runtime benchmarking • Python memory-allocation proxy")
st.warning("Electricity is not directly measured. Runtime and tracemalloc are resource-efficiency proxies.")
tab1, tab2, tab3 = st.tabs(["Static Analyzer", "Benchmark Lab", "Method & Limitations"])

with tab1:
    st.subheader("Analyze Python source")
    upload = st.file_uploader("Upload a .py file", type=["py"])
    default = "def check_items(rows, blocked):\n    for row in rows:\n        for item in row:\n            if item in blocked:\n                print(item)\n"
    source = upload.getvalue().decode("utf-8", errors="replace") if upload else st.text_area("Or paste Python code", default, height=220)
    if st.button("Analyze code"):
        try:
            findings = findings_as_dicts(analyze_source(source, upload.name if upload else "<editor>"))
            if findings:
                st.success(f"Found {len(findings)} potential issue(s).")
                st.dataframe(pd.DataFrame(findings), use_container_width=True, hide_index=True)
            else:
                st.info("No findings from configured rules; this does not prove the code is optimal.")
        except ValueError as e:
            st.error(str(e))

with tab2:
    st.subheader("Baseline vs optimized functions")
    c1, c2 = st.columns(2)
    size = c1.number_input("Input size", 100, 10000, 1500, 100)
    repeats = c2.number_input("Repeated trials", 1, 15, 5)
    st.caption("Nested-loop baseline is quadratic; keep the input size moderate.")
    if st.button("Run benchmarks"):
        with st.spinner("Benchmarking..."):
            results = run_suite(int(size), int(repeats))
        st.session_state["results"] = results
        rows = [{"Workload": r["workload"], "Outputs equivalent": r["outputs_equivalent"],
                 "Baseline median (s)": r["baseline"]["median_seconds"] if r["baseline"] else None,
                 "Optimized median (s)": r["optimized"]["median_seconds"] if r["optimized"] else None,
                 "Speedup (x)": r["speedup"],
                 "Baseline peak bytes": r["baseline"]["median_peak_bytes"] if r["baseline"] else None,
                 "Optimized peak bytes": r["optimized"]["median_peak_bytes"] if r["optimized"] else None}
                for r in results]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        chart = pd.DataFrame(rows).set_index("Workload")[["Baseline median (s)", "Optimized median (s)"]]
        st.bar_chart(chart)
        st.download_button("Download results JSON", json.dumps({"size": int(size), "repeats": int(repeats), "results": results}, indent=2),
                           file_name="benchmark_results.json", mime="application/json")
    elif "results" in st.session_state:
        st.dataframe(pd.DataFrame(st.session_state["results"]), use_container_width=True)

with tab3:
    st.markdown("""
    - **GCA001:** nested loops are flagged as a heuristic; they are not automatically defects.
    - **GCA002:** membership checks inside loops may be expensive if the container is a list.
    - **Runtime:** median of repeated `time.perf_counter` measurements.
    - **Memory:** peak Python-tracked allocations via `tracemalloc`, not total process RAM.
    - **Energy:** not directly measured. Avoid claiming joules, kWh, or verified energy savings.
    - Benchmark outcomes depend on hardware, interpreter, input, and background activity.
    """)
