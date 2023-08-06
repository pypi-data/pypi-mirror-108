import os
import logging
from importlib_metadata import version, PackageNotFoundError
from biolib.app import BioLib

# try fetching version, if it fails (usually when in dev), add default
try:
    BIOLIB_PACKAGE_VERSION = version('pybiolib')
except PackageNotFoundError:
    BIOLIB_PACKAGE_VERSION = '0.0.0'

IS_DEV = os.getenv('BIOLIB_DEV', '').upper() == 'TRUE'

logger = logging.getLogger('biolib')


def configure_logging(default_log_level):
    # set log level
    env_log_level = os.getenv('BIOLIB_LOG')
    if env_log_level is None:
        BioLib.set_logging(default_log_level)
    else:
        log_level_map = {
            'DEBUG': logging.DEBUG,
            'ERROR': logging.ERROR,
            'INFO': logging.INFO,
            'TRACE': BioLib.TRACE_LOGGING,
            'WARNING': logging.WARNING,
            'WARN': logging.WARNING,
        }
        # get log level from map and use default if no match
        log_level = log_level_map.get(env_log_level.upper(), logging.ERROR)
        BioLib.set_logging(log_level)
