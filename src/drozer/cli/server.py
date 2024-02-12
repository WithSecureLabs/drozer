#!/usr/bin/env python

import logging
import sys

from WithSecure.common import logger

from drozer.server import Server

logger.setLevel(logging.INFO)
logger.addStreamHandler()

Server().run(sys.argv[2::])
