import datetime
import logging.config
import os
import yaml


LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
DT_FORMAT = '%Y-%m-%d %H:%M:%S'


def default_logger(name, cfg_path=None,
                   default_level=logging.INFO,
                   default_format=LOG_FORMAT,
                   default_datefmt=DT_FORMAT):
    """
    Get logger configured according to provided YAML config.

    Parameters
    ----------
    name : str
        Specific logger name to distinguish between multiple loggers.
    cfg_path : str
        Pass absolute config path explicitly or set LOG_CFG 
        environment variable. Function provides logger with default
        configuration if neither cfg_path, nor LOG_CFG were set.
    default_level : int
        Level for default configuration. One of logging.{INFO, DEBUG}
    default_format : str
        Message format for default configuration.
    default_datefmt : str
        Datetime format for default configureation.
    env_key : str
        YAML config path environment variable name.

    Returns
    -------
    logging.Logger
    """
    if not cfg_path:
        cfg_path = os.getenv('LOG_CFG', None)
    if not cfg_path:
        logging.basicConfig(level=default_level, datefmt=default_fmt)
    else:
        with open(cfg_path, 'rt') as f:
            cfg = yaml.safe_load(f.read())
        logging.config.dictConfig(cfg)
    return logging.getLogger(name)


def curr_datetime(fmt=DT_FORMAT):
    """
    Formatted current datetime.

    Parameters
    ----------
    fmt : str
        Datetime format. E.g. '%m-%d %H-%M'

    Returns
    -------
    str
        Datetime formatted according to fmt.
    """
    return datetime.datetime.now().strftime(DT_FORMAT)
