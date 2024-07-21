# encoding:utf-8

import logging
import sys
from datetime import datetime

#LEVEL = logging.DEBUG
LEVEL = logging.INFO
#LEVEL = logging.WARNING
#LEVEL = logging.ERROR
#LEVEL = logging.CRITICAL

logging.basicConfig(filename=datetime.now().strftime('%Y-%m-%d-%H-%M-%S.log'),\
                    level = LEVEL,\
        format = '%(asctime)s %(filename)s %(funcName)s line%(lineno)s %(levelname)s - %(message)s')
logger = logging.getLogger()
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logger.info("start logging")