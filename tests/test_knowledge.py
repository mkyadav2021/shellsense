from shellsense import knowledge


def test_known_command():
    result = knowledge.lookup("ls")
    assert result is not None
    assert "description" in result
    assert "flags" in result
    assert "-l" in result["flags"]


def test_unknown_command():
    result = knowledge.lookup("totallynotarealcommand")
    assert result is None


def test_subcommand():
    result = knowledge.lookup("git", "commit")
    assert result is not None
    assert "subcommand_description" in result