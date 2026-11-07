"""Plot Stage 5.2 pilot distributions for one specified structural context.

Usage: python src/plot_stage52_pilot.py --n 128 --seed 20261105
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main(n,seed,context,outdir):
    outdir = Path(outdir) if outdir else ROOT/'reports'
    suffix=f'seed{seed}_n{n}'
    path=outdir/f'stage52_draws_{suffix}.csv'
    df=pd.read_csv(path)
    group=df.loc[df['context_id'].eq(context)]
    if len(group)!=n:
        raise ValueError(f'Expected {n} draws for {context}; found {len(group)}')
    plots=[
        ('break_even_eur_2024_per_mwh','Lifecycle break-even price (EUR 2024/MWh)','break_even'),
        ('npv_eur_2024','Project NPV (EUR 2024)','npv'),
    ]
    for column,xlabel,tag in plots:
        fig,ax=plt.subplots(figsize=(8,5))
        ax.hist(group[column],bins=min(30,max(5,int(n**0.5))))
        ax.set_title(f'Stage 5.2 exploratory pilot: {context}')
        ax.set_xlabel(xlabel)
        ax.set_ylabel('Simulated draws')
        if tag=='npv':
            ax.axvline(0,linestyle='--',linewidth=1)
        fig.text(.5,.015,'Conditional exploratory draws; not a probability forecast',ha='center',fontsize=8)
        fig.tight_layout(rect=[0,.04,1,1])
        output=outdir/f'stage52_{tag}_{context}_{suffix}.png'
        fig.savefig(output,dpi=160)
        plt.close(fig)
        print('Saved:',output)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n',type=int,default=128)
    parser.add_argument('--seed',type=int,default=20261105)
    parser.add_argument('--context',default='GEN002_LC004_R05')
    parser.add_argument('--outdir',type=Path,default=None)
    args=parser.parse_args()
    main(args.n,args.seed,args.context,args.outdir)
