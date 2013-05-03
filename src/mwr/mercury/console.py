#!/usr/bin/python

import logging
import sys

from mwr.common import logger
from mwr.droidhg.console import Console

logger.setLevel(logging.DEBUG)
logger.addStreamHandler()

Console().run(sys.argv[2::])
