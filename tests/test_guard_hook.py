import json
import os
import tempfile
import pathlib
import subprocess
import unittest

HOOK = pathlib.Path(__file__).resolve().parent.parent / ".claude/hooks/guard-subagent-outward.sh"
AGENT = {"agent_id": "a", "agent_type": "implementer"}


def run(payload, allow=None):
    data = payload if isinstance(payload, str) else json.dumps(payload)
    env = {**os.environ, "GUARD_MCP_ALLOW": str(allow)} if allow else None
    return subprocess.run([str(HOOK)], input=data, capture_output=True, text=True, env=env).returncode


REPO = HOOK.parents[2]


def call(tool, **tool_input):
    return run({**AGENT, "tool_name": tool, "cwd": str(REPO), "tool_input": tool_input})


def bash(cmd, agent=True):
    return run({**(AGENT if agent else {}), "tool_name": "Bash", "cwd": str(HOOK.parents[2]), "tool_input": {"command": cmd}})


class GuardHook(unittest.TestCase):
    def test_main_session_passes(self):
        self.assertEqual(bash("git push origin x", agent=False), 0)

    def test_blocks_subagent_push_and_merge(self):
        for cmd in ["git push origin x", "git -C /tmp/r push -u origin b", "cd r && git merge feat/x",
                    "cd /repo\ngit push", "FOO=1 git push", "env git push", "/usr/bin/git push",
                    'bash -c "git push"', "echo $(git push)", "git push", "gh pr merge 12 --squash",
                    "gh api -X PUT repos/o/r/pulls/1/merge", "gh -R o/r pr merge 1", "gh pr --repo o/r merge 1",
                    "git \\\npush"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(bash(cmd), 2)

    def test_allows_subagent_reads(self):
        for cmd in ["git merge-base main HEAD", "git log --grep=merge", "git status && legit push", "gh pr view 3"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(bash(cmd), 0)

    def test_mcp_tools_need_allowlisting(self):
        for tool in ["mcp__github__merge_pull_request", "mcp__x__mergePullRequest", "mcp__notion__notion-create-pages",
                     "mcp__github__get_issue", "mcp__x__create__y"]:
            with self.subTest(tool=tool):
                self.assertEqual(run({**AGENT, "tool_name": tool, "tool_input": {}}), 2)

    def test_allowlisted_mcp_tool_passes(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt") as allow:
            allow.write("# comment\nmcp__docs__search\n")
            allow.flush()
            self.assertEqual(run({**AGENT, "tool_name": "mcp__docs__search", "tool_input": {}}, allow.name), 0)
            self.assertEqual(run({**AGENT, "tool_name": "mcp__docs__search_all", "tool_input": {}}, allow.name), 2)

    def test_mutating_gh_api_and_push_variants(self):
        for cmd in ["gh api graphql -f query=x", "gh api repos/o/r/issues -F title=x", "gh api repos/o/r --input x.json",
                    "gh api repos/o/r -X put", "git send-pack origin main", "git -c alias.x=push x origin main"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(bash(cmd), 2)
        for cmd in ["gh api repos/o/r/pulls", "gh api repos/o/r -X GET"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(bash(cmd), 0)

    def test_parsed_bash_rules(self):
        for cmd in ["gh api x -ftitle=x", "gh api -X 'DELETE' x", 'gh api --method="PATCH" x', 'gh api x "-f" e=1',
                    "git -c 'alias.x=push' x", "GIT_CONFIG_COUNT=1 git x", "gh pr review 1 --approve",
                    "gh pr comment 1 -b x", "gh repo delete o/r --yes", "curl -X POST https://x", "env curl x",
                    "git pull", "cat .ENV", "echo x > .claude/HOOKS/guard.py", "scripts/with-env.sh TOKEN -- env"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(bash(cmd), 2)
        for cmd in ["git diff -- src/merge.py", "git log -- scripts/push.sh", "git grep -n push",
                    "gh pr view 3 --json body", "gh pr diff 3", "gh pr checks 3", "git diff -- .claude/settings.json",
                    "python3 -m pytest", "npm test", "grep -rn process.env src",
                    "cat > n.txt <<'EOF'\nit's fine; git push is just text\nEOF"]:
            with self.subTest(cmd=cmd):
                self.assertEqual(bash(cmd), 0)

    def test_secrets_and_guard_files(self):
        self.assertEqual(call("Read", file_path="/r/.env.local"), 2)
        self.assertEqual(call("Grep", pattern="KEY", path="/r/.env"), 2)
        self.assertEqual(bash("cat .env.local"), 2)
        self.assertEqual(call("Read", file_path="/r/.env.local.example"), 0)
        self.assertEqual(bash("cat .env.local.example"), 0)
        self.assertEqual(call("Read", file_path="/r/src/env.py"), 0)
        self.assertEqual(bash("node -e process.env.NODE_ENV"), 0)
        self.assertEqual(call("Edit", file_path=f"{REPO}/.claude/./hooks/mcp-allow.txt"), 2)
        self.assertEqual(call("Write", file_path=f"{REPO}/.Claude/Settings.local.json"), 2)
        self.assertEqual(call("Write", file_path=f"{REPO}/.claude/agents/researcher.md"), 2)
        self.assertEqual(call("Write", file_path=f"{REPO}/.git/config"), 2)
        self.assertEqual(call("Write", file_path=f"{REPO}/workspace/worktrees/skunkworks/b/.claude/hooks/guard.py"), 0)
        self.assertEqual(call("Grep", pattern="KEY", path="/r", glob=".env*"), 2)
        self.assertEqual(call("Read", file_path="/r/.ENV"), 2)
        self.assertEqual(call("Grep", pattern="process\\.env\\.\\w*", path="/r/src"), 0)
        self.assertEqual(bash("echo x >> .claude/hooks/mcp-allow.txt"), 2)
        self.assertEqual(call("Edit", file_path="/r/src/app.py"), 0)

    def test_main_session_mcp_passes(self):
        self.assertEqual(run({"tool_name": "mcp__github__merge_pull_request", "tool_input": {}}), 0)

    def test_registered_fail_closed_for_bash_and_mcp(self):
        hook = json.loads((HOOK.parents[1] / "settings.json").read_text())["hooks"]["PreToolUse"][0]
        for tool in ("Bash", "Read", "Grep", "Edit", "Write", "mcp__.*"):
            self.assertIn(tool, hook["matcher"].split("|"))
        self.assertEqual(hook["hooks"][0]["onFailure"], "block")

    def test_fails_closed_on_bad_input(self):
        for payload in ['{"agent_id": broken', '["agent_id"]', '{"agent_id": "a", "tool_input": "x"}',
                        '{"agent_id": "a", "tool_name": "Bash", "tool_input": {"command": 5}}']:
            with self.subTest(payload=payload):
                self.assertEqual(run(payload), 2)
        self.assertEqual(run('{"agent_id": "a", "tool_name": null, "tool_input": {"command": null}}'), 0)


if __name__ == "__main__":
    unittest.main()
