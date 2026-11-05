"""Optional refresh; offline analysis uses the bundled raw SMARD snapshot."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, urllib.request, hashlib
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent.parent
RAW=ROOT/'data/raw/smard_2024'
RAW.mkdir(parents=True,exist_ok=True)
BASE='https://www.smard.de/app/chart_data/4169/DE/'

def fetch(name):
    data=urllib.request.urlopen(BASE+name,timeout=30).read()
    json.loads(data)
    (RAW/name).write_bytes(data)
    return {'file':name,'url':BASE+name,'sha256':hashlib.sha256(data).hexdigest()}

if __name__=='__main__':
    index=fetch('index_hour.json')
    stamps=json.loads((RAW/'index_hour.json').read_text())['timestamps']
    tz=ZoneInfo('Europe/Berlin')
    start=int(datetime(2024,1,1,tzinfo=tz).timestamp()*1000)
    end=int(datetime(2025,1,1,tzinfo=tz).timestamp()*1000)
    selected=[t for i,t in enumerate(stamps) if t<end and (i+1==len(stamps) or stamps[i+1]>start)]
    names=[f'4169_DE_hour_{t}.json' for t in selected]
    with ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(fetch,names))
    manifest={'access_date':datetime.now(tz).date().isoformat(),'series_id':'4169','region':'DE','bidding_zone':'Germany/Luxembourg','resolution':'hour','attribution':'Bundesnetzagentur | SMARD.de','license':'CC BY 4.0','license_url':'https://creativecommons.org/licenses/by/4.0/','data_use_url':'https://www.smard.de/en/datennutzung','files':[index]+results}
    (RAW/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(f'Downloaded {len(results)} data blocks. Run analysis separately.')
