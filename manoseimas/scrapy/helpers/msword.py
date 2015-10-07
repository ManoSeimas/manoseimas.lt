import subprocess


def doc2xml(file_content):
    """Convert an MS Word .doc file to DocBook XML.

    Requires antiword to be installed.
    """
    cmd = ['antiword', '-x', 'db', '-']
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(file_content)
    if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, cmd, stderr)
    return stdout
