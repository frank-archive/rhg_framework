import logging
import coloredlogs
import json
import re
import subprocess
import judge_utils
import threading

with open('config.json', 'r') as f:
    config = json.loads(f.read())
DEBUG = config['globals']['debug']
BRUTE = config['globals']['brute']
MATCH_FLAG = config['globals']['flag_match']
api_base = config['api_base']
vuls = config['vuls']
reset_defend_after_fail = config['reset_env_after_fail_attempt']['defend']
reset_attack_after_fail = config['reset_env_after_fail_attempt']['attack']

correct_flags = []

fh = logging.FileHandler(
    'logs/solver.log'
)
fh.setFormatter(
    logging.Formatter(
        '%(asctime)s [%(process)d-%(filename)s] %(levelname)s %(message)s'
    )
)
log = logging.getLogger(__name__)
log.addHandler(fh)
coloredlogs.install(
    level='DEBUG',
    logger=log,
    fmt='%(asctime)s [%(process)d-%(filename)s] %(levelname)s %(message)s'
)


def exec_python(cmd, json_arg: str, pyver='python3'):
    log.debug(f"执行{cmd}文件")
    try:
        process = subprocess.run(
            [pyver, cmd], input=json_arg.encode(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=10
        )
        return process.stdout.decode(), process.stderr.decode()
    except:
        return '',''


def try_exploit(question, vul):
    for exp in vul['exploit']:
        log.debug(f'开始尝试利用脚本{exp}进行攻击')
        pyver = 'python3'
        with open(exp, 'r') as f:
            if 'python2' in f.readline():
                pyver = 'python2'
        flags, exp_log = exec_python(exp, json.dumps(question), pyver=pyver)
        with open(f'logs/{exp.replace("/", "_")}.log', 'w') as f:
            f.write(exp_log)

        for flag in re.findall(MATCH_FLAG, flags):
            print(flag)
            if flag in correct_flags:
                log.warning(f'已经提交过{flag}')
                continue
            if judge_utils.submit_flag(api_base, question, flag):
                # logger
                log.info(
                    f'题目{judge_utils.describe_question(question)}攻击成功,flag为{flag},利用脚本{exp}'
                )
                correct_flags.append(flag)
            else:
                log.warning(f'{flag[:10]}...答案错误')


def try_fix(question, vul):
    for i in vul['fix']:
        log.debug(f'开始尝试利用脚本{i}修复漏洞点')
        pyver = 'python3'
        with open(i, 'r') as f:
            if 'python2' in f.readline():
                pyver = 'python2'
        stdout, fix_log = exec_python(i, json.dumps(question), pyver=pyver)
        with open(f'logs/{i.replace("/", "_")}.log', 'w') as f:
            f.write(fix_log)
        if(stdout != ""):
            log.debug(f"修复脚本{i}输出了:\nBEGIN_STDOUT\n{stdout}\nEND_STDOUT")
        judge_utils.call_defend_check(api_base, question)
        if judge_utils.is_defend_success(api_base, question):
            log.info(f'题目{judge_utils.describe_question(question)}防御成功')
            return
        judge_utils.reset_defend_env(api_base, question)


def solve(i):
    log.debug("开始解题: 题目"+judge_utils.describe_question(i))
    for j in vuls.keys():
        log.info(f'开始打题目{judge_utils.describe_question(i)}')
        if not DEBUG:
            threading.Thread(target=try_exploit, args=(
                i, config['vuls'][j])).start()
            threading.Thread(target=try_fix, args=(
                i, config['vuls'][j])).start()
        else:
            try_exploit(i, config['vuls'][j])
            try_fix(i, config['vuls'][j])


def check_submit(flag, source):
    if judge_utils.submit_flag(api_base, {}, flag):
        # logger
        log.info(
            f'攻击成功,flag为{flag},来自{source}'
        )
        correct_flags.append(flag)
    else:
        log.warning(f'{flag[:10]}...答案错误')


if __name__ == '__main__':
    solve(json.loads(input()))
