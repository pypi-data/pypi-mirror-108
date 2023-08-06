# flake8: noqa
import subprocess  # noqa: I005 S404


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_a28_system_no_param():
    command = ['a28', 'system']
    out, err, exitcode = capture(command)
    assert exitcode == 2
    assert out == b''
    message = b'usage: a28 system [-h] {exists,clean} ...'
    assert err[0:len(message)] == message


def test_a28_exists_no_param():
    command = ['a28', 'system', 'exists']
    out, err, exitcode = capture(command)
    assert exitcode == 0
    message = b'No configuration exists at '
    assert out[0:len(message)] == message


def test_a28_clean_no_param():
    command = ['a28', 'system', 'clean']
    out, err, exitcode = capture(command)
    assert exitcode == 0
    message = b'No configuration to clean.'
    assert out[0:len(message)] == b'No configuration to clean.'
