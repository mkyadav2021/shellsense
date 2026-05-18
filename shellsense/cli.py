import sys

from shellsense.explainer import explain
from shellsense.formatter import format_explanation
from shellsense import cache

from rich.console import Console

console = Console()

HELP = """\
Usage:
  shellsense "<command>"       Explain a shell command
  shellsense clear-cache       Clear all cached explanations
  shellsense status            Show cache statistics

Examples:
  shellsense 'ls -la /tmp'
  shellsense 'ps aux | grep nginx | head -5'
  shellsense 'git commit -m "initial"'
"""


def main():
    args = sys.argv[1:]

    if not args:
        console.print(HELP)
        sys.exit(1)

    first = args[0]

    if first == "clear-cache":
        count = cache.clear()
        console.print(f"[green]Cleared {count} cached entries.[/]")
        return

    if first == "status":
        cache_dir = cache.CACHE_DIR
        if cache_dir.exists():
            entries = list(cache_dir.glob("*.json"))
            console.print(f"[cyan]Cache directory:[/] {cache_dir}")
            console.print(f"[cyan]Cached commands:[/] {len(entries)}")
            for entry in sorted(entries):
                console.print(f"  {entry.stem}")
        else:
            console.print("[dim]No cache directory found.[/]")
        return

    # "shellsense explain ls -la" or "shellsense 'ls -la'"
    if first == "explain":
        command_string = " ".join(args[1:])
    else:
        command_string = first

    if not command_string.strip():
        console.print(HELP)
        sys.exit(1)

    try:
        explanations = explain(command_string)
        format_explanation(explanations)
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted.[/]")
        sys.exit(130)
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)