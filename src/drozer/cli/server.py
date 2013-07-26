#!/usr/bin/python

import logging
import sys

from mwr.common import logger

from drozer.server import Server

logger.setLevel(logging.INFO)
logger.addStreamHandler()

Server().run(sys.argv[2::])
