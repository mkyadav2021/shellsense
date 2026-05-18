import subprocess
import re
from dataclasses import dataclass


@dataclass
class ManPageResult:
    
    description: str
    flags: dict[str, str]   # flag -> explanation
    found: bool = True


def get_man_text(command: str) -> str | None:
    
    try:
        result = subprocess.run(
            ["man", command],
            capture_output=True,
            text=True,
            timeout=5,
            env={"PATH": "/usr/bin:/bin", "MANWIDTH": "120", "LANG": "C"},
        )
        if result.returncode != 0:
            return None

        # 'col -b' strips backspace-based formatting that man uses for bold/underline
        cleaned = subprocess.run(
            ["col", "-b"],
            input=result.stdout,
            capture_output=True,
            text=True,
        )
        return cleaned.stdout

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def extract_description(text: str) -> str:
    # Look for the NAME section
    name_match = re.search(
        r"^NAME\s*\n(.+?)(?=\n[A-Z]{2,})",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not name_match:
        return "No description available"

    name_text = name_match.group(1).strip()

    # The description is usually after " - " or " — "
    dash_match = re.search(r"\s+[-–—]\s+(.+)", name_text)
    if dash_match:
        # Clean up whitespace and newlines
        desc = " ".join(dash_match.group(1).split())
        return desc

    return name_text.split("\n")[0].strip()


def extract_flags(text: str) -> dict[str, str]:
    flags = {}

    # Find the OPTIONS section (or DESCRIPTION as fallback)
    options_match = re.search(
        r"^(OPTIONS|DESCRIPTION)\s*\n(.+?)(?=\n[A-Z]{2,}\s*\n|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not options_match:
        return flags

    options_text = options_match.group(2)

    # Pattern: lines starting with whitespace then a dash (flag definitions)
    # Followed by indented description lines
    flag_pattern = re.compile(
        r"^\s{1,8}(-\S+(?:,\s*-\S+)*(?:\s+\S+)?)\s*\n"  # Flag line
        r"((?:\s{8,}.*\n?)*)",                               # Description lines
        re.MULTILINE,
    )

    for match in flag_pattern.finditer(options_text):
        flag_line = match.group(1).strip()
        desc_lines = match.group(2).strip()

        # Extract individual flags from lines like "-f, --force"
        individual_flags = re.findall(r"(-{1,2}[\w][\w-]*)", flag_line)

        # Clean up the description: join lines and remove excess whitespace
        description = " ".join(desc_lines.split())

        # Truncate very long descriptions to keep output readable
        if len(description) > 200:
            description = description[:197] + "..."

        for flag in individual_flags:
            if flag not in flags:  # Don't overwrite if we already found it
                flags[flag] = description if description else "No description available"

    return flags


def parse_man_page(command: str) -> ManPageResult | None:
    text = get_man_text(command)
    if text is None:
        return None

    description = extract_description(text)
    flags = extract_flags(text)

    return ManPageResult(
        description=description,
        flags=flags,
    )


# Shell builtins that don't have their own man pages
BUILTINS = {
    "cd", "alias", "unalias", "export", "source", ".", "echo", "printf",
    "read", "type", "which", "bg", "fg", "jobs", "set", "unset",
    "pushd", "popd", "dirs", "history", "eval", "exec", "exit",
    "return", "shift", "trap", "wait", "getopts", "declare", "local",
    "readonly", "let", "ulimit", "umask", "shopt",
}


def get_builtin_help(command: str) -> ManPageResult | None:
    """
    Use 'help' to get info on shell builtins.

    'help cd' gives a much cleaner output than digging through bash's man page.
    """
    if command not in BUILTINS:
        return None

    try:
        result = subprocess.run(
            ["bash", "-c", f"help {command}"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None

        text = result.stdout
        lines = text.strip().split("\n")

        # First line is usually: "cd: cd [-L|-P] [dir]"
        # Description follows
        description = ""
        flags = {}

        for i, line in enumerate(lines):
            stripped = line.strip()
            if i == 0:
                continue  # Skip the usage line
            if stripped and not description:
                description = stripped
            # Look for option lines
            option_match = re.match(r"\s+(--?[\w-]+)\s+(.+)", line)
            if option_match:
                flags[option_match.group(1)] = option_match.group(2).strip()

        return ManPageResult(
            description=description or f"Shell builtin: {command}",
            flags=flags,
        )

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None