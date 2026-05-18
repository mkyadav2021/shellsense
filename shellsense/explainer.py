from dataclasses import dataclass, field

from shellsense.parser import CommandSegment, parse_command
from shellsense import knowledge, manpage, tldr, cache


@dataclass
class FlagExplanation:
   
    flag: str
    value: str | None
    explanation: str
    source: str          # Where we found this: "builtin", "man", "tldr"


@dataclass
class CommandExplanation:
   
    command: str
    subcommand: str | None
    description: str
    args: list[str]
    flags: list[FlagExplanation]
    examples: list[dict] = field(default_factory=list)
    source: str = "unknown"


def _get_help_output(command: str) -> dict | None:
    import subprocess

    try:
        result = subprocess.run(
            [command, "--help"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        text = result.stdout or result.stderr
        if text:
            # Just grab the first meaningful line as description
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            description = lines[0] if lines else f"Command: {command}"
            return {"description": description, "flags": {}}
    except (FileNotFoundError, subprocess.TimeoutExpired, PermissionError):
        pass

    return None


def explain_segment(segment: CommandSegment) -> CommandExplanation:
    command = segment.command
    description = f"Command: {command}"
    flag_db: dict[str, str] = {}
    examples: list[dict] = []
    source = "unknown"

    # 1. Built-in knowledge base
    kb = knowledge.lookup(command, segment.subcommand)
    if kb:
        description = kb["description"]
        flag_db = kb.get("flags", {})
        source = "builtin"

        if segment.subcommand and "subcommand_description" in kb:
            description += f" → {kb['subcommand_description']}"

    # 2. Check cache (only if builtin didn't have enough info)
    if not flag_db:
        cached = cache.get(command)
        if cached:
            description = cached.get("description", description)
            flag_db = cached.get("flags", {})
            examples = cached.get("examples", [])
            source = cached.get("source", "cache")

    # 3. Man pages
    if not flag_db:
        man = manpage.parse_man_page(command)
        if man is None:
            # Try shell builtins
            man = manpage.get_builtin_help(command)

        if man:
            if source == "unknown":
                description = man.description
            flag_db = man.flags
            source = "man"

            # Cache the result
            cache.put(command, {
                "description": man.description,
                "flags": man.flags,
                "source": "man",
            })

    # 4. tldr pages — only fetch when we lack flags or a description
    if source == "unknown" or not flag_db:
        tldr_data = tldr.get_tldr(command)
        if tldr_data:
            if source == "unknown":
                description = tldr_data.get("description", description)
            examples = tldr_data.get("examples", [])

            if not flag_db:
                source = "tldr"
                cache.put(command, {
                    "description": description,
                    "flags": {},
                    "examples": examples,
                    "source": "tldr",
                })

    # 5. --help fallback
    if source == "unknown":
        help_data = _get_help_output(command)
        if help_data:
            description = help_data["description"]
            source = "help"

    # Now match the parsed flags against our flag database
    flag_explanations = []
    for flag_info in segment.flags:
        explanation = flag_db.get(flag_info.flag, "")

        if not explanation:
            explanation = "(no description found)"

        flag_explanations.append(FlagExplanation(
            flag=flag_info.flag,
            value=flag_info.value,
            explanation=explanation,
            source=source,
        ))

    return CommandExplanation(
        command=command,
        subcommand=segment.subcommand,
        description=description,
        args=segment.args,
        flags=flag_explanations,
        examples=examples,
        source=source,
    )


def explain(command_string: str) -> list[CommandExplanation]:
   
    segments = parse_command(command_string)
    return [explain_segment(s) for s in segments]