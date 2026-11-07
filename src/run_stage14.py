"""Refresh shared-source consumers in order; retain separate logs and records."""
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
STEPS = ('run_stage12.py','check_stage12_closure.py','run_stage34.py','check_stage14_freshness.py')


def main():
    for script in STEPS:
        print('\nStage 1–4: '+script, flush=True)
        result = subprocess.run([sys.executable, str(ROOT/'src'/script)], cwd=ROOT)
        if result.returncode:
            print('Stopped at '+script+'; inspect the corresponding report/log.', file=sys.stderr)
            return result.returncode
    return 0


if __name__ == '__main__':
    sys.exit(main())
