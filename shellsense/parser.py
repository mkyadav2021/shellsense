"""
Tokenizes and structures shell command strings.

Takes raw input like 'ls -la /tmp' and produces a list of
CommandSegment objects, each representing one command in a pipeline.
"""

import shlex
from dataclasses import dataclass, field


@dataclass
class FlagInfo:
    flag: str
    value: str | None

    @property
    def is_long(self) -> bool:
        return self.flag.startswith("--")


@dataclass
class CommandSegment:
    raw: str
    command: str
    subcommand: str | None = None
    args: list[str] = field(default_factory=list)
    flags: list[FlagInfo] = field(default_factory=list)

# Redirect operators that consume the next token (the filename)
REDIRECT_OPS = {'>', '>>', '2>', '2>>', '&>', '&>>', '<', '<<', '<<<'}
# Redirect operators that don't consume a filename
REDIRECT_NO_TARGET = {'2>&1', '1>&2', '>&2', '>&1'}


def strip_redirects(tokens: list[str]) -> list[str]:
    """Remove redirect operators and their target filenames from a token list."""
    result = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in REDIRECT_NO_TARGET:
            i += 1
            continue
        if token in REDIRECT_OPS:
            i += 2  # skip the operator and the filename after it
            continue
        result.append(token)
        i += 1
    return result


SUBCOMMAND_COMMANDS={
    "git", "docker", "kubectl", "systemctl", "apt", "apt-get",
    "pip", "npm", "cargo", "brew", "journalctl", "ip",
    "podman", "snap", "flatpak", "dnf", "yum", "pacman",
}

FLAGS_WITH_VALUES={
    "-name", "-type", "-mtime", "-atime", "-ctime", "-size",
    "-user", "-group", "-perm", "-exec", "-path", "-iname",
    "-o", "-f", "-d", "-m", "-e", "-i", "-c", "-n", "-p",
    "--output", "--format", "--file", "--config", "--exclude",
    "--include", "--filter", "--sort", "--limit", "--timeout",
    "--user", "--password", "--host", "--port",
}


def split_pipeline(command_string: str) -> list[str]:
    segments = []
    current = []

    try:
        shlex.split(command_string)
    except ValueError:
        return [s.strip() for s in command_string.split("|")]

    in_single_quote = False
    in_double_quote = False

    for char in command_string:
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            current.append(char)
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            current.append(char)
        elif char == "|" and not in_single_quote and not in_double_quote:
            segments.append("".join(current).strip())
            current = []
        else:
            current.append(char)

    if current:
        segments.append("".join(current).strip())

    return [s for s in segments if s]

def expand_short_flags(token: str) -> list[str]:
    if token.startswith("--") or len(token) <= 2:
        return [token]

    # don't treat -7 or -42 as flags
    if token[1:].isdigit():
        return [token]

    return [f"-{char}" for char in token[1:]]


def parse_segment(raw: str) -> CommandSegment:
    try:
        tokens = shlex.split(raw)
    except ValueError:
        tokens = raw.split()

    tokens = strip_redirects(tokens)

    if not tokens:
        return CommandSegment(raw=raw, command="")

    command = tokens[0]
    subcommand = None
    remaining = tokens[1:]

    # Check for subcommands: 'git commit -m "msg"'
    if command in SUBCOMMAND_COMMANDS and remaining:
        # The next token is a subcommand if it doesn't start with -
        if not remaining[0].startswith("-"):
            subcommand = remaining[0]
            remaining = remaining[1:]

    args = []
    flags = []
    i = 0

    while i < len(remaining):
        token = remaining[i]

        if token.startswith("--"):
            # Long flag: --color=auto or --verbose
            if "=" in token:
                flag_name, value = token.split("=", 1)
                flags.append(FlagInfo(flag=flag_name, value=value))
            elif i + 1 < len(remaining) and not remaining[i + 1].startswith("-"):
                # Peek at next token — if it's not a flag, it might be this flag's value
                if token in FLAGS_WITH_VALUES:
                    flags.append(FlagInfo(flag=token, value=remaining[i + 1]))
                    i += 1
                else:
                    flags.append(FlagInfo(flag=token, value=None))
            else:
                flags.append(FlagInfo(flag=token, value=None))

        elif token.startswith("-") and len(token) > 1 and not token[1:].replace(".", "").isdigit():
            # Short flag(s): -la, -n 5, -f file.txt
            # If the full token is a known multi-char flag (e.g. -name, -type),
            # treat it as a single flag rather than expanding character by character.
            if token in FLAGS_WITH_VALUES:
                expanded = [token]
            else:
                expanded = expand_short_flags(token)

            for j, flag in enumerate(expanded):
                # Only the LAST flag in a group can take a value
                is_last = (j == len(expanded) - 1)

                if is_last and flag in FLAGS_WITH_VALUES:
                    if i + 1 < len(remaining) and not remaining[i + 1].startswith("-"):
                        flags.append(FlagInfo(flag=flag, value=remaining[i + 1]))
                        i += 1
                    else:
                        flags.append(FlagInfo(flag=flag, value=None))
                else:
                    flags.append(FlagInfo(flag=flag, value=None))

        else:
            # Positional argument
            args.append(token)

        i += 1

    return CommandSegment(
        raw=raw,
        command=command,
        subcommand=subcommand,
        args=args,
        flags=flags,
    )


def parse_command(command_string: str) -> list[CommandSegment]:
    segments = split_pipeline(command_string)
    return [parse_segment(s) for s in segments]
