import subprocess
from subprocess import PIPE


def run_file(file_path):
    sub_p = subprocess.Popen(['python', file_path], stdout=PIPE)
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
