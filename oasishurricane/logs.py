#!/usr/bin/env python
# coding=utf-8

import os

BASE_DIR = os.path.curdir
LOGS_DIR = BASE_DIR

DEV_LOGFILE = "gethurricaneloss_dev.log"
PROD_LOGFILE = "gethurricaneloss.log"

DEVELOPMENT_LOGFILE = os.path.join(LOGS_DIR, DEV_LOGFILE)
PRODUCTION_LOGFILE = os.path.join(LOGS_DIR, PROD_LOGFILE)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)6s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)6s [%(name)s.%(funcName)s:%(lineno)d]\t%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'development_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DEVELOPMENT_LOGFILE,
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose'
        },
        'production_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PRODUCTION_LOGFILE,
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'simple'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'loggers': {
        'model': {
            'handlers': ['development_logfile', 'production_logfile'],
        },
        'py.warnings': {
            'handlers': ['development_logfile'],
        },
    }
}
