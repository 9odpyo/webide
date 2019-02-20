import os
import uuid
import time


def _get_data_directory():
    cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_dir = 'data'
    return os.path.join(cur_path, data_dir)


def _gen_file_name(code_type):
    # FIXME java filename
    now_time = time.localtime()
    random_name = str(uuid.uuid4()).split('-')[4]
    temp_file_name = '{}-{}-{}_{}.{}'.format(
        now_time.tm_year, now_time.tm_mon, now_time.tm_mday, random_name, code_type.value)
    return temp_file_name


def write_file(code_type, code_text):
    dir_path = _get_data_directory()
    file_name = _gen_file_name(code_type)
    full_path = os.path.join(dir_path, file_name)
    f = open(full_path, 'w')
    f.write(code_text)
    f.close()
    return full_path
