#!/usr/bin/env python3

import sys
import os


PROJECT_TITLE = "PoliRural: Contributions"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rel(*x):
    return os.path.join(BASE_DIR, *x)


# Ensure loggind directory.
LOG_DIR_NAME = 'log'
LOG_DIR = rel(LOG_DIR_NAME)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


# Loggers
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s %(levelname)s] [%(module)s.%(name)s %(funcName)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S %z",
        },
        'semiverbose': {
            'format': "[%(asctime)s %(levelname)s] [%(funcName)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S %z",
        },
        'standard': {
            'format': "[%(asctime)s %(levelname)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S %z",
        },
        'simple': {
            "format" : "[%(asctime)s %(levelname)s] %(message)s",
            'datefmt': "%H:%M:%S %z",
        }
    },
    'filters': {},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': rel('log', 'app.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 1,
            'formatter': 'standard',
        },
        'error': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': rel('log', 'error.log'),
            'maxBytes': 1024*1024*20, # 20 MB
            'backupCount': 1,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
    'loggers': {
        'default': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'error': {
            'handlers': ['error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'console': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
