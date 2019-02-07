import subprocess
from subprocess import PIPE
from mods import CodeType


def _java_compile(file_path):
    subprocess.Popen(['javac', file_path], shell=True)


def run_file(code_type, file_path):
    if code_type == CodeType.PYTHON:
        sub_p = subprocess.Popen(['python', file_path], stdout=PIPE)
    elif code_type == CodeType.SHELL:
        sub_p = subprocess.Popen([file_path], stdout=PIPE)
    elif code_type == CodeType.JAVA:
        _java_compile(file_path)
        sub_p = subprocess.Popen(['java', file_path], stdout=PIPE)  # FIXME control file owner
    elif code_type == CodeType.JAVASCRIPT:
        _java_compile(file_path)
        sub_p = subprocess.Popen(['node', file_path], stdout=PIPE)  # FIXME control file owner
    else:
        return 'error'  # TODO error exception raise

    while True:
        line = sub_p.stdout.readline().decode('utf8')
        if line == '':
            if sub_p.poll() is not None:
                break
            else:
                continue
        yield line
    sub_p.stdout.close()
    return_code = sub_p.wait()
    print(return_code)
