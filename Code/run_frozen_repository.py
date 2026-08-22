"""Run the frozen capstone analysis from source artifacts to final checks."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    python = sys.executable
    env = os.environ.copy()
    env.setdefault("MPLCONFIGDIR", "/tmp/capstone-matplotlib")
    env.setdefault("MPLBACKEND", "Agg")
    env.setdefault("OPENBLAS_NUM_THREADS", "1")
    env.setdefault("OMP_NUM_THREADS", "1")
    env.setdefault("VECLIB_MAXIMUM_THREADS", "1")
    commands = [
        [python, "Code/audit_dataset_sizes.py"],
        [python, "Code/generate_week13_queries.py"],
        [python, "-m", "Code.portal_format", "--file", "Week_13/01_Queries/week_13_query_points.txt"],
        [python, "Code/run_gp_validation.py"],
        [python, "Code/export_performance_summary.py"],
        [python, "Code/run_week12_sensitivity.py"],
        [python, "Code/generate_week12_notebook.py"],
        [python, "Code/build_week13_strategy_notebook.py"],
        [python, "Code/generate_evaluation_notebook.py"],
        [python, "Code/generate_final_visual_results.py"],
        [python, "-m", "jupyter", "nbconvert", "--execute", "--to", "notebook", "--inplace", "Week_12/02_Notebook/Week_12_Capstone.ipynb"],
        [python, "-m", "jupyter", "nbconvert", "--execute", "--to", "notebook", "--inplace", "Week_13/02_Notebook/Week_13_Optimisation_Strategy.ipynb"],
        [python, "-m", "jupyter", "nbconvert", "--execute", "--to", "notebook", "--inplace", "Notebooks/GP_Evaluation_and_Calibration.ipynb"],
        [python, "-m", "jupyter", "nbconvert", "--execute", "--to", "notebook", "--inplace", "Notebooks/Final_Visual_Results.ipynb"],
        [python, "Code/audit_dataset_sizes.py"],
        [python, "Code/freeze_submission.py"],
        [python, "-m", "unittest", "discover", "-s", "Code/tests", "-v"],
    ]
    results = []
    started = time.time()
    for index, command in enumerate(commands, 1):
        print(f"[{index:02d}/{len(commands)}] {' '.join(command)}", flush=True)
        step_started = time.time()
        completed = subprocess.run(command, cwd=root, env=env, check=False)
        results.append(
            {
                "command": command,
                "returncode": completed.returncode,
                "seconds": round(time.time() - step_started, 3),
            }
        )
        if completed.returncode:
            break
    report = {
        "status": "pass" if len(results) == len(commands) and all(row["returncode"] == 0 for row in results) else "fail",
        "python": sys.version,
        "total_seconds": round(time.time() - started, 3),
        "steps_completed": len(results),
        "steps_expected": len(commands),
        "steps": results,
    }
    output = root / "Results" / "frozen_run_report.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}: {report['status']}")
    if report["status"] != "pass":
        raise SystemExit("frozen repository run failed")


if __name__ == "__main__":
    main()
