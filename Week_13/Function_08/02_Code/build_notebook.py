"""Canonical Week 13 Function 08 entry point."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from Code.build_historical_function_notebook import build
if __name__ == "__main__":
    print(build(13, 8, ROOT))
