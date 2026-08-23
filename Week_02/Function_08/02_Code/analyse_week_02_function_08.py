"""Run the canonical Week 02 Function 08 evidence and proposal review."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from Code.week_02_function_review import analyse_week_02_function, write_week_02_artifacts
def analyse(): return analyse_week_02_function(8,ROOT)
if __name__=="__main__":
    for name,path in write_week_02_artifacts(8,ROOT).items(): print(f"{name}: {path}")
