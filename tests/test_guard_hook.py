import json
import pathlib
import subprocess
import unittest

HOOK = pathlib.Path(__file__).resolve().parent.parent / ".claude/hooks/guard-subagent-outward.sh"
AGENT = {"agent_id": "a", "agent_type": "implementer"}


def run(payload):
    data = payload if isinstance(payload, str) else json.dumps(payload)
    return subprocess.run([str(HOOK)], input=data, capture_output=True, text=True).returncode


def bash(cmd, agent=True):
    return run({**(AGENT if agent else {}), "tool_name": "Bash", "tool_input": {"command": cmd}})


class GuardHook(unittest.TestCase):
    def test_main_session_passes(self):
        self.assertEqual(bash("git push origin x", agent=False), 0)

    def test_blocks_subagent_push_and_merge(self):
        for cmd in ["git push origin x", "git -C /tmp/r push -u origin b", "cd r && git merge feat/x",
                    "cd /repo\ngit push", "FOO=1 git push", "env git push", "/usr/bin/git push",
                    'bash -c "git push"', "echo $(git push)", "git push", "gh pr merge 12 --squash",
                    "gh api -X PUT repos/o/r/pulls/1/merge"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(bash(cmd), 2)

    def test_allows_subagent_reads(self):
        for cmd in ["git merge-base main HEAD", "git log --grep=merge", "git status && legit push", "gh pr view 3"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(bash(cmd), 0)

    def test_mcp_tools(self):
        self.assertEqual(run({**AGENT, "tool_name": "mcp__github__merge_pull_request", "tool_input": {}}), 2)
        self.assertEqual(run({**AGENT, "tool_name": "mcp__github__get_issue", "tool_input": {}}), 0)

    def test_fails_closed_on_bad_input(self):
        self.assertEqual(run('{"agent_id": broken'), 2)


if __name__ == "__main__":
    unittest.main()
