import json
import judge_utils
import question_solver

config = None
with open('config.json', 'r') as f:
    config = json.loads(f.read())

api_base = config['api_base']

if __name__ == '__main__':
    questions = judge_utils.get_questions(api_base)
    for i in questions:
        question_solver.solve(i)
