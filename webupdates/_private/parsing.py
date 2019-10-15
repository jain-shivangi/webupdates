#!/usr/bin/env python
__author__ = 'shivangi'

import logging
import argparse
from webupdates import defaults


__description__ = """
    WebUpdates - It's a tool which polls the webpages & sends the new updates if found any.
"""


LOG_LEVELS = {
    "critical": logging.CRITICAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG
}


def configure_logger(log_path, filename, log_level=logging.DEBUG):

    logFormatter = logging.Formatter("%(asctime)s [%(levelname)8s] - %(message)s")
    logger = logging.getLogger()

    fileHandler = logging.FileHandler("{0}/{1}.log".format(log_path, filename))
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    logger.setLevel(log_level)
    return logger


def get_parser():
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument('--json-input', '-i',
                        dest='json_input',
                        help='',
                        type=str,
                        default=defaults.JSON_INPUT)

    parser.add_argument('--json-output', '-o',
                        dest='json_output',
                        help='',
                        type=str,
                        default=defaults.JSON_OUTPUT)

    parser.add_argument('--watch-dog',
                        action='store_true',
                        dest='watch',
                        help='',
                        default=False)

    parser.add_argument('--off-console',
                        action='store_true',
                        dest='off_console',
                        help='',
                        default=False)

    parser.add_argument('--daemonize',
                        action='store_true',
                        dest='daemonize',
                        help='',
                        default=False)

    parser.add_argument('--after-every', '-e',
                        dest='secs',
                        help='In seconds. Default = {0}secs'.format(defaults.DEFAULT_UPDATE_TIME),
                        type=int,
                        default=defaults.DEFAULT_UPDATE_TIME)

    parser.add_argument('--data-path', '-d',
                        help='Default path: {0}'.format(defaults.WEBUPDATES_HOME),
                        dest='data_path',
                        type=str,
                        default=defaults.WEBUPDATES_HOME)

    parser.add_argument('--log-level',
                        dest='log_level',
                        default='info',
                        type=str,
                        choices=[key.upper() for key in LOG_LEVELS.keys()],
                        help='')

    parser.add_argument('--log-output',
                        dest='logoutput',
                        default='-',
                        type=str,
                        help='')

    return parser