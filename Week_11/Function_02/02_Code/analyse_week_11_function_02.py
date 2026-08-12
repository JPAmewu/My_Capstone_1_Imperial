"""Run the focused Week 11 Function 02 evidence review."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
REPO_ROOT=Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path: sys.path.insert(0,str(REPO_ROOT))
from Code.weekly_function_review import analyse_weekly_function, plot_weekly_function, write_review_artifacts
WEEK=11; FUNCTION=2

def analyse():
    """Return the validated table, summary, and consolidated figure."""
    frame,summary=analyse_weekly_function(WEEK,FUNCTION,REPO_ROOT)
    return frame,summary,plot_weekly_function(frame,summary)

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--write-artifacts",action="store_true"); args=parser.parse_args()
    frame,summary,figure=analyse()
    if args.write_artifacts: summary=write_review_artifacts(WEEK,FUNCTION,REPO_ROOT)
    print(frame.to_string(index=False)); print(json.dumps(summary,indent=2)); figure.clear()
if __name__=="__main__": main()
