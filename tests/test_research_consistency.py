"""Editorial anchors and cross-stage invalidation; mutations stay in temp fixtures."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT/'src'))
import research_consistency as research
import stage12_provenance as p12
import stage34_provenance as p34
import run_stage14
from check_stage14_freshness import freshness_issues


class ResearchConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        names = set(p12.input_paths(PROJECT)) | set(p12.GENERATED) | set(p34.input_paths(PROJECT)) | set(p34.OUTPUTS)
        for name in names:
            target = self.root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT/name, target)

        # Stage 7 publication links in the README must also
        # resolve inside the temporary project fixture.
        tracked_paper_files = subprocess.run(
            ["git", "ls-files", "--", "paper/"],
            cwd=PROJECT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()

        for relative in tracked_paper_files:
            source = PROJECT / relative
            if not source.is_file():
                continue

            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        # Synthetic records isolate record checks; the real combined runner is
        # exercised separately on the complete supplied project, not mocked here.
        self.r12 = {'schema_version':1,'status':'passed','evidence_issues':[],
                    'python':sys.version,'packages':{n:p12.metadata.version(n) for n in p12.PACKAGES},
                    'steps':[{'script':s,'exit_code':0} for s in p12.STEPS],
                    'input_hashes':p34.hashes(self.root,p12.input_paths(self.root)),
                    'output_hashes':p34.hashes(self.root,p12.GENERATED)}
        self.r34 = {'schema_version':1,'status':'passed_with_limitations','environment':p34.environment(),
                    'steps':[{'script':s,'exit_code':0} for s in p34.STEPS],
                    'input_hashes':p34.hashes(self.root,p34.input_paths(self.root)),
                    'output_hashes':p34.hashes(self.root,p34.OUTPUTS)}
        self.save_records()

    def save_records(self):
        p34.write_json(self.root/p12.SUMMARY,self.r12)
        p34.write_json(self.root/p34.SUMMARY,self.r34)

    def edit_json(self,name,update):
        p=self.root/name;r=json.loads(p.read_text());update(r);p.write_text(json.dumps(r))

    def test_current_anchors_documents_and_both_records(self):
        self.assertEqual(research.audit(self.root)['errors'],[])
        self.assertEqual(freshness_issues(self.root),[])

    def test_hypothesis_wording_disagreement(self):
        p=self.root/'research/01_research_proposal.md'
        p.write_text(p.read_text().replace('may compensate','will compensate'))
        self.assertTrue(any('wording' in e for e in research.audit(self.root)['errors']))

    def test_confirmation_rejected_even_if_all_documents_changed(self):
        self.edit_json('data/research_status.json',lambda r:r['hypotheses'][0].update(status='confirmed'))
        for name in research.DOCUMENTS:
            p=self.root/name;p.write_text(p.read_text().replace('Status: **open**.','Status: **confirmed**.',1))
        self.assertTrue(any('unsupported confirmation' in e for e in research.audit(self.root)['errors']))

    def test_future_stage_cannot_be_marked_complete(self):
        self.edit_json('data/research_status.json',lambda r:r['stages'][4].update(status='completed'))
        self.assertTrue(any('Stage status' in e for e in research.audit(self.root)['errors']))

    def test_missing_hypothesis_assessment_rejected(self):
        self.edit_json('data/research_status.json',lambda r:r['hypotheses'][1].update(next_evidence=''))
        self.assertTrue(research.audit(self.root)['errors'])

    def test_changed_numeric_result_requires_editorial_reconciliation(self):
        p=self.root/'reports/lifecycle_summary.csv'
        p.write_text(p.read_text().replace('213.42','999.42'))
        # CSV retains full precision; change the selected value independently.
        import csv
        with p.open(newline='') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
        for row in rows:
            if row['scenario_id']=='LC004':row['break_even_eur_2024_per_mwh']='999'
        with p.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
        self.assertTrue(any('anchor differs' in e for e in research.audit(self.root)['errors']))

    def test_duplicate_anchor_selector_rejected(self):
        self.edit_json('data/research_findings.json',lambda r:r[3].update(where={'scenario_id':'LR020'}))
        self.assertTrue(any('nonunique' in e for e in research.audit(self.root)['errors']))

    def test_empirical_label_rejected(self):
        self.edit_json('data/research_findings.json',lambda r:r[0].update(classification='measured_cost'))
        self.assertTrue(any('classification' in e for e in research.audit(self.root)['errors']))

    def test_broken_local_link_detected(self):
        p=self.root/'research/31_research_status_and_claims.md'
        p.write_text(p.read_text()+'\n[missing](absent.md)\n')
        self.assertTrue(any('unresolved' in e for e in research.audit(self.root)['errors']))

    def test_shared_company_change_invalidates_both_records(self):
        p=self.root/'data/companies.csv';p.write_text(p.read_text()+'\n')
        issues=freshness_issues(self.root)
        self.assertTrue(any('Stage 1–2' in e and 'companies.csv' in e for e in issues))
        self.assertTrue(any('Changed input: data/companies.csv' in e for e in issues))

    def test_refreshed_stage34_cannot_hide_stale_stage12(self):
        p=self.root/'data/companies.csv';p.write_text(p.read_text()+'\n')
        self.r34['input_hashes']=p34.hashes(self.root,p34.input_paths(self.root));self.save_records()
        self.assertEqual(p34.freshness_issues(self.root),[])
        self.assertTrue(p12.freshness_issues(self.root))

    def test_incomplete_stage12_hash_set_rejected(self):
        self.r12['input_hashes'].pop('data/companies.csv');self.save_records()
        self.assertTrue(any('file set' in e for e in freshness_issues(self.root)))

    def test_failed_stage12_rejected(self):
        self.r12['status']='failed';self.save_records()
        self.assertTrue(freshness_issues(self.root))

    def test_incomplete_stage12_steps_rejected(self):
        self.r12['steps'].pop();self.save_records()
        self.assertTrue(any('step coverage' in e for e in freshness_issues(self.root)))

    def test_stage12_environment_change_rejected(self):
        self.r12['packages']['tabulate']='different';self.save_records()
        self.assertTrue(any('versions' in e for e in freshness_issues(self.root)))

    def test_raw_snapshot_tampering_rejected(self):
        raw=next((self.root/'data/raw/smard_2024').glob('4169*.json'))
        raw.write_text(raw.read_text()+'\n')
        self.assertTrue(any('snapshot hash mismatch' in e for e in freshness_issues(self.root)))

    def test_checks_do_not_refresh_records(self):
        paths=[self.root/p12.SUMMARY,self.root/p34.SUMMARY]
        before=[(p.read_bytes(),p.stat().st_mtime_ns) for p in paths]
        freshness_issues(self.root);research.audit(self.root)
        self.assertEqual(before,[(p.read_bytes(),p.stat().st_mtime_ns) for p in paths])

    def test_failed_stage12_attempt_invalidates_previous_success(self):
        (self.root/'data/funding_rounds.csv').unlink()
        result=subprocess.run([sys.executable,'src/run_stage12.py'],cwd=self.root,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        record=json.loads((self.root/p12.SUMMARY).read_text())
        self.assertEqual(record['status'],'failed')
        self.assertTrue(p12.freshness_issues(self.root))

    def test_document_paths_discovered_after_numbering_migration(self):
        from migrate_research_numbering import OLD, NEW
        (self.root/'research'/NEW).rename(self.root/'research'/OLD)
        code = (
            "import sys; sys.path.insert(0,'src'); "
            "import stage34_provenance as p; "
            "from migrate_research_numbering import migrate_research_numbering, OLD, NEW; "
            "migrate_research_numbering(p.ROOT); names=p.input_paths(p.ROOT); "
            "assert 'research/'+OLD not in names; assert 'research/'+NEW in names; "
            "p.hashes(p.ROOT,names)"
        )
        result=subprocess.run([sys.executable,'-c',code],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_combined_runner_stops_after_first_failure(self):
        with patch.object(run_stage14.subprocess,'run',return_value=subprocess.CompletedProcess([],7)) as run:
            self.assertEqual(run_stage14.main(),7)
            self.assertEqual(run.call_count,1)

    def test_combined_runner_dependency_order(self):
        with patch.object(run_stage14.subprocess,'run',return_value=subprocess.CompletedProcess([],0)) as run:
            self.assertEqual(run_stage14.main(),0)
            self.assertEqual([Path(c.args[0][1]).name for c in run.call_args_list],list(run_stage14.STEPS))


if __name__=='__main__':
    unittest.main(verbosity=2)
