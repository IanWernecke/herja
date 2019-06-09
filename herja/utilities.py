import subprocess


def execute(args, cwd=None):
    """Execute a command with subprocess to obtain the stdout, stderr, and return code."""
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd
    )
    stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode
