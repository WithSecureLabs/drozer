#!/usr/bin/python

import logging
import sys

from mwr.common import logger

from drozer.shellcode.manager import ShellCodeManager

logger.setLevel(logging.DEBUG)
logger.addStreamHandler()

ShellCodeManager().run(sys.argv[2::])
