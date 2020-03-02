"""
Copyright 2020 Gould Southern
Author: Ryan Ledford [ https://github.com/rledford ]
"""

import os
from sys import stdout
import logging
from logging.handlers import RotatingFileHandler
import __main__

_log_dir = os.path.join(os.path.dirname(
    os.path.realpath(__main__.__file__)), 'logs')
_log_file = os.path.join(_log_dir, 'application.log')

if not os.path.isdir(_log_dir):
    os.mkdir(_log_dir)

#logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger('Application Log')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

fh = RotatingFileHandler(
    _log_file, maxBytes=5 * 1e6, backupCount=5)
fh.setFormatter(formatter)
sh = logging.StreamHandler(stdout)
sh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(sh)

logger.info(
    '****************************** Log Start ******************************')