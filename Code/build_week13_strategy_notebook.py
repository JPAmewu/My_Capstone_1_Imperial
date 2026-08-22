"""Build the Week 13 strategy notebook after verified Week 12 ingestion."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat as nbf


def build(root: Path) -> Path:
    notebook = nbf.v4.new_notebook()
    notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
    notebook.cells = [
        nbf.v4.new_markdown_cell(
            "# Week 13 optimisation strategy — 12th query submission\n\n"
            "## tl;dr\n\n"
            "The supplied cumulative Week 12 files reproduce all 88 published Week 1–11 pairs exactly and add eight aligned Week 12 evaluations. "
            "The corrected cumulative data are used to refit eight anisotropic Matérn-5/2 Gaussian Processes. "
            "One bounded, finite, six-decimal and previously unevaluated Week 13 query is selected for every function after comparing UCB, EI and PI."
        ),
        nbf.v4.new_markdown_cell(
            "## Context & Methods\n\n"
            "**Primary evidence:** the supplied `week_12_inputs.txt` and `week_12_outputs.txt`, preserved byte-for-byte under `Results/source_evidence/week_12/`. "
            "Their SHA-256 hashes and source-file date are recorded in the ledger and validation report.\n\n"
            "The pre-reconciliation Week 12 query file repeated the Week 11 queries and matched none of the supplied final-round inputs. "
            "It is preserved under `Week_12/01_Queries/archive/`; the supplied 12th input row is now the active Week 12 submission record.\n\n"
            "### Key assumptions\n\n"
            "- Each function is maximised independently on `[0,1]^d`.\n"
            "- The exact 88-pair prefix match establishes continuity with the published ledger.\n"
            "- Source-file dates are provenance metadata, not authoritative platform timestamps.\n"
            "- GP predictions guide an expensive next evaluation but do not prove global optimality."
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\n"
            "import json,sys\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "get_ipython().run_line_magic('matplotlib','inline')\n"
            "ROOT=Path.cwd().resolve()\n"
            "while not (ROOT/'Code').is_dir() and ROOT!=ROOT.parent: ROOT=ROOT.parent\n"
            "sys.path.insert(0,str(ROOT))\n"
            "from Code.weekly_evidence import DIMENSIONS,pairs_through_week\n"
            "from Code.data_validation import validate_observations\n"
            "ledger=pd.read_csv(ROOT/'Results/query_output_ledger.csv')\n"
            "strategy=pd.read_csv(ROOT/'Week_13/04_Results/week_13_strategy_summary.csv')\n"
            "comparison=pd.read_csv(ROOT/'Week_13/04_Results/week_13_acquisition_comparison.csv')\n"
            "validation=json.loads((ROOT/'Results/week_12_evidence_validation.json').read_text())\n"
            "print(f'Repository: {ROOT}')"
        ),
        nbf.v4.new_markdown_cell("## Data\n\n### Week 12 reconciliation and returned observations"),
        nbf.v4.new_code_cell(
            "assert validation['historical_prefix_pairs_checked']==88\n"
            "assert validation['historical_prefix_mismatches']==0\n"
            "assert validation['week_12_pairs_appended']==8\n"
            "week12=ledger.loc[ledger.week.eq(12),['function','query','returned_output','evidence_status']]\n"
            "week12"
        ),
        nbf.v4.new_markdown_cell(
            "### Data-quality profile\n\n"
            "The intended grain is one evaluated query and one scalar response per function. "
            "The checks below cover row alignment, dimensions, finite values, unit-hypercube bounds and exact duplicates."
        ),
        nbf.v4.new_code_cell(
            "evidence={}; quality=[]\n"
            "for function in range(1,9):\n"
            "    data=ROOT/f'Week_01/Function_{function:02d}/03_Data'\n"
            "    inputs=np.load(data/'initial_inputs.npy'); outputs=np.load(data/'initial_outputs.npy').reshape(-1)\n"
            "    pairs=pairs_through_week(12,function)\n"
            "    inputs=np.vstack([inputs]+[np.asarray(query,float)[None,:] for query,_ in pairs])\n"
            "    outputs=np.r_[outputs,[value for _,value in pairs]]\n"
            "    inputs,outputs=validate_observations(inputs,outputs,dimensions=DIMENSIONS[function])\n"
            "    rounded=np.round(inputs,6); duplicate_rows=len(rounded)-len(np.unique(rounded,axis=0))\n"
            "    evidence[function]=(inputs,outputs)\n"
            "    quality.append({'Function':f'F{function}','Rows':len(outputs),'Dimensions':inputs.shape[1],"
            "'Missing values':int(np.isnan(inputs).sum()+np.isnan(outputs).sum()),'Out-of-bounds coordinates':int(((inputs<0)|(inputs>1)).sum()),"
            "'Repeated rows at 6dp':duplicate_rows,'Minimum output':outputs.min(),'Mean output':outputs.mean(),"
            "'Output SD':outputs.std(),'Maximum output':outputs.max(),'Latest output':outputs[-1]})\n"
            "quality=pd.DataFrame(quality); quality"
        ),
        nbf.v4.new_markdown_cell(
            "### Standardised output distributions\n\n"
            "Raw outputs are not comparable across functions. This box plot standardises each function independently so spread and outliers can be compared without mixing objective units."
        ),
        nbf.v4.new_code_cell(
            "standardised=[]\n"
            "for function,(inputs,outputs) in evidence.items():\n"
            "    scale=outputs.std() or 1.0\n"
            "    standardised.append((outputs-outputs.mean())/scale)\n"
            "fig,ax=plt.subplots(figsize=(10,4.5))\n"
            "ax.boxplot(standardised,tick_labels=[f'F{i}' for i in range(1,9)],patch_artist=True,"
            "boxprops={'facecolor':'#dce9f2','edgecolor':'#264653'},medianprops={'color':'#d97706','linewidth':2})\n"
            "ax.axhline(0,color='#444',lw=.8,ls='--'); ax.set(title='Within-function standardised output distributions',xlabel='Function',ylabel='Standardised objective value')\n"
            "ax.grid(axis='y',alpha=.25); fig.tight_layout(); plt.show()"
        ),
        nbf.v4.new_markdown_cell("### Updated within-function performance"),
        nbf.v4.new_code_cell(
            "performance=strategy[['function','verified_observations','verified_best','week_12_output','week_12_improvement']].copy()\n"
            "performance['improved_incumbent']=performance.week_12_improvement>0\n"
            "performance"
        ),
        nbf.v4.new_markdown_cell(
            "### Per-function trajectories, running best and input coverage\n\n"
            "Each function is plotted in its own objective units. Orange diamonds mark the verified Week 12 evaluation and stars mark the incumbent. The coordinate heatmap shows how the evaluated inputs cover each dimension."
        ),
        nbf.v4.new_code_cell(
            "for function,(inputs,outputs) in evidence.items():\n"
            "    query_number=np.arange(1,len(outputs)+1); incumbent=int(np.argmax(outputs))\n"
            "    fig,axes=plt.subplots(1,3,figsize=(15,4.1),gridspec_kw={'width_ratios':[1.15,1.15,1]})\n"
            "    axes[0].plot(query_number,outputs,color='#2a6fbb',marker='o',ms=3.5,lw=1.4)\n"
            "    axes[0].scatter(query_number[-1],outputs[-1],marker='D',s=65,color='#d97706',label='Week 12',zorder=4)\n"
            "    axes[0].scatter(query_number[incumbent],outputs[incumbent],marker='*',s=150,color='#f2c14e',edgecolor='#333',label='Incumbent',zorder=5)\n"
            "    axes[0].set(title='Observed objective',xlabel='Verified query number',ylabel='Objective value'); axes[0].legend()\n"
            "    axes[1].step(query_number,np.maximum.accumulate(outputs),where='post',color='#287271',lw=2)\n"
            "    axes[1].scatter(query_number[-1],np.maximum.accumulate(outputs)[-1],marker='D',s=55,color='#d97706',zorder=4)\n"
            "    axes[1].set(title='Running best',xlabel='Verified query number',ylabel='Best objective so far')\n"
            "    image=axes[2].imshow(inputs.T,aspect='auto',cmap='Blues',vmin=0,vmax=1)\n"
            "    axes[2].set(title='Input-coordinate coverage',xlabel='Verified query number',ylabel='Dimension')\n"
            "    axes[2].set_yticks(range(inputs.shape[1]),[f'x{i+1}' for i in range(inputs.shape[1])]); fig.colorbar(image,ax=axes[2],label='Coordinate')\n"
            "    for axis in axes[:2]: axis.grid(alpha=.22)\n"
            "    fig.suptitle(f'Function {function}: verified evidence through Week 12',fontweight='bold'); fig.tight_layout(); plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "### Descriptive coordinate–output associations\n\n"
            "Spearman correlations summarise monotonic association only. They can reveal potentially influential coordinates, but they do not establish causality or represent nonlinear interactions completely."
        ),
        nbf.v4.new_code_cell(
            "association=np.full((8,8),np.nan)\n"
            "for function,(inputs,outputs) in evidence.items():\n"
            "    for dimension in range(inputs.shape[1]): association[function-1,dimension]=pd.Series(inputs[:,dimension]).corr(pd.Series(outputs),method='spearman')\n"
            "fig,ax=plt.subplots(figsize=(11,5.2)); image=ax.imshow(association,aspect='auto',cmap='RdBu_r',vmin=-1,vmax=1)\n"
            "ax.set_xticks(range(8),[f'x{i}' for i in range(1,9)]); ax.set_yticks(range(8),[f'F{i}' for i in range(1,9)])\n"
            "ax.set(title='Spearman coordinate–output associations',xlabel='Input dimension',ylabel='Function')\n"
            "for i in range(8):\n"
            "    for j in range(8):\n"
            "        if np.isfinite(association[i,j]): ax.text(j,i,f'{association[i,j]:.2f}',ha='center',va='center',fontsize=8,color='white' if abs(association[i,j])>.55 else '#222')\n"
            "fig.colorbar(image,ax=ax,label='Spearman correlation'); fig.tight_layout(); plt.show()"
        ),
        nbf.v4.new_markdown_cell("## Results\n\n### UCB, EI and PI comparison"),
        nbf.v4.new_code_cell(
            "comparison[['function','method','candidate','candidate_source','predicted_mean','predicted_std','acquisition_score','kappa','xi_fraction_of_output_std']]"
        ),
        nbf.v4.new_markdown_cell(
            "### Acquisition alternatives by function\n\n"
            "Acquisition scores are not compared across UCB, EI and PI because they have different mathematical scales. Instead, each panel compares the GP mean and uncertainty at the best candidate identified by each method."
        ),
        nbf.v4.new_code_cell(
            "fig,axes=plt.subplots(2,4,figsize=(15,8),sharex=False); colours={'UCB':'#2a6fbb','EI':'#d97706','PI':'#287271'}\n"
            "for function,axis in zip(range(1,9),axes.ravel()):\n"
            "    rows=comparison.loc[comparison.function.eq(function)].set_index('method').loc[['UCB','EI','PI']]\n"
            "    x=np.arange(3); axis.errorbar(x,rows.predicted_mean,yerr=rows.predicted_std,fmt='none',ecolor='#555',capsize=4,lw=1.3)\n"
            "    axis.scatter(x,rows.predicted_mean,s=65,c=[colours[m] for m in rows.index],edgecolor='#222',zorder=3)\n"
            "    chosen=strategy.loc[strategy.function.eq(function),'method'].iloc[0]; chosen_x=['UCB','EI','PI'].index(chosen)\n"
            "    axis.scatter(chosen_x,rows.loc[chosen,'predicted_mean'],s=170,facecolors='none',edgecolors='#111',linewidths=2,label='Selected')\n"
            "    axis.set_xticks(x,rows.index); axis.set(title=f'F{function}',ylabel='Predicted objective ± 1 SD'); axis.grid(axis='y',alpha=.22)\n"
            "fig.suptitle('GP predictions at each acquisition method’s leading candidate',fontweight='bold'); fig.tight_layout(); plt.show()"
        ),
        nbf.v4.new_markdown_cell("### Selected function-specific strategies"),
        nbf.v4.new_code_cell(
            "selected=strategy[['function','method','query','kappa','xi_fraction_of_output_std','local_scale','fitted_length_scales','predicted_mean','predicted_std','distance_from_incumbent','reason']]\n"
            "selected"
        ),
        nbf.v4.new_markdown_cell(
            "### Fitted anisotropic length scales\n\n"
            "Shorter fitted length scales indicate faster modelled variation along a coordinate; values at configured bounds should be interpreted cautiously."
        ),
        nbf.v4.new_code_cell(
            "length_scale_matrix=np.full((8,8),np.nan)\n"
            "for row in strategy.itertuples():\n"
            "    values=json.loads(row.fitted_length_scales); length_scale_matrix[int(row.function)-1,:len(values)]=values\n"
            "fig,ax=plt.subplots(figsize=(11,5.2)); image=ax.imshow(length_scale_matrix,aspect='auto',cmap='YlGnBu',vmin=.01,vmax=2)\n"
            "ax.set_xticks(range(8),[f'x{i}' for i in range(1,9)]); ax.set_yticks(range(8),[f'F{i}' for i in range(1,9)])\n"
            "ax.set(title='Fitted Matérn length scales by coordinate',xlabel='Input dimension',ylabel='Function')\n"
            "for i in range(8):\n"
            "    for j in range(8):\n"
            "        if np.isfinite(length_scale_matrix[i,j]): ax.text(j,i,f'{length_scale_matrix[i,j]:.2f}',ha='center',va='center',fontsize=8,color='white' if length_scale_matrix[i,j]>1.2 else '#222')\n"
            "fig.colorbar(image,ax=ax,label='Length scale'); fig.tight_layout(); plt.show()"
        ),
        nbf.v4.new_code_cell(
            "fig,axes=plt.subplots(1,3,figsize=(15,4.2))\n"
            "axes[0].bar(strategy.function.astype(str),strategy.week_12_improvement,color=np.where(strategy.week_12_improvement>0,'#2ca02c','#9aa0a6'))\n"
            "axes[0].axhline(0,color='black',lw=.8); axes[0].set(title='Week 12 improvement over prior best',xlabel='Function',ylabel='Objective improvement')\n"
            "axes[1].bar(strategy.function.astype(str),strategy.predicted_std,color='#6f4e9c'); axes[1].set(title='Uncertainty at selected query',xlabel='Function',ylabel='Predictive standard deviation')\n"
            "axes[2].bar(strategy.function.astype(str),strategy.distance_from_incumbent,color='#26828e'); axes[2].set(title='Distance from incumbent',xlabel='Function',ylabel='Euclidean distance')\n"
            "fig.tight_layout(); plt.show()"
        ),
        nbf.v4.new_markdown_cell("### Submission strings and integrity checks"),
        nbf.v4.new_code_cell(
            "lines=(ROOT/'Week_13/01_Queries/week_13_query_points.txt').read_text().strip().splitlines()\n"
            "for line in lines: print(line)\n"
            "assert len(lines)==8 and len(strategy)==8 and len(comparison)==24\n"
            "for row,line in zip(strategy.itertuples(),lines):\n"
            "    function=int(row.function); query=np.asarray(json.loads(row.query),float)\n"
            "    assert line==f'Function_{function}:'+'-'.join(f'{value:.6f}' for value in query)\n"
            "    assert query.shape==(DIMENSIONS[function],)\n"
            "    assert np.isfinite(query).all() and np.all((query>=0)&(query<=1))\n"
            "    data=ROOT/f'Week_01/Function_{function:02d}/03_Data'\n"
            "    observed=np.load(data/'initial_inputs.npy')\n"
            "    observed=np.vstack([observed]+[np.asarray(q,float)[None,:] for q,_ in pairs_through_week(12,function)])\n"
            "    assert len(observed)==row.verified_observations\n"
            "    assert not np.any(np.all(np.isclose(observed,query,rtol=0,atol=5e-7),axis=1))\n"
            "print('Print week 13 query points')"
        ),
        nbf.v4.new_markdown_cell(
            "## Takeaways\n\n"
            "- Week 12 establishes new verified incumbents for F3, F4, F5, F6 and F7; F2 is close to its existing best and F8 is also near its best.\n"
            "- UCB remains appropriate for F1 and F8 because their useful signal is sparse relative to the search space.\n"
            "- EI or PI provides stronger exploitation for functions whose Week 12 results reinforce promising regions.\n"
            "- The proposed coordinates are not evaluations. They may enter the immutable ledger only after eight aligned platform outputs are returned."
        ),
    ]
    output=root/'Week_13/02_Notebook/Week_13_Optimisation_Strategy.ipynb'
    nbf.write(notebook,output); print(output); return output


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--repository',type=Path,default=Path.cwd())
    build(parser.parse_args().repository.resolve())


if __name__=='__main__': main()
