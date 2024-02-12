#!/usr/bin/env python

import logging
import sys

from WithSecure.common import logger

from drozer.console import Console

logger.setLevel(logging.DEBUG)
logger.addStreamHandler()

Console().run(sys.argv[2::])
