import os
import subprocess
from subprocess import PIPE
from mods import CodeType


def _replace_multiple(main_string, to_be_replaces, new_string):
    for elem in to_be_replaces:
        if elem in main_string:
            main_string = main_string.replace(elem, new_string)

    return main_string


def _permission_change(file_path):
    os.chmod(file_path, 0o755)


def _java_compile(file_path):
    subprocess.Popen(['javac', file_path])
    return os.path.splitext(file_path)[0]


def run_file(code_type, file_path):
    if code_type == CodeType.PYTHON:
        sub_p = subprocess.Popen(['python', file_path], stdout=PIPE)
    elif code_type == CodeType.SHELL:
        _permission_change(file_path)  # FIXME control file owner
        sub_p = subprocess.Popen(file_path, stdout=PIPE)
    elif code_type == CodeType.JAVA:
        _java_compile(file_path)
        dir_path = os.path.dirname(file_path)
        file_path = _java_compile(file_path)
        _permission_change(file_path)  # FIXME control file owner
        execute_path = _replace_multiple(file_path, '/', '.')
        sub_p = subprocess.Popen(['java', '-cp', dir_path, execute_path], stdout=PIPE, shell=True)
    elif code_type == CodeType.JAVASCRIPT:
        _java_compile(file_path)
        sub_p = subprocess.Popen(['node', file_path], stdout=PIPE)
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
