import json
import judge_utils
import question_solver
import rev_shell_receiver
import threading
import zipfile
import os
import heartbeat
import time

import logging
import coloredlogs

log = logging.getLogger(__name__)
coloredlogs.install(
    level='DEBUG',
    logger=log,
    fmt='%(asctime)s [%(process)d-%(filename)s] %(levelname)s %(message)s'
)

with open('config.json', 'r') as f:
    config = json.loads(f.read())
DEBUG = config['globals']['debug']

api_base = config['api_base']
revsh = threading.Thread(target=rev_shell_receiver.createSocket)
ping = threading.Thread(target=heartbeat.start_heartbeat, args=[api_base])
revsh.start()
ping.start()
solves = []
log_lock = True


def collect_logs():
    global log_lock
    while log_lock == False:
        continue
    log_lock = False
    i = 1
    compressed_logs = zipfile.ZipFile(
        f'logs{i}.zip', 'w', zipfile.ZIP_DEFLATED)
    for j in os.listdir('logs'):
        compressed_logs.write('logs/'+j)
    os.system('rm -f logs/*')
    print(f'dumping logs to logs{i}.zip...')
    log_lock = True


def main():
    if os.path.exists('logs') == False:
        os.mkdir('logs')
    result = False
    try:
        while not result:
            try:
                log.info('fetching problems')
                questions = judge_utils.get_questions(api_base)
                log.info('fetched problems')
                result = True
            except:
                log.error('problem fetching error, retrying in 10')
                time.sleep(10)
                result = False
        for i in questions:
            if DEBUG:
                question_solver.solve(i)
            else:
                solves.append(
                    threading.Thread(
                        target=question_solver.solve, args=[i]
                    )
                )
                solves[-1].start()
    except KeyboardInterrupt:
        'stopped'
    except:
        pass


if __name__ == '__main__':
    while True:
        try:
            main()
            collect_logs()
            for i in solves:
                i.join()
            time.sleep(5)
        except KeyboardInterrupt:
            confirm = input('exit?(Y/n)')
            if confirm == 'n':
                pass
            else:
                rev_shell_receiver.stop_thread = True
                heartbeat.stop_heartbeat = True
                revsh.join()
                ping.join()
                exit(0)
