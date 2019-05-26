import json
import judge_utils
import question_solver
import rev_shell_receiver
import threading
import zipfile
import os
import shutil

with open('config.json', 'r') as f:
    config = json.loads(f.read())
DEBUG = config['globals']['debug']

api_base = config['api_base']
revsh = threading.Thread(target=rev_shell_receiver.createSocket)
revsh.start()
solves = []

def collect_logs():
    i = 1
    while os.path.exists(f'logs{i}.zip'):
        i += 1
    compressed_logs = zipfile.ZipFile(f'logs{i}.zip', 'w', zipfile.ZIP_DEFLATED)
    for j in os.listdir('logs'):
        compressed_logs.write('logs/'+j)
    shutil.rmtree('logs')
    os.mkdir('logs')
    print(f'dumping logs to logs{i}.zip...')

def main():
    if os.path.exists('logs') == False:
        os.mkdir('logs')
    questions = judge_utils.get_questions(api_base)
    try:
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
        for i in solves:
            i.join()
    except KeyboardInterrupt:
        'stopped'
    collect_logs()
    rev_shell_receiver.stop_thread = True
    revsh.join()

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        exit(0)