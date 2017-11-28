#!/usr/bin/env python

import logging
import sys

from mwr.common import logger

from drozer.console import Console

logger.setLevel(logging.DEBUG)
logger.addStreamHandler()

print "sys args:",sys.argv[2::]
Console().run(sys.argv[2::])
