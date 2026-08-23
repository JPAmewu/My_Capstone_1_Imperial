"""Canonical Week 13 Function 07 entry point."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from Code.historical_function_review import write_historical_artifacts
if __name__ == "__main__":
    print(write_historical_artifacts(13, 7, ROOT))
