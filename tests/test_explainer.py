from shellsense.explainer import explain


def test_known_command():
    results = explain("ls -la")
    assert len(results) == 1
    assert results[0].command == "ls"
    assert results[0].description != ""
    flag_names = [f.flag for f in results[0].flags]
    assert "-l" in flag_names
    assert "-a" in flag_names


def test_pipeline_explanation():
    results = explain("ps aux | grep nginx")
    assert len(results) == 2
    assert results[0].command == "ps"
    assert results[1].command == "grep"
    assert results[1].args == ["nginx"]


def test_unknown_command():
    # Should not crash, just give minimal info
    results = explain("somefakecommand --flag")
    assert len(results) == 1
    assert results[0].command == "somefakecommand"


def test_subcommand():
    results = explain("git commit -m 'initial'")
    assert results[0].command == "git"
    assert results[0].subcommand == "commit"