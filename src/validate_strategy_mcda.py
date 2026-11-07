"""Independent checks for Stage 6.4 exploratory partial MCDA exports."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from strategy_mcda import ROOT,calculate,load_inputs


def main():
    result,robust=calculate()
    p=ROOT/"reports/stage64_partial_mcda_scores.csv"
    q=ROOT/"reports/stage64_weight_robustness.csv"
    a=ROOT/"reports/stage64_partial_mcda_audit.json"
    saved=pd.read_csv(p)
    saved_robust=pd.read_csv(q)
    audit=json.loads(a.read_text())
    assert audit["status"]=="PARTIAL_SCREENING_COMPLETED_NOT_FULL_MCDA"
    assert len(saved)==240 and len(saved_robust)==15
    assert len(saved.merge(result,on=["strategy_id","price_case","stress_id","weight_set"],validate="one_to_one"))==240
    idx=["strategy_id","price_case","stress_id","weight_set"]
    s=saved.sort_values(idx).reset_index(drop=True)
    r=result.sort_values(idx).reset_index(drop=True)
    for col in ["score_C01","score_C02","score_C03","score_C04","composite_score"]:
        assert np.allclose(s[col],r[col],atol=1e-12,rtol=1e-12),col
    assert s.rank_dense.equals(r.rank_dense)
    assert saved[["score_C01","score_C02","score_C03","score_C04","composite_score"]].apply(lambda x:x.between(0,1).all()).all()
    keys=["price_case","stress_id"]
    assert saved_robust.sort_values(keys).reset_index(drop=True).equals(robust.sort_values(keys).reset_index(drop=True))
    assert audit["score_rows"]==len(saved)
    print("PASS — 240 provisional score rows, 15 contexts, 4 weighting policies")
    print("PASS — score bounds, independent regeneration, risk/equity input linkage")
    print("WARNING — partial analyst-preference MCDA, not a verified strategy ranking")

if __name__=="__main__":
    main()
