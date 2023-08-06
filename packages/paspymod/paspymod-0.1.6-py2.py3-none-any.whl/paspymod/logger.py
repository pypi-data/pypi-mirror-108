import logging
from .utility import f_check as f

try:
    level = logging.getLevelName(f().loaded['debug_level'])
except:
    logging.basicConfig(level = logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S', \
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s')
else:
    logging.basicConfig(level = level, datefmt='%Y-%m-%d %H:%M:%S', \
        format='%(asctime)s %(name)s %(levelname)-8s %(message)s')
