COMMANDS: dict[str, dict] = {
    "ls": {
        "description": "List directory contents",
        "flags": {
            "-l": "Use long listing format (permissions, owner, size, date)",
            "-a": "Show hidden files (those starting with .)",
            "-h": "Print sizes in human-readable format (1K, 234M, 5G)",
            "-R": "List subdirectories recursively",
            "-t": "Sort by modification time, newest first",
            "-r": "Reverse the sort order",
            "-S": "Sort by file size, largest first",
            "-d": "List directories themselves, not their contents",
            "--color": "Colorize the output (auto, always, never)",
            "-1": "List one file per line",
            "-i": "Print the inode number of each file",
        },
    },
    "cd": {
        "description": "Change the current working directory",
        "flags": {
            "-": "Switch to the previous directory",
            "~": "Go to your home directory",
            "..": "Go up one directory level",
        },
    },
    "grep": {
        "description": "Search for text patterns in files or input",
        "flags": {
            "-i": "Ignore case distinctions in patterns",
            "-r": "Search recursively through directories",
            "-n": "Print line numbers with output",
            "-v": "Invert match — show lines that DON'T match",
            "-c": "Print only a count of matching lines",
            "-l": "Print only names of files with matches",
            "-w": "Match whole words only",
            "-e": "Specify the pattern (useful for patterns starting with -)",
            "-E": "Use extended regular expressions (same as egrep)",
            "-P": "Use Perl-compatible regular expressions",
            "--include": "Search only files matching this pattern",
            "--exclude": "Skip files matching this pattern",
            "-A": "Print N lines after each match",
            "-B": "Print N lines before each match",
            "-C": "Print N lines before and after each match (context)",
        },
    },
    "find": {
        "description": "Search for files and directories in a directory tree",
        "flags": {
            "-name": "Find files matching a name pattern (case-sensitive)",
            "-iname": "Find files matching a name pattern (case-insensitive)",
            "-type": "Filter by type: f=file, d=directory, l=symlink",
            "-size": "Filter by size (+10M = over 10MB, -1k = under 1KB)",
            "-mtime": "Filter by modification time in days (+7 = over 7 days ago)",
            "-atime": "Filter by access time in days",
            "-ctime": "Filter by change time in days",
            "-user": "Filter by file owner",
            "-group": "Filter by file group",
            "-perm": "Filter by permissions (e.g. 755, /u+w)",
            "-delete": "Delete found files (use with caution!)",
            "-exec": "Execute a command on each found file",
            "-maxdepth": "Limit how deep to search in subdirectories",
            "-mindepth": "Skip the first N levels of directories",
            "-empty": "Find empty files or directories",
            "-newer": "Find files newer than a reference file",
        },
    },
    "chmod": {
        "description": "Change file permissions",
        "flags": {
            "-R": "Change permissions recursively for directories",
            "-v": "Print a message for each file processed",
            "-c": "Like -v but only report changes",
            "--reference": "Use another file's permissions as a template",
        },
    },
    "cat": {
        "description": "Print file contents to the terminal",
        "flags": {
            "-n": "Number all output lines",
            "-b": "Number non-empty output lines only",
            "-s": "Squeeze multiple blank lines into one",
            "-E": "Show $ at the end of each line",
            "-T": "Show tab characters as ^I",
        },
    },
    "cp": {
        "description": "Copy files and directories",
        "flags": {
            "-r": "Copy directories recursively",
            "-i": "Prompt before overwriting",
            "-f": "Force overwrite without prompting",
            "-v": "Print each file as it's copied",
            "-p": "Preserve file attributes (timestamps, permissions)",
            "-a": "Archive mode — preserves everything (-r + -p + links)",
            "--backup": "Make a backup of each existing destination file",
        },
    },
    "mv": {
        "description": "Move or rename files and directories",
        "flags": {
            "-i": "Prompt before overwriting",
            "-f": "Force overwrite without prompting",
            "-v": "Print each file as it's moved",
            "-n": "Do not overwrite existing files",
            "--backup": "Make a backup of each existing destination file",
        },
    },
    "rm": {
        "description": "Remove files or directories",
        "flags": {
            "-r": "Remove directories and their contents recursively",
            "-f": "Force removal without prompting",
            "-i": "Prompt before every removal",
            "-v": "Print each file as it's removed",
            "-d": "Remove empty directories",
        },
    },
    "mkdir": {
        "description": "Create new directories",
        "flags": {
            "-p": "Create parent directories as needed (no error if existing)",
            "-v": "Print a message for each directory created",
            "-m": "Set permissions for the new directory",
        },
    },
    "tar": {
        "description": "Archive and compress files",
        "flags": {
            "-c": "Create a new archive",
            "-x": "Extract files from an archive",
            "-t": "List the contents of an archive",
            "-z": "Compress or decompress using gzip",
            "-j": "Compress or decompress using bzip2",
            "-J": "Compress or decompress using xz",
            "-v": "Verbose — list files being processed",
            "-f": "Specify the archive filename (must come last before filename)",
            "-C": "Change to directory before extracting",
            "--exclude": "Exclude files matching a pattern",
        },
    },
    "curl": {
        "description": "Transfer data from or to a server using URLs",
        "flags": {
            "-o": "Write output to a file instead of stdout",
            "-O": "Save file with the same name as the remote file",
            "-L": "Follow redirects",
            "-s": "Silent mode — no progress bar or errors",
            "-v": "Verbose — show request and response headers",
            "-X": "Specify the HTTP method (GET, POST, PUT, DELETE)",
            "-H": "Add a custom header",
            "-d": "Send data in the request body (implies POST)",
            "-F": "Submit form data (multipart)",
            "-u": "Provide username:password for authentication",
            "-k": "Allow insecure SSL connections",
            "-I": "Fetch headers only (HEAD request)",
            "--cookie": "Send cookies from a string or file",
            "--max-time": "Maximum time in seconds for the request",
        },
    },
    "ps": {
        "description": "Show information about running processes",
        "flags": {
            "a": "Show processes from all users",
            "u": "Show detailed user-oriented format",
            "x": "Include processes not attached to a terminal",
            "-e": "Show every process on the system",
            "-f": "Full format listing",
            "-p": "Show only the specified process ID",
            "--sort": "Sort output by a field (e.g. --sort=-%mem)",
        },
    },
    "kill": {
        "description": "Send a signal to a process (default: SIGTERM to stop it)",
        "flags": {
            "-9": "Send SIGKILL — force kill immediately (cannot be caught)",
            "-15": "Send SIGTERM — ask the process to terminate gracefully",
            "-l": "List all available signal names",
            "-s": "Specify the signal to send by name",
        },
    },
    "head": {
        "description": "Show the first lines of a file or input",
        "flags": {
            "-n": "Number of lines to show (default: 10)",
            "-c": "Number of bytes to show",
        },
    },
    "tail": {
        "description": "Show the last lines of a file or input",
        "flags": {
            "-n": "Number of lines to show (default: 10)",
            "-f": "Follow — keep watching for new lines (great for logs)",
            "-c": "Number of bytes to show",
        },
    },
    "awk": {
        "description": "Pattern scanning and text processing language",
        "flags": {
            "-F": "Set the field separator (e.g. -F: to split on colons)",
            "-v": "Set a variable before execution",
            "-f": "Read the AWK program from a file",
        },
    },
    "sed": {
        "description": "Stream editor for filtering and transforming text",
        "flags": {
            "-i": "Edit files in place (modify the original file)",
            "-e": "Add a script/command to execute",
            "-n": "Suppress automatic printing — only print when told to",
            "-r": "Use extended regular expressions",
            "-E": "Use extended regular expressions (same as -r)",
        },
    },
    "xargs": {
        "description": "Build and execute commands from standard input",
        "flags": {
            "-I": "Replace a placeholder with each input line (e.g. -I{} mv {} /tmp/)",
            "-n": "Use at most N arguments per command",
            "-P": "Run up to N processes in parallel",
            "-0": "Input items are separated by null bytes (use with find -print0)",
            "-t": "Print each command before executing it",
            "-p": "Prompt before executing each command",
        },
    },
    "ssh": {
        "description": "Connect to a remote machine securely over the network",
        "flags": {
            "-p": "Specify the port to connect to",
            "-i": "Use a specific private key file for authentication",
            "-v": "Verbose mode — useful for debugging connection issues",
            "-L": "Set up local port forwarding (tunnel)",
            "-R": "Set up remote port forwarding",
            "-N": "Don't execute a remote command (useful with port forwarding)",
            "-f": "Go to background before executing the command",
            "-o": "Set an SSH option (e.g. -o StrictHostKeyChecking=no)",
        },
    },
    "chown": {
        "description": "Change file owner and group",
        "flags": {
            "-R": "Apply changes recursively to directories",
            "-v": "Print a message for each file processed",
            "--reference": "Use another file's ownership as a template",
        },
    },
    "wc": {
        "description": "Count lines, words, and bytes in files or input",
        "flags": {
            "-l": "Count lines only",
            "-w": "Count words only",
            "-c": "Count bytes only",
            "-m": "Count characters only",
        },
    },
    "sort": {
        "description": "Sort lines of text",
        "flags": {
            "-r": "Reverse the sort order",
            "-n": "Sort numerically instead of alphabetically",
            "-k": "Sort by a specific field/column",
            "-u": "Remove duplicate lines",
            "-t": "Set the field delimiter",
            "-h": "Sort human-readable numbers (2K, 1G)",
        },
    },
    "uniq": {
        "description": "Filter out repeated adjacent lines",
        "flags": {
            "-c": "Prefix lines with a count of how many times they appeared",
            "-d": "Only print duplicate lines",
            "-u": "Only print unique lines",
            "-i": "Ignore case when comparing",
        },
    },
    "docker": {
        "description": "Manage containers and images",
        "subcommands": {
            "run": "Create and start a new container",
            "build": "Build an image from a Dockerfile",
            "ps": "List running containers",
            "images": "List downloaded images",
            "pull": "Download an image from a registry",
            "push": "Upload an image to a registry",
            "exec": "Run a command inside a running container",
            "stop": "Stop a running container",
            "rm": "Remove a stopped container",
            "rmi": "Remove an image",
            "logs": "View container output logs",
            "compose": "Manage multi-container applications",
        },
    },
    "git": {
        "description": "Distributed version control system",
        "subcommands": {
            "init": "Create a new Git repository",
            "clone": "Download a repository from a remote URL",
            "add": "Stage files for the next commit",
            "commit": "Save staged changes to the repository history",
            "push": "Upload local commits to a remote repository",
            "pull": "Download and merge remote changes",
            "status": "Show the current state of the working directory",
            "log": "Show the commit history",
            "branch": "List, create, or delete branches",
            "checkout": "Switch branches or restore files",
            "merge": "Combine two branches together",
            "diff": "Show changes between commits, branches, or files",
            "stash": "Temporarily save uncommitted changes",
            "reset": "Undo commits or unstage files",
            "rebase": "Reapply commits on top of another branch",
        },
    },
}


def lookup(command: str, subcommand: str | None = None) -> dict | None:
  
    entry = COMMANDS.get(command)
    if entry is None:
        return None

    result = {"description": entry["description"]}

    # If there's a subcommand, check if we know about it
    if subcommand and "subcommands" in entry:
        sub_desc = entry["subcommands"].get(subcommand)
        if sub_desc:
            result["subcommand_description"] = sub_desc

    if "flags" in entry:
        result["flags"] = entry["flags"]

    return result

#we will keep expanding this file