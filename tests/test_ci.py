"""Structural checks on the shared CI workflows and caller templates (docs/ci.md#rules)."""
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS = sorted((ROOT / ".github/workflows").glob("*.yml"))
TEMPLATES = sorted((ROOT / "ci/templates").glob("*.yml"))
EXTRAS = sorted((ROOT / "ci/templates/extras").glob("*.yml"))
STACKS = ("python", "node", "go", "rust")
USES = re.compile(r"^\s*(?:- )?uses: (\S+)(?: # (\S+))?$")
ANY_USES = re.compile(r"^\s*(?:- )?uses:", re.M)
RUN = re.compile(r"^(\s*(?:- )?)run:(.*)$")


def run_blocks(text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if m := RUN.match(line):
            body = [m.group(2)]
            for l in lines[i + 1:]:
                if l.strip() and len(l) - len(l.lstrip()) <= len(m.group(1)):
                    break
                body.append(l)
            yield "\n".join(body)


class CiFiles(unittest.TestCase):
    def test_every_action_is_sha_pinned_with_a_version(self):
        pins = {}
        for f in WORKFLOWS + TEMPLATES + EXTRAS:
            lines = [l for l in f.read_text().splitlines() if ANY_USES.match(l)]
            self.assertTrue(all(USES.match(l) for l in lines), f"{f.name}: a uses: line isn't `ref` or `ref # version`")
            for ref, version in (USES.match(l).groups() for l in lines):
                with self.subTest(file=f.name, ref=ref):
                    if ref.startswith("./"):
                        self.assertTrue((ROOT / ref).exists())
                        continue
                    name, _, sha = ref.partition("@")
                    if name.startswith("OWNER/skunkworks/"):
                        self.assertEqual((sha, version), ("SHA", "VERSION"))
                        self.assertTrue((ROOT / name.split("/", 2)[2].replace("STACK", "python")).exists())
                        continue
                    self.assertRegex(sha, r"^[0-9a-f]{40}$")
                    self.assertTrue(version)
                    self.assertEqual(pins.setdefault(name, sha), sha, "same action pinned to different SHAs")

    def test_jobs_have_timeouts_and_read_only_defaults(self):
        for f in WORKFLOWS + TEMPLATES + EXTRAS:
            text = f.read_text()
            with self.subTest(file=f.name):
                if f not in EXTRAS:
                    self.assertIn("\npermissions:\n  contents: read\n", text)
                self.assertEqual(text.count("actions/checkout@"), text.count("persist-credentials: false"))
                self.assertNotIn("pull_request_target", text)
                for job in re.split(r"\n  (?=[\w-]+:\n)", text.split("\njobs:\n", 1)[-1]):
                    if "runs-on:" in job:
                        self.assertRegex(job, r"\n    timeout-minutes: \d+\n", "a job without its own timeout")

    def test_templates_gate_needs_every_other_job(self):
        for f in TEMPLATES + [ROOT / ".github/workflows/ci.yml"]:
            text = f.read_text()
            jobs = re.findall(r"^  ([\w-]+):\n", text.split("\njobs:\n", 1)[1], re.M)
            needs = re.search(r"ci-ok:\n    needs: \[(.*?)\]", text).group(1).split(", ")
            gate = text.split("  ci-ok:\n", 1)[1]
            with self.subTest(file=f.name):
                self.assertEqual(sorted(needs), sorted(j for j in jobs if j != "ci-ok"))
                self.assertIn("ci-gate.yml", gate)
                self.assertIn("    if: always()\n", gate)
                self.assertIn("      actions: read\n", gate)
                self.assertIn("concurrency:", text)

    def test_every_stack_has_a_shared_workflow(self):
        self.assertIn("/ci-STACK.yml@SHA", (ROOT / "ci/templates/ci.yml").read_text())
        for stack in STACKS:
            with self.subTest(stack=stack):
                self.assertTrue((ROOT / f".github/workflows/ci-{stack}.yml").exists())

    def test_stage_jobs_skip_when_their_commands_are_empty(self):
        conds = {"lint": "inputs.lint != '' || inputs.typecheck != ''", "test": "inputs.test != ''", "audit": "inputs.audit != ''"}
        for stack in STACKS:
            text = (ROOT / f".github/workflows/ci-{stack}.yml").read_text()
            jobs = re.findall(r"^  ([\w-]+):\n    if: (.*)\n", text.split("\njobs:\n", 1)[1], re.M)
            with self.subTest(stack=stack):
                self.assertEqual(dict(jobs), conds)

    def test_tools_are_downloaded_and_verified_not_built(self):
        for f in WORKFLOWS + TEMPLATES + EXTRAS:
            for run in run_blocks(f.read_text()):
                with self.subTest(file=f.name):
                    self.assertNotIn("go run", run)
                    if re.search(r"\b(?:curl|wget)\b", run):
                        self.assertIn("sha256sum -c", run)

    def test_renovate_configs_parse(self):
        for f in (ROOT / "renovate.json", ROOT / "ci/templates/renovate.json"):
            self.assertIn("helpers:pinGitHubActionDigests", json.loads(f.read_text())["extends"])


if __name__ == "__main__":
    unittest.main()
