import json
import judge_utils
import subprocess
import threading
import logging
import coloredlogs, logging

BRUTE = False  # 所有题把所有的exp和fix都试一遍
DEBUG = True

config = None
with open('config.json', 'r') as f:
    config = json.loads(f.read())

api_base = config['api_base']
vuls = config['vuls']
reset_defend_after_fail = config['reset_env_after_fail_attempt']['defend']
reset_attack_after_fail = config['reset_env_after_fail_attempt']['attack']
correct_flags = []

log = logging.getLogger(__name__)
coloredlogs.install(
    level='DEBUG',
    logger=log,
    fmt='%(asctime)s [%(process)d-%(filename)s] %(levelname)s %(message)s'
)

def exec_python(cmd, json_arg, pyver='python2'):
    return subprocess.run([
        pyver+' '+cmd,
        json_arg
    ]).stdout.decode()


def try_exploit(question, vul):
    for exp in vul['exploit']:
        log.debug(f'开始尝试利用脚本{exp}进行攻击')
        flags = exec_python(exp, question)
        for flag in flags.split('\n'):
            if flag in correct_flags:
                log.debug(f'已经提交过{flag}')
                continue
            if judge_utils.submit_flag(api_base, question, flag):
                log.info(f'题目{question}攻击成功,flag为{flag}')  # logger
                correct_flags.append(flag)
            else:
                log.debug(f'{flag[:10]}...答案错误')


def try_fix(question, vul):
    for i in vul['fix']:
        log.debug(f'开始尝试利用脚本{i}修复漏洞点')
        exec_python(i, json.dumps(question))
        judge_utils.call_defend_check(api_base, question)
        if judge_utils.is_defend_success(api_base, question):
            log.info(f'题目{question}防御成功')
            return
        judge_utils.reset_defend_env(api_base, question)


if __name__ == '__main__':
    questions = judge_utils.get_questions(api_base)
    for i in questions:
        for j in vuls.keys():
            if not BRUTE and 'vulnerable' in exec_python(config['vuls'][j]['matcher'], json.dumps(i)):
                if not DEBUG:
                    threading.Thread(try_exploit, args=(i, config['vuls'][j])).start()
                    threading.Thread(try_fix, args=(i, config['vuls'][j])).start()
                else:
                    try_exploit(i, config['vuls'][j])
                    try_fix(i, config['vuls'][j])
