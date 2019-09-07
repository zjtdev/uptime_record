#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging, logging.handlers, os, sys, datetime, re
import subprocess
try:
    HASH_GIT = subprocess.check_output(["git", "describe", '--always']).strip()
    HASH_GIT = str(HASH_GIT, encoding='utf-8')
except:
    HASH_GIT = ''
PATH_FILE = os.path.dirname(os.path.abspath(__file__))
LOG_FOLDER = os.path.join(PATH_FILE, 'log')
DATE_FORMAT = '%Y-%m-%d'

class LoggingFilter(logging.Filter):
    def __init__(self, hash_git):
        super().__init__()
        self.hash_git = hash_git
    def filter(self, record):
        record.hash_git = self.hash_git
        return True

def get_logger(name = None):
    # 清除7天前的log文件
    clear_logger_files(7)
    out_to_console = False
    logger = logging.getLogger(name)
    logger.addFilter(LoggingFilter(HASH_GIT))
    if (len(logger.handlers) <= 0):
        if out_to_console:
            handler = generate_handler_console(name)
        else:
            handler = generate_handler_file(name)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(hash_git)s %(filename)s:%(lineno)d - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    return logger

def generate_handler_file(name):
    if (not os.path.exists(LOG_FOLDER)):
        os.makedirs(LOG_FOLDER)
    date_str = datetime.datetime.now().date().strftime(DATE_FORMAT)
    logger_filename = '{}/{}.{}.log'.format(LOG_FOLDER, name, date_str)
    handler = logging.FileHandler(logger_filename)
    return handler

def clear_logger_files(days):
    if os.path.exists(LOG_FOLDER):
        date_to_clear = datetime.datetime.now().date() - datetime.timedelta(days = days)
        for log_filename in os.listdir(LOG_FOLDER):
            match = re.search(r'\.([0-9]+-[0-9]+-[0-9]+)\.', log_filename)
            if match:
                date_str = match.group(1)
                log_date = datetime.datetime.strptime(date_str, DATE_FORMAT).date()
                if log_date < date_to_clear:
                    log_file = os.path.join(LOG_FOLDER, log_filename)
                    os.remove(log_file)

def generate_handler_console(name):
    handler = logging.StreamHandler(sys.stdout)
    return handler