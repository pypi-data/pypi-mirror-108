from pyshellrunner import run, ShellRunner
import pytest

def test_run_echo():
    res = run("echo -n 'test'")

    assert res.output == 'test'
    assert res.exit_code == 0

def test_run_bad_command():
    with pytest.raises(ShellRunner.CommandFailed):
        res = run("ls /akjshkjhdksa")
