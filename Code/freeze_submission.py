"""Create the deterministic final-submission version and checksum manifest."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import matplotlib
import nbclient
import nbformat
import numpy
import pandas
import scipy
import sklearn

RELEASE_TAG = "capstone-final-v1.0.4"
FROZEN_ON = "2026-08-20"
FILES = (
    "Results/query_output_ledger.csv",
    "Results/bbo_query_ledger.csv",
    "Results/week12_sensitivity_analysis.csv",
    "Results/gp_rolling_validation_predictions.csv",
    "Results/gp_validation_metrics.csv",
    "Results/gp_final_hyperparameters.csv",
    "Week_12/02_Notebook/Week_12_Capstone.ipynb",
    "Notebooks/GP_Evaluation_and_Calibration.ipynb",
    "Documentation/EVALUATION.md",
    "Documentation/DATASET_DATASHEET.md",
    "Documentation/MODEL_CARD.md",
    "Code/run_week12_sensitivity.py",
    "Code/run_gp_validation.py",
    "requirements-lock.txt",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [relative for relative in FILES if not (root / relative).is_file()]
    if missing:
        raise FileNotFoundError(f"submission artifacts missing: {missing}")
    manifest = {
        "release_tag": RELEASE_TAG,
        "version_resolution": f"git rev-list -n 1 {RELEASE_TAG}",
        "frozen_on": FROZEN_ON,
        "python": platform.python_version(),
        "libraries": {
            "numpy": numpy.__version__, "pandas": pandas.__version__,
            "scipy": scipy.__version__, "scikit-learn": sklearn.__version__,
            "matplotlib": matplotlib.__version__, "nbformat": nbformat.__version__,
            "nbclient": nbclient.__version__,
        },
        "seeds": {
            "week12_gp_and_candidates": "4200 + function (4201–4208)",
            "rolling_validation_gp": "7300 + function * 100 + held_out_week",
            "sensitivity_candidates": "9100 + function (9101–9108)",
            "sensitivity_gp": "9200 + function (9201–9208)",
        },
        "canonical_post_week11_counts": [21, 21, 26, 41, 31, 31, 41, 51],
        "checksums_sha256": {relative: sha256(root / relative) for relative in FILES},
    }
    output = root / "Results" / "submission_manifest.json"
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output} with {len(FILES)} checksums")


if __name__ == "__main__":
    main()
