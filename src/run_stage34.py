"""Offline, ordered Stage 3–4 rebuild with source and generated-output hashes."""

import os
from pathlib import Path
import subprocess
import sys

from migrate_research_numbering import migrate_research_numbering

from stage34_provenance import (
    ROOT, INPUTS, OUTPUTS, STEPS, SUMMARY, environment, hashes,
    input_paths, now, write_json, check_review_alignment,
)


def main():
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    state = {"schema_version": 1, "status": "running", "started_at_utc": now(),
             "steps": [], "input_hashes": {}, "output_hashes": {},
             "interpretation": "Execution and consistency only; assumptions remain unvalidated."}
    # Invalidate an older successful record before any preflight or mutation.
    write_json(ROOT / SUMMARY, state)
    try:
        if sys.flags.optimize or os.environ.get("PYTHONOPTIMIZE") not in (None, "", "0"):
            raise RuntimeError("Disable Python optimization: existing validators use assert.")
        required = set(INPUTS) | {"src/" + name for name in STEPS}
        required |= {"src/stage34_provenance.py", "src/stage4_reconciliation.py",
                     "src/lcoe_model.py", "src/project_cash_flow.py",
                     "src/prepare_milestone_review.py", "src/economic_validation.py"}
        missing = sorted(name for name in required if not (ROOT / name).is_file())
        if missing:
            raise FileNotFoundError("Missing required files: " + ", ".join(missing))
        numbering = migrate_research_numbering(ROOT)
        if numbering == "renamed":
            print("Research numbering corrected: economic assumptions document is now 27.", flush=True)
        check_review_alignment(ROOT)
        state["environment"] = environment()
        state["input_hashes"] = hashes(ROOT, input_paths(ROOT))
        write_json(ROOT / SUMMARY, state)
        child_env = os.environ.copy()
        child_env["MPLBACKEND"] = "Agg"
        with (reports / "stage34_run.log").open("w", encoding="utf-8") as log:
            for script in STEPS:
                print("Running " + script, flush=True)
                item = {"script": script, "started_at_utc": now()}
                state["steps"].append(item)
                log.write("\n### " + script + "\n")
                log.flush()
                result = subprocess.run([sys.executable, str(ROOT / "src" / script)],
                                        cwd=ROOT, env=child_env, stdout=log,
                                        stderr=subprocess.STDOUT)
                item.update(exit_code=result.returncode, finished_at_utc=now())
                if result.returncode:
                    raise RuntimeError(f"{script} failed ({result.returncode}); see reports/stage34_run.log")
        if hashes(ROOT, input_paths(ROOT)) != state["input_hashes"]:
            raise RuntimeError("Source inputs, scripts, or human review changed during rebuild.")
        if environment() != state["environment"]:
            raise RuntimeError("Dependency versions changed during rebuild.")
        state["output_hashes"] = hashes(ROOT, OUTPUTS)
        state["status"] = "passed_with_limitations"
        state["finished_at_utc"] = now()
        write_json(ROOT / SUMMARY, state)
        print("Rebuild finished: passed_with_limitations")
        print(f"Steps passed: {len(STEPS)}/{len(STEPS)}")
        print("Log: reports/stage34_run.log")
        print("Environment and hashes: " + SUMMARY)
        print("Human editorial review and economic calibration remain required.")
        return 0
    except Exception as exc:
        state.update(status="failed", error=str(exc), finished_at_utc=now())
        write_json(ROOT / SUMMARY, state)
        print("FAILED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
