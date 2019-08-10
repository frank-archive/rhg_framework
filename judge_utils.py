import requests
import json
requests.packages.urllib3.disable_warnings()

def describe_question(question) -> str:
    """
    此函数用于简单描述一道题目，用于日志输出
    """
    return str(question['challengeID'])


def get_questions(api_base) -> list:
    """
    此函数将调用比赛的获取题目信息接口并解析
    返回题目列表
    """
    return requests.get(
        api_base+"/get_question_status",
        headers={"User-Agent": "curl/7.63.0"},
        auth=('student02', 'JMc4UotE'),
        verify=False
    ).json()["AiChallenge"]


def submit_flag(api_base, q, flag) -> bool:
    """
    此函数用于调用提交flag接口
    返回flag是否正确
    其中q为提交的题目信息
    """
    return requests.post(
        api_base+"/sub_answer",
        data={"answer": flag},
        auth=('student02', 'JMc4UotE'),
        verify=False
    ).json()['status'] == 1


def call_defend_check(api_base, q) -> None:
    '''
    此函数用于请求对防御机进行check
    一般无返回值
    '''
    return requests.post(
        api_base+'/call_question_check',
        data={
            "ChallengeID": q['challengeID']
        },
        auth=('student02', 'JMc4UotE'),
        verify=False
    ).json()['status'] == 1


def is_defend_success(api_base, q) -> bool:
    '''
    此函数用于判断一道题是否防御成功
    返回布尔值表示是否防御成功
    '''
    for i in requests.get(
        api_base+'/get_check_info',
        auth=('student02', 'JMc4UotE'),
        verify=False
    ).json()['check_status']:
        if i['challengeID'] == q['challengeID']:
            return (i['web'] == [1, 0] or i['server'] == [1, 0])
    return False


def reset_defend_env(api_base, q):
    '''
    此函数用于重置题目防御环境
    在config.json中配置是否每次防御失败后都调用
    '''
    return requests.post(
        api_base+'/reset_question',
        data={
            'ChallengeID': q['challengeID'],
            'type': 2
        },
        auth=('student02', 'JMc4UotE'),
        verify=False
    )


def reset_attack_env(api_base, q):
    '''
    用于重置攻击环境
    config.json中配置
    '''
    return requests.post(
        api_base+'/reset_question',
        data={
            'ChallengeID': q['challengeID'],
            'type': 2
        },
        auth=('student02', 'JMc4UotE'),
        verify=False
    )

def heartbeat(api_base):
    '''
    心跳
    '''
    requests.get(
        api_base + '/heartbeat',
        auth=('student02', 'JMc4UotE'),
        verify=False
    )
