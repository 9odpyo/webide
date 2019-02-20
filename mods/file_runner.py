import subprocess
from subprocess import PIPE


def run_file(file_path):
    cmd = ""

    if file_path.find(".py") != -1:
        cmd = "python"
    elif file_path.find(".js") != -1:
        cmd = "node"

    sub_p = subprocess.Popen([cmd, file_path], stdout=PIPE)
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
