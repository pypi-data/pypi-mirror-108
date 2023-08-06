import os

import pytest

from pyshellrunner import ShellRunner


TEST_OUTPUT_SCRIPT = """
set -e

echo_stdout () {
    for i in $(seq 10000); do
        echo "stdout ${i}"
    done
}

echo_stderr () {
    for i in $(seq 10000); do
        >&2 echo "stderr ${i}"
    done
}

echo_mixed () {
    COUNT=$1
    for i in $(seq $COUNT); do
        >&2 echo "stderr ${i}"
        echo "stdout ${i}"
    done
}

$@
"""


@pytest.fixture(scope="module")
def output_script():
    script_path = "/tmp/test-pyshellrunner-output.sh"

    with open(script_path, "+w") as script:
        script.write(TEST_OUTPUT_SCRIPT)
        os.chmod(script_path, 0o777)

    return script_path


def test_stdout(output_script):
    ShellRunner(verbosity=3).run(f"{output_script} echo_stdout 10000")


def test_stderr(output_script):
    ShellRunner(verbosity=3).run(f"{output_script} echo_stderr 10000")


def test_mixed(output_script):
    ShellRunner(verbosity=3).run(f"{output_script} echo_mixed 10000")
