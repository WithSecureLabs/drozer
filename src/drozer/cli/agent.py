#!/usr/bin/env python

import logging
import sys

from WithSecure.common import logger

from drozer.agent.manager import AgentManager

logger.setLevel(logging.DEBUG)
logger.addStreamHandler()

AgentManager().run(sys.argv[2::])
