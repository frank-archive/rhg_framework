from paramiko import SSHClient, AutoAddPolicy

import logging
import coloredlogs
import json

json.loads(input())

log = logging.getLogger(__name__)
coloredlogs.install(
    level='DEBUG',
    logger=log,
    fmt='%(asctime)s [%(process)d-%(filename)s] %(levelname)s %(message)s'
)
log.addHandler(logging.FileHandler(
    'logs/solver.log'
))
log.info('asdfasdf')
log.error('asdfasdf')