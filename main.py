import json
import judge_utils
import question_solver
import rev_shell_receiver
import threading

with open('config.json', 'r') as f:
    config = json.loads(f.read())
DEBUG = config['globals']['debug']

api_base = config['api_base']
revsh = threading.Thread(target=rev_shell_receiver.createSocket)
revsh.start()
solves = []

if __name__ == '__main__':
    questions = judge_utils.get_questions(api_base)
    try:
        for i in questions:
            if DEBUG:
                question_solver.solve(i)
            else:
                solves.append(
                    threading.Thread(target=question_solver.solve,args=[i])
                )
                solves[-1].start()
        for i in solves:
            i.join()
    except KeyboardInterrupt:
        'stopped'
    rev_shell_receiver.stop_thread = True
    revsh.join()
