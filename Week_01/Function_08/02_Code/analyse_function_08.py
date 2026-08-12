"""Independent analysis for Week 01 Function 08."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
REPO_ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(REPO_ROOT))
from Code.data_loading import load_numpy_pair
from Code.data_validation import validate_observations
ROOT=Path(__file__).resolve().parents[1]
STRATEGY="Bayesian Optimisation"
SUBMITTED_QUERY=np.array([0.273673,0.2604,0.073937,0.078562,0.862321,0.230729,0.10688,0.352588],dtype=float)
SUBMITTED_RETURN=9.8157087929671

def analyse_function_08(data_dir: Path=ROOT/"03_Data") -> tuple[pd.DataFrame,dict]:
    """Return validated observations and an evidence summary."""
    x,y=load_numpy_pair(data_dir/"initial_inputs.npy",data_dir/"initial_outputs.npy")
    x,y=validate_observations(x,y)
    table=pd.DataFrame(x,columns=[f"x{i+1}" for i in range(x.shape[1])])
    table.insert(0,"query",np.arange(1,len(y)+1)); table["objective"]=y
    best=int(np.argmax(y))
    summary={"function":"08","strategy":STRATEGY,"n_observations":int(len(y)),
      "n_dimensions":int(x.shape[1]),"best_query":best+1,"best_input":x[best].tolist(),
      "best_output":float(y[best]),"minimum_output":float(y.min()),"mean_output":float(y.mean()),
      "standard_deviation":float(y.std()),"submitted_query":SUBMITTED_QUERY.tolist(),
      "submitted_return":float(SUBMITTED_RETURN),"submitted_improves_starter_best":bool(SUBMITTED_RETURN>y[best]),
      "submitted_improvement":float(SUBMITTED_RETURN-y[best])}
    return table,summary

def create_figure(table: pd.DataFrame,summary: dict) -> plt.Figure:
    """Return one consolidated Matplotlib diagnostic."""
    dims=[c for c in table if c.startswith("x")]; fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    axes[0].plot(table["query"],table["objective"],marker="o",lw=1.2)
    axes[0].scatter(summary["best_query"],summary["best_output"],color="crimson",s=70,label="starter best",zorder=3)
    axes[0].axhline(summary["submitted_return"],color="darkgreen",ls="--",label="submitted return")
    axes[0].set(title="Objective by query",xlabel="Query",ylabel="Objective"); axes[0].legend()
    im=axes[1].imshow(table[dims].to_numpy().T,aspect="auto",cmap="viridis",vmin=0,vmax=1)
    axes[1].set(title="Input coordinates",xlabel="Query",ylabel="Dimension"); axes[1].set_yticks(range(len(dims)),dims)
    fig.colorbar(im,ax=axes[1],label="Coordinate value"); fig.suptitle(f"Week 01 Function 08 — {STRATEGY}")
    fig.tight_layout(rect=(0, 0, 1, 0.94)); return fig

def write_artifacts(results_dir: Path=ROOT/"04_Results",figures_dir: Path=ROOT/"05_Figures") -> dict:
    """Write deterministic CSV, JSON, and PNG artifacts."""
    table,summary=analyse_function_08(); results_dir.mkdir(parents=True,exist_ok=True); figures_dir.mkdir(parents=True,exist_ok=True)
    table.to_csv(results_dir/"observations.csv",index=False)
    (results_dir/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    fig=create_figure(table,summary); fig.savefig(figures_dir/"function_08_diagnostics.png",dpi=160,bbox_inches="tight"); plt.close(fig)
    return summary

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--write-artifacts",action="store_true"); args=parser.parse_args()
    table,summary=analyse_function_08(); summary=write_artifacts() if args.write_artifacts else summary
    print(table.to_string(index=False)); print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
