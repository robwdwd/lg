# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Filter Gen and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Convert .env settings into starlette config."""

import yaml
from starlette.config import Config
from starlette.datastructures import Secret

try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import Loader


def load_config(config_file: str):
    """Loads the looking glass configuration.

    Args:
        config_file (str): filename to loads

    Returns:
        dict: Configuration dictionary
    """
    with open(config_file, "r") as conf:
        cfg = yaml.load(conf, Loader)
        return cfg


config = Config(".env")

PORT = config("PORT", default="8011", cast=int)
LISTEN = config("LISTEN", default="127.0.0.1")
ROOT_PATH = config("ROOT_PATH", default="")

USERNAME = config("USERNAME")
PASSWORD = config("PASSWORD")

DEBUG = config("DEBUG", cast=bool, default=False)
LOG_LEVEL = config("LOG_LEVEL", default="info")

SECRET_KEY = config("SECRET_KEY", cast=Secret)
CSRF_SECRET = config("CSRF_SECRET", cast=Secret)
SESSION_NAME = config("SESSION_NAME", default="lg_session")

CONFIG_FILE = config("CONFIG_FILE", default="config.yml", cast=load_config)

PING_MULTI_MAX_SOURCE = config("PING_MULTI_MAX_SOURCE", cast=int, default=3)
PING_MULTI_MAX_IP = config("PING_MULTI_MAX_IP", cast=int, default=10)
