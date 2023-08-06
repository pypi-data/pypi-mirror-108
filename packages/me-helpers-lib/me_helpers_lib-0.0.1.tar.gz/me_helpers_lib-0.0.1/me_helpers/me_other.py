from me_main_libs import *
from matplotlib import cm
from numpy import linspace
from functools import wraps
import signal
import psutil
import copy


# TODO: move to me_files
def create_logger(name):
    from loguru import logger
    logger.remove()
    logger_ = copy.deepcopy(logger)
    logger_.add(name,
                format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}')
    return logger_


def time_func(func):
    """
    use it as decorator: @time_func at the top of function
    """
    @ wraps(func)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {func.__name__} took {t2 - t1} seconds")
        return result
    return measure_time


def time_func_log(logger_var):
    def time_func(func):
        """
        use it as decorator: @time_func_log at the top of function
        """
        @ wraps(func)
        def measure_time(self, *args, **kwargs):
            t1 = time.time()
            result = func(self, *args, **kwargs)
            t2 = time.time()
            getattr(self, logger_var).debug(
                f"{func.__name__} took {t2 - t1} seconds")
            return result
        return measure_time
    return time_func


def make_colors(number):
    print('\n\n\n use create_colors !!!\n\n\n')


def create_colors(number):
    start = 0.0
    stop = 1.0
    number_of_lines = 9
    cm_subsection = linspace(start, stop, number)

    # here we choose coolwarm, check dir(cm) and
    # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
    # for more
    colors = [cm.coolwarm(x) for x in cm_subsection]
    return colors


def create_requests_session(headers_str):
    headers = {}
    for x in headers_str.split('\n'):
        y = x.split(':', maxsplit=1)
        headers[y[0].strip()] = y[1].strip()

    session = requests.Session()
    session.headers.clear()
    session.headers.update(headers)
    return session


def create_requests_headers(headers_str):
    headers = {}
    for x in headers_str.split('\n'):
        y = x.split(':', maxsplit=1)
        headers[y[0].strip()] = y[1].strip()
    return headers
