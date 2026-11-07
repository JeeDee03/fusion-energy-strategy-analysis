"""Build a consolidated review chapter and figures from current project CSVs.
Only writes dedicated generated outputs; never edits research source chapters.
"""
from pathlib import Path
import csv,json,warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

ROOT=Path(__file__).resolve().parent.parent
DATA=ROOT/'data'; REPORTS=ROOT/'reports'; RESEARCH=ROOT/'research'
REPORTS.mkdir(exist_ok=True);RESEARCH.mkdir(exist_ok=True)
def read(name):
    path=DATA/name
    if not path.is_file():
        raise FileNotFoundError(f'Missing {path}. Add the files from the previous enhancement steps first.')
    return pd.read_csv(path,keep_default_na=False)
def table(frame):
    def clean(x): return str(x).replace('|',' / ').replace('\n',' ')
    cols=list(frame.columns)
    lines=['| '+' | '.join(map(clean,cols))+' |','| '+' | '.join(['---']*len(cols))+' |']
    lines += ['| '+' | '.join(clean(v) for v in row)+' |' for row in frame.itertuples(index=False,name=None)]
    return '\n'.join(lines)
companies=read('companies.csv'); funding=read('funding_rounds.csv');snapshots=read('funding_snapshots.csv')
sources=read('sources.csv');milestones=read('milestones.csv'); evidence=read('partnership_evidence.csv');tags=read('partnership_capability_tags.csv')
claims=read('claims.csv');links=read('claim_sources.csv');pc=read('partnership_claims.csv');pl=read('partnership_claim_sources.csv')
for frame,key in [(companies,'company_id'),(funding,'funding_id'),(snapshots,'snapshot_id'),(sources,'source_id'),(milestones,'milestone_id'),(evidence,'partnership_id')]:
    assert frame[key].is_unique, f'Duplicate {key}'
for frame in [funding,snapshots,milestones,evidence]:
    assert frame.company_id.isin(companies.company_id).all(), 'Unknown company reference'
    assert frame.source_id.isin(sources.source_id).all(), 'Unknown source reference'
assert set(tags.partnership_id)==set(evidence.partnership_id), 'Partnership tag coverage differs'
assert not tags.duplicated(['partnership_id','capability']).any()
combined=pd.concat([claims,pc],ignore_index=True)
combined_links=pd.concat([links,pl],ignore_index=True)
assert combined.claim_id.is_unique, 'Claim ID collision across domains'
assert combined_links.claim_id.isin(combined.claim_id).all()
assert combined_links.source_id.isin(sources.source_id).all()
assert not combined_links.duplicated(['claim_id','source_id']).any()
issues=[]
for row in snapshots.itertuples():
    c=claims[claims.entity_id==row.snapshot_id]
    if len(c)!=1: issues.append(f'{row.snapshot_id}: expected one financing claim; found {len(c)}.')
    elif {'company_source_checked': 'original_source_checked'}.get(c.iloc[0].verification_status, c.iloc[0].verification_status) != {'company_source_checked': 'original_source_checked'}.get(row.verification_status, row.verification_status):
        issues.append(f'{row.snapshot_id}: snapshot status {row.verification_status} differs from claim status {c.iloc[0].verification_status}. Review both tables.')
if (claims.verification_status=='pending_review').any():issues.append('One or more financing claims remain pending_review; do not describe all financial claims as verified.')
combined.to_csv(DATA/'all_claims.csv',index=False)
combined_links.to_csv(DATA/'all_claim_sources.csv',index=False)
name=dict(zip(companies.company_id,companies.company_name));source=dict(zip(sources.source_id,sources.url))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
# Equal marker sizes: original-currency values appear as labels, not comparable bubble areas.
f=funding.copy();f['date']=pd.to_datetime(f.announcement_date);f['million']=pd.to_numeric(f.amount_original)/1e6
order=companies.company_id.tolist();ypos={c:i for i,c in enumerate(order)}
fig,ax=plt.subplots(figsize=(12,6))
for i,c in enumerate(order): ax.axhline(i,color='#e7edf0',linewidth=1,zorder=0)
for row in f.itertuples():
    y=ypos[row.company_id];ax.scatter(row.date,y,s=65,color='#176b87',edgecolors='white',zorder=3)
    ax.annotate(f'{row.million:g}m {row.currency}',(row.date,y),xytext=(0,12),textcoords='offset points',ha='center',fontsize=9)
ax.set_yticks(range(len(order)),[name[c] for c in order]);ax.invert_yaxis()
ax.set_ylim(len(order)-.5,-.65)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3));ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.set_xlim(f.date.min()-pd.Timedelta(days=65),f.date.max()+pd.Timedelta(days=65))
ax.set_title('Selected disclosed financing events',pad=20);ax.set_xlabel('Announcement date')
fig.text(.02,.025,'Source: company disclosures in funding_rounds.csv. Equal-sized markers; labels use original currencies. Selected events, not complete histories.',fontsize=8)
fig.tight_layout(rect=(0,.06,1,1));fig.savefig(REPORTS/'funding_event_timeline.png',dpi=180);plt.close(fig)
# Binary map depicts recorded tags, never partnership quality or measured capacity.
label_map={'capital':'Capital','utility_expertise':'Utility expertise','site_access':'Site access','public_support':'Public support','scientific_rd':'Scientific R&D','offtake':'Offtake','manufacturing':'Manufacturing','computing_simulation':'Computing / simulation','technology_supply':'Technology supply'}
unknown=set(tags.capability)-set(label_map)
assert not unknown,f'Unrecognized capability labels: {unknown}'
labels=[x for x in label_map if x in set(tags.capability)]
lookup=evidence.set_index('partnership_id').company_id.to_dict()
counts=pd.DataFrame(0,index=order,columns=labels)
for row in tags.itertuples():counts.loc[lookup[row.partnership_id],row.capability]+=1
binary=(counts>0).astype(int)
fig,ax=plt.subplots(figsize=(12,5.8));ax.imshow(binary,cmap=ListedColormap(['#edf1f3','#176b87']),vmin=0,vmax=1,aspect='auto')
ax.set_yticks(range(len(order)),[name[c] for c in order]);ax.set_xticks(range(len(labels)),[label_map[c] for c in labels],rotation=35,ha='right')
for i in range(len(order)):
    for j in range(len(labels)):
        if binary.iloc[i,j]:ax.text(j,i,'Recorded',ha='center',va='center',color='white',fontsize=8)
ax.set_title('Capabilities documented in the selected partnership sample',pad=15)
fig.text(.02,.02,'Blank = not coded in this sample; not evidence of absence. Multiple tags per relationship. No quality or strength score.',fontsize=8)
fig.tight_layout(rect=(0,.06,1,1));fig.savefig(REPORTS/'partnership_evidence_map.png',dpi=180);plt.close(fig)
summary_path=DATA/'electricity_summary_2024.json'
if not summary_path.is_file():raise FileNotFoundError('Run python src/electricity_market_analysis.py first.')
s=json.loads(summary_path.read_text())
for filename in ['electricity_price_distribution_2024.png','electricity_monthly_2024.png','electricity_price_duration_2024.png']:
    assert (REPORTS/filename).is_file(),f'Missing {filename}; run electricity analysis first.'
sv=snapshots.copy();sv['Company']=sv.company_id.map(name)
sv['Evidence source']=sv.source_id.map(lambda sid:f'[{sid}]({source[sid]})')
sv=sv.rename(columns={'as_of_date':'Reference date','amount_million':'Reported million','currency':'Currency','comparison_basis':'Scope','qualifier':'Qualifier','verification_status':'Review status'})
sv=sv[['Company','Reference date','Reported million','Currency','Scope','Qualifier','Review status','Evidence source']]
coverage=f.groupby('company_id').agg(Recorded_events=('funding_id','count'),First_record=('announcement_date','min'),Last_record=('announcement_date','max')).reset_index()
coverage['Company']=coverage.company_id.map(name);coverage=coverage[['Company','Recorded_events','First_record','Last_record']]
coverage.columns=['Company','Recorded events','First recorded event','Last recorded event']
ev=evidence.copy();ev['Company']=ev.company_id.map(name);ev['Source']=ev.source_id.map(lambda sid:f'[{sid}]({source[sid]})')
ev=ev.rename(columns={'partner_name':'Partner','commitment_form':'Reported form','documented_contribution':'Documented contribution','undisclosed_terms':'Unresolved terms'})
ev=ev[['Company','Partner','Reported form','Documented contribution','Unresolved terms','Source']]
ms=milestones.copy();ms['Company']=ms.company_id.map(name)
ms['Target period']=ms.apply(lambda r:r['target_date'] or r['target_period_text'] or r['target_year'],axis=1)
ms['Source']=ms.source_id.map(lambda sid:f'[{sid}]({source[sid]})')
ms=ms.rename(columns={'project_name':'Project','milestone_name':'Event / target','statement_date':'Statement date','actual_date':'Exact event date','status':'Reported state'})
ms=ms[['Company','Project','Event / target','Statement date','Target period','Exact event date','Reported state','Source']]
issue_text='\n'.join('- '+x for x in issues) if issues else 'No snapshot/claim status mismatches or pending financing claims were detected by these checks. This is not a certification of factual completeness.'
text='''# Stage 1–2 Synthesis: Financing, Partnerships and Electricity-Market Context

*Generated from the current project inputs. Historical company-disclosure cutoff: 24 October 2026. This file is regenerated by src/integrate_stage12.py; make lasting factual edits in the input datasets and methodological edits in the script or source chapters.*

## 1. Research purpose and boundaries

The project asks how Proxima Fusion should position itself technologically, economically and strategically in Europe. This chapter preserves the Stage 1–2 descriptive boundary. Technical benchmarking and conditional economic models are now implemented in Stages 3–4; see [current integrated status](31_research_status_and_claims.md). Those extensions do not change the descriptive scope or validate hypotheses here. The five companies form a purposive case sample, not a representative census. See [research protocol](05_analysis_protocol.md) and [data dictionary](06_data_dictionary.md).

The evidence separates financing events from cumulative disclosures, company funding from project budgets, and announced relationships from demonstrated economic outcomes. It does not rank technical success from capital raised or partnership counts.

## 2. Financing: scope and event chronology

### Table 1. Coverage of selected financing events

'''+table(coverage)+'''

These intervals describe the recorded sample, not a systematic search proving all events were captured. The timeline uses original-currency labels and equal-sized markers; no currency-equivalent funding ranking is encoded.

### Figure 1. Selected financing-event timeline

![Selected financing-event timeline](../reports/funding_event_timeline.png)

### Table 2. Historical cumulative disclosures

'''+table(sv)+'''

Cumulative snapshots include their constituent rounds and must not be summed with them. Different reporting dates, public/private scope and qualifiers prevent a like-for-like financing ranking. An arithmetic residual between selected rounds and a cumulative disclosure does not identify a missing transaction. Lower bounds remain lower bounds; historic totals must not be labeled current without new evidence. See [funding audit](07_funding_audit.md); where its earlier review notes conflict with updated inputs, resolve the inconsistency before publication.

## 3. Partnerships: roles, commitment forms and unresolved terms

### Figure 2. Recorded contribution categories

![Partnership evidence map](../reports/partnership_evidence_map.png)

Each colored cell indicates at least one recorded contribution in the selected sample. Blank cells mean not coded, not absent. The display is binary and does not rank quality, breadth of the full ecosystem, or realized commercial impact. One relationship can contribute several capabilities.

### Table 3. Partnership evidence matrix

'''+table(ev)+'''

An investment, conditional public indication, PPA, service contract and award selection create different obligations. The publicly reported agreement form is not a legal enforceability opinion. Undisclosed prices, liabilities and termination terms remain unknown. Potential reductions in funding burden or execution risk remain mechanisms for later scenario analysis, not established causal results. See [partnership methodology](09_partnership_evidence_analysis.md).

## 4. Development chronology: reported events versus targets

### Table 4. Selected historical milestone observations

'''+table(ms)+'''

Statement dates must not silently become exact event dates. reported_completed records a party's account, not independent verification. Year-only or decade-level targets retain their precision; older schedules are historical observations rather than latest forecasts. This sparse register cannot establish comparative delay rates or technical readiness. See [milestone methodology](08_milestone_methodology.md).

## 5. Electricity-market context

The first empirical baseline covers 2024 DE/LU hourly day-ahead prices. The raw dataset was retrieved in October 2026 and can contain revisions; it is not an archived October 24 vintage. The observations below are author calculations from the retained SMARD series, attributed to Bundesnetzagentur | SMARD.de under CC BY 4.0.

'''
metrics=pd.DataFrame([['Covered hours',str(s['hours'])],['Mean price',f"{s['mean_eur_mwh']:.2f} EUR/MWh"],['Median price',f"{s['median_eur_mwh']:.2f} EUR/MWh"],['Negative-price hours',str(s['negative_price_hours'])],['Negative-price share',f"{s['negative_price_share_pct']:.2f}%"]],columns=['Measure','2024 result'])
text+=table(metrics)+'''

### Figure 3. Monthly prices and negative-price exposure

![Monthly electricity-market context](../reports/electricity_monthly_2024.png)

The time-weighted market mean is not a future sales-price assumption or an LCOE competitiveness threshold. A plant's capture price weights prices by its actual production. Availability, dispatch flexibility and contracts therefore belong in later revenue scenarios. No future distribution is calibrated from this single year's price dispersion. See [electricity baseline](10_electricity_market_baseline.md) for all three price figures, equations, source links, exchange-specific limitations and quality checks.

## 6. Implications for the research hypotheses

| Hypothesis | What this chapter contributes | What remains to be evaluated |
|---|---|---|
| H1 — Technology economics | Historical market context and explicit distinction between generation cost and realized price | Technical parameters, FOAK/NOAK costs, availability, financing and future revenue scenarios |
| H2 — Partnerships | Source-linked contributions and explicit missing contract terms | Allocation of capital, liabilities, retained value and control under defined alternatives |
| H3 — Manufacturing scalability | Recorded manufacturing and technology-supply relationships | Repeatable component costs, learning assumptions, redesign needs and deployment scale |

None of the three hypotheses is validated by descriptive funding or partnership records. Current Stage 3 evidence and Stage 4 conditional models are summarized in [chapter 31](31_research_status_and_claims.md); all three hypotheses remain open.

## 7. Data consistency and open issues

'''+issue_text+'''

The enhanced dataset remains selected and historical. Source review is not audited financial assurance. Missing values, party claims and modeling assumptions must remain distinct. The checks below do not establish exhaustive research coverage or independently demonstrated technological performance.

## 8. Reproduction and document ownership

Run python src/electricity_market_analysis.py before this integration script when refreshing the electricity outputs. Then run python src/integrate_stage12.py. The script generates this chapter, two new figures, data/all_claims.csv and data/all_claim_sources.csv. The combined claim files are derived unions; edit the financing and partnership source tables instead. Existing chapters and original data files are preserved.

This generated chapter is the consolidated Stage 1–2 reading entry point. Keep research/03_market_financing_analysis.md as the detailed financing chapter and the numbered audit/methodology notes as supporting documentation. No automatic replacement of their manually edited text is performed. Final editorial consolidation and publication review remain part of the final report stage.
'''
(RESEARCH/'11_stage12_synthesis.md').write_text(text)
for issue in issues:warnings.warn(issue)
print(f'Integrated {len(companies)} companies, {len(funding)} selected funding events, {len(evidence)} partnership records and {len(milestones)} milestone observations.')
print(f'Generated {len(combined)} combined claims; original claim files preserved.')
print('Saved research/11_stage12_synthesis.md and two new figures.')
print(f'Consistency issues requiring review: {len(issues)}')
