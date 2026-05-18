# ShellSense

Ever typed a command you copied from the internet and had no idea what half of it does? ShellSense explains it in plain English — flag by flag, piece by piece.

```
$ shellsense 'tar -czf backup.tar.gz /home/user/documents'
```

```
  tar -- Archive and compress files

  Arguments:
    /home/user/documents

  Flag              Explanation
  -c                Create a new archive
  -z                Compress or decompress using gzip
  -f backup.tar.gz  Specify the archive filename (must come last before filename)

  Source: built-in database
```

It handles pipes too:

```
$ shellsense 'ps aux | grep nginx | head -5'
```

Each command in the pipeline gets its own breakdown.

---

## What it does

- Breaks down any Linux shell command into its parts
- Explains what each flag does in plain English
- Handles pipes, subcommands (`git commit`, `docker run`), grouped flags (`-la`), and flags with values (`-name "*.log"`)
- Looks up explanations from a built-in database, man pages, and tldr pages — in that order
- Caches results so repeated lookups are instant

---

## Installation

You need Python 3.10 or higher.

```bash
git clone https://github.com/mkyadav2021/shellsense.git
cd shellsense
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

That's it. The `shellsense` command is now available in your terminal whenever the virtual environment is active.

---

## Usage

```bash
# Explain a command
shellsense 'ls -la /tmp'
shellsense 'tar -czf archive.tar.gz /home'
shellsense 'git commit -m "initial"'
shellsense 'ps aux | grep nginx | head -5'
shellsense 'grep -rn "error" /var/log 2>&1'

# Utility commands
shellsense status       # show what's cached and where
shellsense clear-cache  # wipe all cached results
```

To activate the virtual environment in a new terminal session:

```bash
source .venv/bin/activate
```

### Quoting tip

Always wrap the command in **single quotes**. Single quotes pass everything inside to ShellSense exactly as written — double quotes, `>`, `*`, and `$` are all preserved:

```bash
shellsense 'find . -name "*.log" -mtime +7'   # correct — * and " are safe
shellsense "find . -name '*.log' -mtime +7"   # also fine — no special chars
shellsense "echo "hello" > file.txt"           # broken — shell eats the inner "
```

The only time you can't use single quotes is if the command itself contains a single quote (rare).

---

## How it works

When you pass a command, ShellSense:

1. **Parses** the command string into structured pieces (base command, subcommand, flags, arguments)
2. **Looks up** explanations in this priority order:
   - Built-in knowledge base (instant, covers the most common commands)
   - Local cache (instant, from previous lookups)
   - System man pages (comprehensive, slightly slower)
   - tldr pages (fetched from GitHub, includes examples)
   - `--help` output (last resort)
3. **Prints** a colour-coded breakdown using Rich

---

## Project structure

```
shellsense/
    shellsense/
        cli.py          # Entry point, reads sys.argv
        parser.py       # Breaks command strings into structured pieces
        knowledge.py    # Built-in database of common commands and flags
        manpage.py      # Reads and parses system man pages
        tldr.py         # Fetches tldr pages from GitHub
        explainer.py    # Orchestrates all sources, merges results
        formatter.py    # Coloured terminal output via Rich
        cache.py        # Saves results to ~/.cache/shellsense/
    tests/
        test_parser.py
        test_knowledge.py
        test_explainer.py
```

---

## Running the tests

```bash
pytest tests/ -v
```

---

## Known limitations

- `ps aux` uses BSD-style flags without a dash — ShellSense sees `aux` as a positional argument rather than flags, so those won't be explained individually. Use `ps -ef` for POSIX-style output.
- The built-in knowledge base covers the most common commands. If a command isn't there, it falls back to man pages and tldr, which may be slower or less precise.
- tldr pages require an internet connection.

---

## Requirements

- Python 3.10+
- Linux or macOS (for man page access)
- [`rich`](https://github.com/Textualize/rich) — installed automatically
