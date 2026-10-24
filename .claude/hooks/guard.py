"""Guard for subagent tool calls (docs/agents.md#safety-subagents-cant-act-outward).

Reads a PreToolUse payload on stdin. Exit 0 allows, exit 2 blocks (reason on
stderr). Only called for payloads with an agent_id; any error blocks.
"""
import json
import os
import re
import shlex
import sys

ALLOW_FILE = os.environ.get("GUARD_MCP_ALLOW") or os.path.join(os.path.dirname(__file__), "mcp-allow.txt")
LIVE_ROOT = os.path.normcase(os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())).lower()
NETWORK = {"curl", "wget", "ssh", "scp", "sftp", "rsync", "nc", "ncat", "netcat", "telnet", "ftp", "socat"}
WRAPPERS = {"env", "command", "exec", "nohup", "time", "sudo", "nice", "timeout", "xargs", "stdbuf"}
SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "eval"}
WRITERS = {"tee", "cp", "mv", "rm", "chmod", "chown", "ln", "install", "truncate", "dd", "touch", "mkdir", "rmdir"}
GIT_OUTWARD = {"push", "merge", "pull", "send-pack"}
GH_READ = {"pr": {"view", "diff", "checks", "list", "status"}, "issue": {"view", "list", "status"},
           "run": {"view", "list"}, "workflow": {"view", "list"}, "repo": {"view"},
           "release": {"view", "list"}, "search": None, "status": None}


class Blocked(Exception):
    pass


def is_secret(text):
    """A .env-style credential file (.env, .env.local, …), except the committed example."""
    name = os.path.basename(str(text).rstrip("/")).lower()
    return name.startswith(".env") and not name.endswith(".example")


def guarded(path, cwd):
    """The live checkout's guard, settings and agents, and any repo's git config or hooks."""
    full = os.path.normcase(os.path.realpath(os.path.join(cwd, os.path.expanduser(str(path))))).lower()
    live = full.startswith(LIVE_ROOT + "/.claude/") and \
        re.match(r"(hooks|agents)/|settings[^/]*\.json$", full[len(LIVE_ROOT) + 9:])
    return bool(live or re.search(r"/\.git/(config|hooks/)", full + "/"))


def check_tool(tool, args, cwd):
    paths = [str(args.get(k) or "") for k in ("file_path", "path", "notebook_path", "glob")]
    if tool == "Glob":
        paths.append(str(args.get("pattern") or ""))
    if tool in ("Read", "Grep", "Glob", "NotebookRead") and any(is_secret(p) or re.search(r"(^|/)\.e[\w*?\[\]{}]*$", p.lower())
                                                               for p in paths if p):
        raise Blocked(".env files hold credentials and are main-session only.")
    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        path = args.get("file_path") or args.get("notebook_path") or ""
        if guarded(path, cwd):
            raise Blocked("the guard, settings, agents and git config are main-session only.")


def commands(text):
    """Split a shell string into simple commands (token lists), recursing into $(…), `…` and -c strings.
    Heredoc bodies are data, so they're dropped before parsing."""
    text = re.sub(r"<<-?\s*(['\"]?)(\w+)\1([^\n]*)\n.*?\n\s*\2\s*(?=\n|$)", r"\3", text, flags=re.S)
    for inner in re.findall(r"\$\(([^()]*)\)|`([^`]*)`", text):
        yield from commands(inner[0] or inner[1])
    lexer = shlex.shlex(text.replace("\\\n", " ").replace("\n", ";"), posix=True, punctuation_chars=";&|()<>")
    lexer.whitespace_split = True
    current = []
    for token in lexer:
        if token and set(token) <= set(";&|()\n"):
            if current:
                yield current
            current = []
        else:
            current.append(token)
    if current:
        yield current


def check_command(tokens, cwd):
    # Leading assignments, then wrappers like env/sudo.
    while tokens and (re.match(r"^\w+=", tokens[0]) or os.path.basename(tokens[0]) in WRAPPERS):
        if tokens[0].upper().startswith("GIT_CONFIG"):
            raise Blocked("git config overrides are main-session only.")
        tokens = tokens[1:]
        while tokens and tokens[0].startswith("-") and os.path.basename(tokens[0]) not in WRAPPERS:
            tokens = tokens[1:]
    if not tokens:
        return
    prog, args = os.path.basename(tokens[0]).lower(), tokens[1:]
    if prog in SHELLS:
        for i, a in enumerate(args):
            if a == "-c" and i + 1 < len(args) or prog == "eval":
                for cmd in commands(" ".join(args[i + 1:] if a == "-c" else args)):
                    check_command(cmd, cwd)
                break
    if prog == "with-env.sh":
        raise Blocked("with-env.sh loads credentials and is main-session only.")
    if prog in NETWORK:
        raise Blocked(f"{prog} is main-session only (network).")
    if prog == "git":
        i = 0
        while i < len(args) and args[i].startswith("-"):
            if args[i] in ("-c", "-C", "--git-dir", "--work-tree", "--namespace") and i + 1 < len(args):
                if args[i] == "-c" and "alias." in args[i + 1].lower():
                    raise Blocked("git aliases are main-session only.")
                i += 1
            elif "alias." in args[i].lower():
                raise Blocked("git aliases are main-session only.")
            i += 1
        sub = args[i].lower() if i < len(args) else ""
        if sub in GIT_OUTWARD or (sub == "config" and any("alias." in a.lower() for a in args)):
            raise Blocked(f"git {sub} is reserved for the main session.")
    if prog == "gh":
        rest = [a for a in args]
        while rest and rest[0].startswith("-"):
            rest = rest[2:] if rest[0] in ("-R", "--repo", "--hostname") else rest[1:]
        group = rest[0] if rest else ""
        if group == "api":
            joined = " ".join(rest[1:])
            if re.search(r"(?:^|\s)(?:-[fF]|--field|--raw-field|--input)", joined) or "graphql" in joined or \
                    re.search(r"(?:-X|--method)[\s=]*(?!get\b)\w", joined, re.I):
                raise Blocked("only GET gh api calls are allowed for subagents.")
        elif group not in GH_READ or (GH_READ[group] is not None and (len(rest) < 2 or rest[1] not in GH_READ[group])):
            raise Blocked(f"gh {' '.join(rest[:2])} is main-session only; subagents may only read.")
    if any(is_secret(a) for a in args):
        raise Blocked(".env files hold credentials and are main-session only.")
    targets = [args[i + 1] for i, a in enumerate(args[:-1]) if a in (">", ">>")]
    if prog in WRITERS or prog in ("sed", "perl") and any(a.startswith("-i") for a in args):
        targets += [a for a in args if not a.startswith("-")]
    if any(guarded(t, cwd) for t in targets):
        raise Blocked("the guard, settings, agents and git config are main-session only.")


def main():
    data = json.load(sys.stdin)
    if not isinstance(data, dict):
        raise Blocked("guard hook got unexpected input.")
    if not data.get("agent_id"):
        return 0
    tool = data.get("tool_name") or ""
    args = data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    if not isinstance(args, dict):
        raise Blocked("guard hook got unexpected tool input.")
    if tool.startswith("mcp__"):
        try:
            lines = open(ALLOW_FILE).read().splitlines()
        except OSError:
            lines = []
        if tool not in {l.strip() for l in lines if l.strip() and not l.startswith("#")}:
            raise Blocked(f"{tool} is not in .claude/hooks/mcp-allow.txt; MCP tools are main-session only unless allowlisted.")
        return 0
    check_tool(tool, args, cwd)
    if tool == "Bash":
        command = args.get("command") or ""
        if not isinstance(command, str):
            raise Blocked("guard hook got an unexpected command.")
        for cmd in commands(command):
            check_command(cmd, cwd)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Blocked as err:
        sys.stderr.write(f"Blocked: {err}\n")
        sys.exit(2)
    except Exception as err:  # fail closed
        sys.stderr.write(f"Blocked: guard hook error ({type(err).__name__}).\n")
        sys.exit(2)
