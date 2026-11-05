"""Reproduce the 2024 DE/LU historical baseline from bundled SMARD JSON."""
from pathlib import Path
import json, hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent.parent
RAW=ROOT/'data/raw/smard_2024'
REPORTS=ROOT/'reports'
REPORTS.mkdir(exist_ok=True)
manifest=json.loads((RAW/'manifest.json').read_text())
for item in manifest['files']:
    assert hashlib.sha256((RAW/item['file']).read_bytes()).hexdigest()==item['sha256'], 'Raw snapshot changed: '+item['file']
records=[]
for file in sorted(RAW.glob('4169_DE_hour_*.json')):
    for timestamp,price in json.loads(file.read_text())['series']:
        records.append((timestamp,price))
df=pd.DataFrame(records,columns=['timestamp_ms','price_eur_mwh'])
df['interval_start_utc']=pd.to_datetime(df.timestamp_ms,unit='ms',utc=True)
start=pd.Timestamp('2024-01-01',tz='Europe/Berlin').tz_convert('UTC')
end=pd.Timestamp('2025-01-01',tz='Europe/Berlin').tz_convert('UTC')
df=df[(df.interval_start_utc>=start)&(df.interval_start_utc<end)].sort_values('interval_start_utc').copy()
assert not df.interval_start_utc.duplicated().any(), 'Duplicate UTC interval'
expected=pd.date_range(start,end,freq='h',inclusive='left')
assert len(expected)==8784
assert pd.DatetimeIndex(df.interval_start_utc).equals(expected), 'Missing/irregular hourly timestamps'
df['price_eur_mwh']=pd.to_numeric(df.price_eur_mwh,errors='raise')
assert np.isfinite(df.price_eur_mwh).all(), 'Missing/non-finite price; no interpolation allowed'
df['interval_start_local']=df.interval_start_utc.dt.tz_convert('Europe/Berlin')
df['duration_hours']=1.0
df['source_id']='ES001'
df['month']=df.interval_start_local.dt.strftime('%Y-%m')
prices=df.price_eur_mwh.to_numpy()
negative=prices<0
maxrun=run=0
for is_negative in negative:
    run=run+1 if is_negative else 0
    maxrun=max(maxrun,run)
summary={'year':2024,'bidding_zone':'Germany/Luxembourg','hours':len(df),'mean_eur_mwh':float(prices.mean()),'median_eur_mwh':float(np.median(prices)),'population_std_eur_mwh':float(prices.std(ddof=0)),'p05_eur_mwh':float(np.quantile(prices,.05)),'p95_eur_mwh':float(np.quantile(prices,.95)),'min_eur_mwh':float(prices.min()),'max_eur_mwh':float(prices.max()),'negative_price_hours':int(negative.sum()),'negative_price_share_pct':float(100*negative.mean()),'hours_above_100_eur_mwh':int((prices>100).sum()),'longest_negative_run_hours':maxrun}
# Cross-check the raw-series identity against the regulator's published historical summary.
assert round(summary['mean_eur_mwh'],2)==78.51, 'Published mean differs; investigate data revisions'
assert summary['negative_price_hours']==457, 'Published negative-hour count differs; investigate'
assert summary['min_eur_mwh']==-135.45 and summary['max_eur_mwh']==936.28
assert summary['hours_above_100_eur_mwh']==2296
export=df[['interval_start_utc','interval_start_local','duration_hours','price_eur_mwh','source_id']]
export.to_csv(ROOT/'data/electricity_prices_de_lu_2024.csv',index=False)
monthly=df.groupby('month').agg(mean_eur_mwh=('price_eur_mwh','mean'),hours=('price_eur_mwh','size'),negative_price_hours=('price_eur_mwh',lambda x:int((x<0).sum())))
monthly['negative_price_share_pct']=100*monthly.negative_price_hours/monthly.hours
monthly.to_csv(ROOT/'data/electricity_monthly_2024.csv')
(ROOT/'data/electricity_summary_2024.json').write_text(json.dumps(summary,indent=2))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
credit='Source: Bundesnetzagentur | SMARD.de (CC BY 4.0); author calculations. DE/LU, 2024.'
fig,ax=plt.subplots(figsize=(10,5.5))
ax.hist(prices,bins=90,color='#176b87',edgecolor='white',linewidth=.4)
ax.axvline(0,color='#c64747',linewidth=1.5,label='Zero price')
ax.axvline(prices.mean(),color='#df9c27',linewidth=2,label=f'Mean: {prices.mean():.2f} EUR/MWh')
ax.set(title='Hourly day-ahead price distribution',xlabel='Price (EUR/MWh)',ylabel='Hourly intervals')
ax.legend();fig.text(.06,.02,credit,fontsize=8);fig.tight_layout(rect=(0,.05,1,1));fig.savefig(REPORTS/'electricity_price_distribution_2024.png',dpi=160);plt.close(fig)
fig,axes=plt.subplots(2,1,figsize=(10,7),sharex=True)
x=np.arange(len(monthly))
axes[0].bar(x,monthly.mean_eur_mwh,color='#176b87');axes[0].set(ylabel='Mean (EUR/MWh)',title='Monthly day-ahead prices and negative-price exposure')
axes[1].bar(x,monthly.negative_price_share_pct,color='#c64747');axes[1].set(ylabel='Negative-price hours (%)',xlabel='Delivery month, Europe/Berlin')
axes[1].set_xticks(x,[str(i) for i in range(1,13)])
fig.text(.06,.02,credit,fontsize=8);fig.tight_layout(rect=(0,.05,1,1));fig.savefig(REPORTS/'electricity_monthly_2024.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(figsize=(10,5.5))
ax.plot(100*(np.arange(len(prices))+.5)/len(prices),np.sort(prices)[::-1],color='#176b87',linewidth=1.5)
ax.axhline(0,color='#c64747',linewidth=1)
ax.set(title='Day-ahead price duration curve',xlabel='Share of annual hours ranked from highest to lowest price (%)',ylabel='Price (EUR/MWh)')
fig.text(.06,.02,credit,fontsize=8);fig.tight_layout(rect=(0,.05,1,1));fig.savefig(REPORTS/'electricity_price_duration_2024.png',dpi=160);plt.close(fig)
print('Electricity data checks passed: 8,784 hourly intervals; no missing values or duplicate UTC timestamps.')
print(json.dumps(summary,indent=2))
print('Saved processed datasets and three charts; no future price forecast calculated.')
