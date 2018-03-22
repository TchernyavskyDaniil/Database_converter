import logging
import sys

def get_formatter():
    formatter = logging.Formatter('%(asctime)s:%(msecs)d-%(name)s-%(levelname)s: %(message)s')
    formatter.default_msec_format = '%s.%03d'
    formatter.datefmt = "%d.%m.%Y %H:%M:%S"
    return formatter


def create_file_handler(path,formatter):
    fh = logging.FileHandler(path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    return fh

def create_console_handler(formatter):
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    return ch

def init_logging(logger_path, logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = get_formatter()
    fh = create_file_handler(logger_path,formatter)
    logger.addHandler(fh)
    ch = create_console_handler(formatter)
    logger.addHandler(ch)
