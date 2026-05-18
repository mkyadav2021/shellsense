from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box

from shellsense.explainer import CommandExplanation

console = Console()


def format_explanation(explanations: list[CommandExplanation]) -> None:
  
    total = len(explanations)

    for i, exp in enumerate(explanations):
        # Header: command name and description
        if total > 1:
            title = f"Part {i + 1} of {total}"
            if i > 0:
                title += " (piped from previous)"
        else:
            title = None

        # Build the command name display
        cmd_name = exp.command
        if exp.subcommand:
            cmd_name += f" {exp.subcommand}"

        header = Text()
        header.append(cmd_name, style="bold cyan")
        header.append(f"  —  {exp.description}", style="dim")

        console.print()
        console.print(Panel(header, title=title, border_style="blue", box=box.ROUNDED))

        # Positional arguments
        if exp.args:
            console.print("  [bold yellow]Arguments:[/]")
            for arg in exp.args:
                console.print(f"    [green]{arg}[/]")
            console.print()

        # Flags
        if exp.flags:
            table = Table(
                show_header=True,
                header_style="bold magenta",
                box=box.SIMPLE,
                padding=(0, 2),
            )
            table.add_column("Flag", style="bold green", min_width=16)
            table.add_column("Explanation", style="white")

            for flag in exp.flags:
                flag_display = flag.flag
                if flag.value:
                    flag_display += f" {flag.value}"

                table.add_row(flag_display, flag.explanation)

            console.print(table)

        # Examples from tldr (if available)
        if exp.examples:
            console.print("  [bold yellow]Examples:[/]")
            # Show up to 3 examples to keep output concise
            for example in exp.examples[:3]:
                console.print(f"    [dim]{example['description']}[/]")
                console.print(f"    [green]$ {example['command']}[/]")
                console.print()

        # Source attribution
        source_labels = {
            "builtin": "built-in database",
            "man": "man page",
            "tldr": "tldr pages",
            "help": "--help output",
            "cache": "cache",
        }
        source_label = source_labels.get(exp.source, exp.source)
        console.print(f"  [dim italic]Source: {source_label}[/]")

    console.print()