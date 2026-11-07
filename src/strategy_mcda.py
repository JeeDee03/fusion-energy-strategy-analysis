"""Stage 6.4 exploratory PARTIAL MCDA (C01-C04 ONLY).

Requires preexisting Stage 6.2/6.3 results. Does not estimate company strategy
success, contractual viability, debt financing or full eight-criterion ranking.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DATA = ROOT / "data"
STRATEGIES = {"STR01", "STR02", "STR03", "STR04"}
CRITERIA = {"C01", "C02", "C03", "C04"}
PRICE_CASES = {"P120", "P170", "P200"}
STRESSES = {"RS00", "RS01", "RS02", "RS03", "RS04"}


def require_file(path):
    if not path.is_file():
        raise FileNotFoundError(f"Missing input: {path}. Run Stage 6.2/6.3 first.")
    return path


def load_inputs(root=ROOT):
    root = Path(root)
    result = pd.read_csv(require_file(root / "reports/stage63_risk_allocation_results.csv"))
    value = pd.read_csv(require_file(root / "reports/stage62_value_capture_results.csv"))
    sc = pd.read_csv(require_file(root / "data/strategy_value_capture_scenarios.csv"))
    weights = pd.read_csv(require_file(root / "data/strategy_mcda_weights.csv"))
    evidence = pd.read_csv(require_file(root / "data/strategy_mcda_evidence_register.csv"))
    expected = {"strategy_id", "price_case", "stress_id", "company_stressed_npv_eur", "company_baseline_npv_eur", "capex_risk_company_share", "price_risk_company_share"}
    if not expected.issubset(result.columns):
        raise ValueError(f"Missing Stage 6.3 fields: {sorted(expected-set(result.columns))}")
    if len(result) != 60 or result.duplicated(["strategy_id", "price_case", "stress_id"]).any():
        raise ValueError("Stage 6.3 must have 60 unique strategy/price/stress rows")
    if set(result.strategy_id) != STRATEGIES or set(result.price_case) != PRICE_CASES or set(result.stress_id) != STRESSES:
        raise ValueError("Unexpected Stage 6.3 coverage")
    if len(value) != 12 or value.duplicated(["strategy_id", "price_case"]).any():
        raise ValueError("Stage 6.2 must have 12 unique strategy/price rows")
    if set(sc.strategy_id) != STRATEGIES or len(sc) != 4 or sc.strategy_id.duplicated().any():
        raise ValueError("Expected four unique strategy assumptions")
    if (result[["company_stressed_npv_eur", "capex_risk_company_share", "price_risk_company_share"]].isna().any().any()
        or not np.isfinite(result[["company_stressed_npv_eur", "capex_risk_company_share", "price_risk_company_share"]]).all().all()):
        raise ValueError("Nonfinite financial inputs")
    for share in ("capex_risk_company_share", "price_risk_company_share"):
        if not result[share].between(0, 1).all():
            raise ValueError(f"Invalid risk share: {share}")
    if not sc.equity_fraction.between(0, 1).all():
        raise ValueError("Invalid ownership share")
    merged = result.merge(value[["strategy_id", "price_case", "company_npv_eur"]], on=["strategy_id", "price_case"], validate="many_to_one")
    base = merged[merged.stress_id == "RS00"]
    if not np.allclose(base.company_stressed_npv_eur, base.company_npv_eur, rtol=1e-12, atol=0.1):
        raise ValueError("Stage 6.2/6.3 baseline reconciliation failed")
    if not set(weights.columns) == {"weight_set", "criterion_id", "weight", "assumption_class"}:
        raise ValueError("Weight CSV schema mismatch")
    for ws, w in weights.groupby("weight_set"):
        if len(w) != 4 or set(w.criterion_id) != CRITERIA or w.criterion_id.duplicated().any():
            raise ValueError(f"Invalid criteria coverage: {ws}")
        if (w.weight < 0).any() or not np.isfinite(w.weight).all() or not np.isclose(w.weight.sum(),1,atol=1e-12):
            raise ValueError(f"Weights must sum to 1: {ws}")
    if len(evidence) != 8 or set(evidence.criterion_id) != {f"C{i:02d}" for i in range(1,9)} or evidence.criterion_id.duplicated().any():
        raise ValueError("Evidence must classify all 8 criteria")
    if set(evidence.loc[evidence.mcda_status.str.startswith("included"), "criterion_id"]) != CRITERIA:
        raise ValueError("Unexpected qualitative scoring status")
    return result, sc, weights, evidence


def score_group(group, scenario, policy):
    """Within scenario min-max scores, no cross-context cardinal interpretation."""
    df = group.sort_values("strategy_id").copy()
    vals = {
        "C01": -df.equity_fraction.to_numpy(dtype=float),
        "C02": df.company_stressed_npv_eur.to_numpy(dtype=float),
        "C03": -df.capex_risk_company_share.to_numpy(dtype=float),
        "C04": -df.price_risk_company_share.to_numpy(dtype=float),
    }
    out = {}
    for cid, v in vals.items():
        spread = float(np.ptp(v))
        out[cid] = (v-v.min())/spread if spread > 1e-9 else np.full(len(v),0.5)
    result = pd.DataFrame({"strategy_id":df.strategy_id.values,"price_case":scenario[0], "stress_id":scenario[1], "weight_set":policy})
    for cid, x in out.items():
        result[f"score_{cid}"] = x
    return result


def calculate(root=ROOT):
    results, strategies, weights, evidence = load_inputs(root)
    rows = results.merge(strategies[["strategy_id", "equity_fraction"]], on="strategy_id",validate="many_to_one")
    frames=[]
    for (price,stress), part in rows.groupby(["price_case","stress_id"],sort=True):
        if len(part) != 4:
            raise ValueError(f"Incomplete comparison scenario {price}, {stress}")
        for policy, w in weights.groupby("weight_set"):
            f=score_group(part,(price,stress),policy)
            wm=w.set_index("criterion_id").weight.to_dict()
            f["composite_score"] = sum(float(wm[c])*f[f"score_{c}"] for c in sorted(CRITERIA))
            f["rank_dense"] = f.composite_score.rank(method="dense",ascending=False).astype(int)
            f["scope_label"] = "PARTIAL_FOUR_CRITERIA_EXPLORATORY_SCREENING_NOT_STRATEGY_RANKING"
            frames.append(f)
    scores=pd.concat(frames,ignore_index=True)
    expected_len=4*3*5*len(weights.weight_set.unique())
    assert len(scores)==expected_len
    # Detect whether the leaders depend on weighting assumptions; ties retained.
    leaders=scores[scores.rank_dense==1]
    robustness=(leaders.groupby(["price_case","stress_id"])
                .agg(num_leading_strategies=("strategy_id","nunique"),
                     top_strategy_ids=("strategy_id",lambda s:";".join(sorted(set(s)))))
                .reset_index())
    robustness["weight_sensitive"] = robustness.num_leading_strategies>1
    return scores,robustness


def main():
    REPORTS.mkdir(parents=True,exist_ok=True)
    scores,robustness=calculate()
    p1=REPORTS/"stage64_partial_mcda_scores.csv"
    p2=REPORTS/"stage64_weight_robustness.csv"
    scores.to_csv(p1,index=False)
    robustness.to_csv(p2,index=False)
    sources=[DATA/"strategy_mcda_weights.csv",DATA/"strategy_mcda_evidence_register.csv",
             DATA/"strategy_value_capture_scenarios.csv",REPORTS/"stage62_value_capture_results.csv",
             REPORTS/"stage63_risk_allocation_results.csv"]
    audit={"status":"PARTIAL_SCREENING_COMPLETED_NOT_FULL_MCDA",
           "scored_criteria":["C01","C02","C03","C04"],
           "excluded_or_pending":["C05","C06","C07","C08"],
           "scenarios":15,"weight_sets":int(scores.weight_set.nunique()),"score_rows":len(scores),
           "scenarios_with_different_leaders_across_weight_sets":int(robustness.weight_sensitive.sum()),
           "source_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
           "limitations":["Ownership fraction is a capital exposure proxy, not actual capital-at-risk.",
                          "Risk fractions are hypothetical contractual allocations, not observed risk.",
                          "C01 and C03 may overlap economically; their weights are subjective and must be stress-tested.",
                          "C05 excluded due to overlapping financing risk; C06-C08 lack defensible scores.",
                          "Min-max scores are relative to alternatives within each price/stress scenario.",
                          "The 4-criterion scores are not comparable across price/stress contexts.",
                          "Supplier sales and markups presume customer viability; no debt, default, contract certainty or financing waterfalls.",
                          "Do not interpret highest weighted score as a verified strategic recommendation."]}
    p3=REPORTS/"stage64_partial_mcda_audit.json"
    p3.write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    print("Stage 6.4:",audit["status"])
    print("Score rows:",len(scores),"| Weight-sensitive contexts:",int(robustness.weight_sensitive.sum()),"of 15")
    print("P170 / RS04 — provisional score illustration:")
    print(scores[(scores.price_case=="P170")&(scores.stress_id=="RS04")][["weight_set","strategy_id","composite_score","rank_dense"]].to_string(index=False))
    print("Outputs:",p1.name,p2.name,p3.name)

if __name__=="__main__":
    main()
