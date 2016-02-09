#!/usr/bin/env python

import logging
import sys

from mwr.common import logger

from drozer.ssl import SSLManager

logger.setLevel(logging.DEBUG)
logger.addStreamHandler()

SSLManager().run(sys.argv[2::])
    
