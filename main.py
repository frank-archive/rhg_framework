import json
import judge_utils
import subprocess

BRUTE = True  # 所有题把所有的exp和fix都试一遍
config = json.load(open('config.json', 'r'))
api_base = config['api_base']
vuls = config['vuls']


def exec_python(cmd, json_arg, pyver='python2'):
    return subprocess.run([pyver+' '+cmd, json_arg]).stdout.decode()


def solve_question(q: judge_utils.Question):
    for j in vuls:
        if not BRUTE and 'vulnerable' in exec_python(j['matcher'], json.dumps(q)):
            flags = exec_python(j['exploit'], json.dumps(q))
            for flag in flags.split('\n'):
                if judge_utils.submit_flag(api_base, q, flag):
                    print(f'攻击成功,flag为{flag}')  # logger
                    break  # 攻击成功
            for i in j['fix']:
                exec_python(i, json.dumps(q))
                judge_utils.call_check(api_base, i)
            judge_utils.update_check_info(api_base)
            #if success: print('防御成功')


if __name__ == '__main__':
    questions = judge_utils.get_questions(api_base)
    for i in questions:
        solve_question(i)
