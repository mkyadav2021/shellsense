from shellsense.parser import parse_command, FlagInfo


def test_simple_command():
    result = parse_command("ls")
    assert len(result) == 1
    assert result[0].command == "ls"
    assert result[0].flags == []
    assert result[0].args == []


def test_flags_and_args():
    result = parse_command("ls -la /tmp")
    seg = result[0]
    assert seg.command == "ls"
    assert seg.args == ["/tmp"]
    flag_names = [f.flag for f in seg.flags]
    assert "-l" in flag_names
    assert "-a" in flag_names


def test_pipeline():
    result = parse_command("ps aux | grep nginx | head -5")
    assert len(result) == 3
    assert result[0].command == "ps"
    assert result[1].command == "grep"
    assert result[2].command == "head"


def test_flag_with_value():
    result = parse_command('find . -name "*.log"')
    seg = result[0]
    assert seg.command == "find"
    assert seg.args == ["."]
    name_flag = [f for f in seg.flags if f.flag == "-name"][0]
    assert name_flag.value == "*.log"


def test_subcommand():
    result = parse_command('git commit -m "initial"')
    seg = result[0]
    assert seg.command == "git"
    assert seg.subcommand == "commit"


def test_long_flag_with_equals():
    result = parse_command("ls --color=auto")
    seg = result[0]
    flag = seg.flags[0]
    assert flag.flag == "--color"
    assert flag.value == "auto"
