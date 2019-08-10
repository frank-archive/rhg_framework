import judge_utils
import time
import logging
import coloredlogs

log = logging.getLogger(__name__)
coloredlogs.install(
    level='DEBUG',
    logger=log,
    fmt='%(asctime)s [%(process)d-%(filename)s] %(levelname)s %(message)s'
)
stop_heartbeat = False


def start_heartbeat(api_base):
    while True:
        try:
            judge_utils.heartbeat(api_base)
            log.info('heartbeat success')
            t = 60
        except:
            log.error('heartbeat failed, retrying in 20')
            t = 20
        while t > 0:
            t -= 1
            time.sleep(1)
            if stop_heartbeat == True:
                return
