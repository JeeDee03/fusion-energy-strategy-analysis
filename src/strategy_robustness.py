"""Stage 6.5: stakeholder-viability gates and linear price thresholds.

Conditional screening, not empirical deal feasibility or full strategic rankings.
Uses Stage 6.3 stakeholder NPVs and Stage 6.4 provisional MCDA outputs.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
P = ("P120", "P170", "P200")
S = ("RS00", "RS01", "RS02", "RS03", "RS04")
IDS = ("STR01", "STR02", "STR03", "STR04")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inputs(root=ROOT):
    root=Path(root)
    paths={
        "risk": root/"reports/stage63_risk_allocation_results.csv",
        "mcda": root/"reports/stage64_partial_mcda_scores.csv",
        "policies": root/"data/strategy_feasibility_policies.csv",
    }
    for p in paths.values():
        if not p.exists(): raise FileNotFoundError(f"Missing {p}; run Stage 6.3/6.4 or install Stage 6.5 CSV.")
    r=pd.read_csv(paths["risk"]); m=pd.read_csv(paths["mcda"]); pol=pd.read_csv(paths["policies"])
    npv_cols=["company_stressed_npv_eur", "external_stressed_npv_eur", "stressed_project_npv_eur", "incremental_company_cost_pv_eur"]
    required={"strategy_id","price_case","stress_id",*npv_cols}
    if not required.issubset(r.columns): raise ValueError(f"Missing risk columns {sorted(required-set(r.columns))}")
    if len(r)!=60 or r.duplicated(["strategy_id","price_case","stress_id"]).any(): raise ValueError("Risk file must contain 60 unique scenarios")
    if set(r.strategy_id)!=set(IDS) or set(r.price_case)!=set(P) or set(r.stress_id)!=set(S):raise ValueError("Risk coverage mismatch")
    if not np.isfinite(r[npv_cols].to_numpy(dtype=float)).all():raise ValueError("Nonfinite risk values")
    if len(m)!=240 or m.duplicated(["strategy_id","price_case","stress_id","weight_set"]).any():raise ValueError("MCDA must contain 240 unique rows")
    if not {"strategy_id","price_case","stress_id","weight_set","composite_score","rank_dense"}.issubset(m.columns):raise ValueError("MCDA missing columns")
    if set(m.strategy_id)!=set(IDS) or set(m.price_case)!=set(P) or set(m.stress_id)!=set(S):raise ValueError("MCDA coverage mismatch")
    if len(pol)!=1 or pol.iloc[0]["policy_id"]!="FP01":raise ValueError("Expected one explicit exploratory policy FP01")
    q=pol.iloc[0]
    if float(q["company_min_npv_eur"])!=0 or float(q["external_min_npv_eur"])!=0 or float(q["project_min_npv_eur"])!=0:
        raise ValueError("This version requires zero-NPV gates")
    if q["integrated_external_rule"]!="not_applicable":raise ValueError("STR01 must have no external-investor gate")
    for _,v in r.iterrows():
        err=v.company_stressed_npv_eur + v.external_stressed_npv_eur - (v.stressed_project_npv_eur-v.incremental_company_cost_pv_eur)
        if abs(err)>max(2,abs(v.stressed_project_npv_eur)*1e-9): raise ValueError("Stakeholder NPV reconciliation failure")
    return r,m,pol,paths


def screening(r,m):
    z=r.copy()
    z["company_gate"]=z.company_stressed_npv_eur>=0
    z["external_gate"]=np.where(z.strategy_id=="STR01",True,z.external_stressed_npv_eur>=0)
    z["project_gate"]=z.stressed_project_npv_eur>=0
    z["stakeholder_joint_gate"]=z.company_gate & z.external_gate
    z["all_economic_gates"]=z.stakeholder_joint_gate & z.project_gate
    z["policy_status"]=np.where(z.all_economic_gates,"PASSES_EXPLORATORY_ECONOMIC_GATES","FAILS_AT_LEAST_ONE_ECONOMIC_GATE")
    leaders=m[m.rank_dense==1].groupby(["price_case","stress_id"]).strategy_id.agg(lambda x: ';'.join(sorted(set(x)))).reset_index(name="provisional_mcda_leaders")
    overview=z.groupby(["price_case","stress_id"]).agg(feasible_strategy_count=("all_economic_gates","sum")).reset_index().merge(leaders,on=["price_case","stress_id"],how="left",validate="one_to_one")
    overview["eligible_strategy_ids"]=[";".join(sorted(part.loc[part.all_economic_gates,"strategy_id"])) for _,part in z.groupby(["price_case","stress_id"],sort=True)]
    overview["provisional_leader_viable"]=[bool(any(x in eligible.split(';') for x in leader.split(';'))) for eligible,leader in zip(overview.eligible_strategy_ids,overview.provisional_mcda_leaders)]
    overview["interpretation"]=np.where(overview.feasible_strategy_count>0,"EVALUATE_ELIGIBLE_STRATEGIES_ONLY","NO_ECONOMICALLY_ELIGIBLE_STRATEGY_NO_RECOMMENDATION")
    return z,overview


def thresholds(r):
    out=[]
    for (sid,stress),g in r.groupby(["strategy_id","stress_id"],sort=True):
        d=g.set_index("price_case")
        if set(d.index)!=set(P):raise ValueError("Missing price cases")
        rec={"strategy_id":sid,"stress_id":stress}
        limits=[]; errors=[]
        for label,col in [("company","company_stressed_npv_eur"),("external","external_stressed_npv_eur"),("project","stressed_project_npv_eur")]:
            x1,x2=120.,200.
            y1,y2=float(d.loc["P120",col]),float(d.loc["P200",col])
            slope=(y2-y1)/(x2-x1)
            yp=y1+slope*(170.-x1)
            residual=abs(float(d.loc["P170",col])-yp)
            tol=max(2.,max(abs(y1),abs(y2))*1e-9)
            if residual>tol:raise ValueError(f"Price-NPV nonlinearity {sid}/{stress}/{label}: {residual}")
            errors.append(residual)
            rec[f"{label}_npv_slope_eur_per_eur_mwh"]=slope
            if label=="external" and sid=="STR01":
                rec[f"{label}_break_even_price_eur_mwh"]=np.nan
                continue
            if slope<=1e-9:
                req= -np.inf if min(y1,y2)>=0 else np.inf
            else: req=x1-y1/slope
            rec[f"{label}_break_even_price_eur_mwh"]=req
            limits.append(req)
        rec["joint_economic_threshold_price_eur_mwh"]=max(limits)
        threshold=rec["joint_economic_threshold_price_eur_mwh"]
        rec["threshold_location"]=("WITHIN_TESTED_120_TO_200" if 120<=threshold<=200 else "EXTRAPOLATED_ABOVE_200" if threshold>200 else "BELOW_TESTED_120")
        rec["max_linearity_residual_eur"]=max(errors)
        rec["interpretation"]="ZERO_NPV_GATES_NO_CUSTOMER_FINANCING_OR_CONTRACT_FEASIBILITY"
        out.append(rec)
    return pd.DataFrame(out)


def calculate(root=ROOT):
    r,m,p,paths=inputs(root)
    return (*screening(r,m),thresholds(r),paths)


def main():
    gate,context,threshold,paths=calculate()
    output=ROOT/"reports";output.mkdir(exist_ok=True)
    gate.to_csv(output/"stage65_feasibility_screen.csv",index=False)
    context.to_csv(output/"stage65_context_gate_summary.csv",index=False)
    threshold.to_csv(output/"stage65_price_thresholds.csv",index=False)
    audit={"status":"CONDITIONAL_ECONOMIC_GATES_COMPLETE_NOT_STRATEGY_RECOMMENDATION", "risk_rows":len(gate),"context_rows":len(context),"threshold_rows":len(threshold),"eligible_rows":int(gate.all_economic_gates.sum()),"contexts_with_eligible_strategy":int((context.feasible_strategy_count>0).sum()),"inputs_sha256":{name:sha(path) for name,path in paths.items()}, "limits":["Zero NPV is a screening convention, not a bankability or financing criterion", "Thresholds above tested prices are linear extrapolations of the toy scenario", "Supplier customer contract remains assumed, not validated", "No default, warranty, debt, manufacturing investment, or qualitative C06-C08 scores", "No probability weights assigned to prices, stresses or strategies"]}
    (output/"stage65_feasibility_audit.json").write_text(json.dumps(audit,indent=2)+"\n")
    print("Stage 6.5:",audit["status"])
    print(f"{len(gate)} screened rows; {int(gate.all_economic_gates.sum())} pass; {int((context.feasible_strategy_count>0).sum())}/15 contexts have any eligible strategy")
    print("\nBreak-even contractual price thresholds (EUR/MWh) under RS00:")
    print(threshold[threshold.stress_id=="RS00"][["strategy_id","company_break_even_price_eur_mwh","external_break_even_price_eur_mwh","joint_economic_threshold_price_eur_mwh","threshold_location"]].to_string(index=False,float_format=lambda x:f"{x:.2f}"))
    print("WARNING — This model does not certify supplier demand, financing or an optimal business model.")

if __name__=="__main__":main()
