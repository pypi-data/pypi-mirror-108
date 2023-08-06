from me_main_libs import *
import copy
import psutil


def create_logger(name):
    from loguru import logger
    logger.remove()
    logger_ = copy.deepcopy(logger)
    logger_.add(name,
                format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}', colorize=False)
    return logger_


def create_logger_2(folder, name):
    from loguru import logger
    logger.remove()
    logger_ = copy.deepcopy(logger)
    path = os.path.join(folder, f'{name}.log')
    logger_.add(path,
                format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}', colorize=False)
    return logger_


def create_parquet(df, folder, name):
    path = os.path.join(folder, f'{name}.parquet')
    df.to_parquet(path)
    return path


def create_html_from_df(df, folder, name, index=False, header=False, render_links=True):
    path = os.path.join(folder, f'{name}.html')
    df.to_html(path, index=index, header=header,
               render_links=render_links)
    return path


def create_png_from_plt(fig, folder, name):
    path = os.path.join(folder, f'{name}.png')
    fig.savefig(path)
    return path


def create_txt(data, folder, name):
    _file = os.path.join(folder, f'{name}.txt')
    with open(_file, 'w') as f:
        for line in data:
            f.write(str(line))
    return _file


def create_json(data, folder, name):
    _file = os.path.join(folder, f'{name}.json')
    with open(_file, "w") as f:
        json.dump(data, f)
    return _file


def read_parquet(folder, name):
    _file = os.path.join(folder, f'{name}.parquet')
    data = pd.read_parquet(_file)
    return data


def read_txt(folder, name, readlines=False):
    _file = os.path.join(folder, f'{name}.txt')
    with open(_file, 'r') as f:
        if readlines:
            x = f.readlines()
        else:
            x = f.read()
    return x


def read_log(folder, name, readlines=False):
    _file = os.path.join(folder, f'{name}.log')
    with open(_file, 'r') as f:
        if readlines:
            x = f.readlines()
        else:
            x = f.read()
    return x


def read_json(folder, name):
    _file = os.path.join(folder, f'{name}.json')
    with open(_file) as f:
        data = json.load(f)
    return data


def update_txt(data, folder, name):
    _file = os.path.join(folder, f'{name}.txt')
    with open(_file, 'a') as f:
        for line in data:
            f.write(str(line))
    return _file


def erase_txt(folder, name):
    _file = os.path.join(folder, f'{name}.txt')
    open(_file, "w").close()


def erase_log(folder, name):
    _file = os.path.join(folder, f'{name}.log')
    open(_file, "w").close()


def erase_json(folder, name):
    _file = os.path.join(folder, f'{name}.json')
    open(_file, "w").close()


def delete_files(files):
    for x in files:
        os.remove(x)


def delete_folder(folder):
    pass


def convert_py_to_ipynb(file):
    out_file = f'{file[:-3]}.ipynb'
    command = f'ipynb-py-convert {file} {out_file}'

    p = psutil.Popen(command, shell=True)
    while p.is_running():
        time.sleep(1)
    return out_file


def convert_ipynb_to_html(file):
    out_file = f'{file[:-6]}.html'
    command = f'jupyter nbconvert --to html {file}'

    p = psutil.Popen(command, shell=True)
    while p.is_running():
        time.sleep(1)
    return out_file


def convert_py_to_html(file):
    ipynb = convert_py_to_ipynb(file)
    html = convert_ipynb_to_html(ipynb)
    return html
