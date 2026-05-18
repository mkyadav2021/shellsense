import urllib.request
import urllib.error
import json


TLDR_API = "https://raw.githubusercontent.com/tldr-pages/tldr/main/pages"
PLATFORMS = ["common", "linux", "macos", "osx"]


def fetch_tldr(command: str) -> str | None:
  
    for platform in PLATFORMS:
        url = f"{TLDR_API}/{platform}/{command}.md"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "shellsense/0.1"})
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.read().decode("utf-8")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            continue

    return None


def parse_tldr(markdown: str) -> dict:
  
    lines = markdown.strip().split("\n")
    description_lines = []
    examples = []

    current_desc = None

    for line in lines:
        line = line.strip()

        if line.startswith("# "):
            continue  # Skip title

        if line.startswith("> "):
            description_lines.append(line[2:])

        elif line.startswith("- "):
            current_desc = line[2:].rstrip(":")

        elif line.startswith("`") and line.endswith("`") and current_desc:
            examples.append({
                "description": current_desc,
                "command": line[1:-1],
            })
            current_desc = None

    return {
        "description": " ".join(description_lines),
        "examples": examples,
    }


def get_tldr(command: str) -> dict | None:

    markdown = fetch_tldr(command)
    if markdown is None:
        return None

    return parse_tldr(markdown)