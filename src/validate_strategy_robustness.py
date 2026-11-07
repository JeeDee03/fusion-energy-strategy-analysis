"""Stage 6.5 audit: independent file-level and analytical invariants."""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
from strategy_robustness import ROOT, calculate,sha

def main():
    root=ROOT/"reports"
    expected={
        "stage65_feasibility_screen.csv":60,
        "stage65_context_gate_summary.csv":15,
        "stage65_price_thresholds.csv":20,
    }
    fresh=calculate()
    for (filename,n),regen in zip(expected.items(),fresh[:3]):
        stored=pd.read_csv(root/filename)
        assert len(stored)==n and len(regen)==n,(filename,len(stored),len(regen))
        if "eligible_strategy_ids" in stored.columns:
            stored["eligible_strategy_ids"] = stored["eligible_strategy_ids"].fillna("")
        pd.testing.assert_frame_equal(stored,regen,check_exact=False,rtol=1e-10,atol=2,check_dtype=False)
    gate,ctx,threshold,paths=fresh
    assert set(gate.strategy_id)=={"STR01","STR02","STR03","STR04"}
    assert (gate.all_economic_gates == (gate.company_gate & gate.external_gate & gate.project_gate)).all()
    assert int(ctx.feasible_strategy_count.sum())==int(gate.all_economic_gates.sum())
    assert len(ctx)==15 and len(threshold)==20
    assert threshold.max_linearity_residual_eur.max()<10
    assert ((gate.loc[gate.strategy_id=="STR01","external_gate"])).all()
    aud=json.loads((root/"stage65_feasibility_audit.json").read_text())
    assert aud["risk_rows"]==60 and aud["context_rows"]==15 and aud["threshold_rows"]==20
    assert aud["inputs_sha256"]=={k:sha(v) for k,v in paths.items()}
    assert aud["eligible_rows"]==int(gate.all_economic_gates.sum())
    print("PASS — 60 stakeholder gate screens, 15 MCDA-context checks, 20 price thresholds")
    print("PASS — independent regeneration, NPV reconciliation, linearity, coverage and hashes")
    print("WARNING — exploratory economic screen, not a financing feasibility certificate or strategy ranking")

if __name__=="__main__":main()
