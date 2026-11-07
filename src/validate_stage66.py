"""Independently check Stage 6.6 saved outputs against source reports."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from integrate_stage66 import ROOT,FILES,file_hash,analyze

def main():
    ev,ctx,summary=analyze(ROOT)
    p=ROOT/'reports'
    saved_ev=pd.read_csv(p/'stage66_strategy_evidence_matrix.csv')
    saved_ctx=pd.read_csv(p/'stage66_context_synthesis.csv')
    pd.testing.assert_frame_equal(saved_ev,ev,check_dtype=False,check_exact=False,rtol=1e-12,atol=1e-6)
    pd.testing.assert_frame_equal(saved_ctx,ctx,check_dtype=False,check_exact=False,rtol=1e-12,atol=1e-6)
    audit=json.loads((p/'stage66_synthesis_audit.json').read_text())
    assert audit['derived_summary']==summary, 'Audit summary differs from regenerated calculations'
    for name,digest in audit['source_hashes_sha256'].items():
        assert name in FILES and file_hash(ROOT/FILES[name])==digest, f'Source hash mismatch: {name}'
    md=(p/'stage66_synthesis_summary.md').read_text()
    assert summary['status'] in md and f"**{summary['eligible_scenarios']}**" in md
    assert len(saved_ev)==4 and len(saved_ctx)==15
    print('PASS — Source coverage, Stage 6.3/6.5 NPV reconciliation and regenerated synthesis')
    print('PASS — 4 strategy evidence rows, 15 contexts, checked source hashes and narrative key metrics')
    print('WARNING — Strategic viability and actual financing arrangements remain unverified')

if __name__=='__main__':main()
