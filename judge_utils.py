import requests

def get_questions(api_base) -> list(dict):
    """
    此函数将调用比赛的获取题目信息接口并解析
    返回题目列表
    """
    ret = []
    for i in requests.get(
        api_base+"/get_question_status",
        headers={"User-Agent": "curl/7.63.0"},
        auth=('student07', '')
    ).json()["AiChallenge"]:
        ret.append(i)
    return ret


def submit_flag(api_base, q, flag) -> bool:
    """
    此函数用于调用提交flag接口
    返回flag是否正确
    其中q为提交的题目信息
    """
    return requests.post(
        api_base+"/sub_answer",
        data={"answer": flag},
        auth=('student07', '')
    ).json()['status'] == 1


def call_defend_check(api_base, q) -> None:
    '''
    此函数用于请求对防御机进行check
    一般无返回值
    '''
    requests.post(
        api_base+'/call_question_check',
        data={
            "ChallengeID": q['challengeID']
        },
        auth=('student07', '')
    ).json()['status'] == 1
    return


def is_defend_success(api_base, q) -> bool:
    '''
    此函数用于判断一道题是否防御成功
    返回布尔值表示是否防御成功
    '''
    requests.get(
        api_base+'/get_check_info',
        auth=('student07', '')
    ).json()['check_status']
    return


def reset_defend_env(api_base, q):
    '''
    此函数用于重置题目防御环境
    在config.json中配置是否每次防御失败后都调用
    '''
    requests.post(
        api_base+'/reset_question',
        data={
            'ChallengeID': q['challengeID'],
            'type': 2
        },
        auth=('student07', '')
    )


def reset_attack_env(api_base, q):
    '''
    用于重置攻击环境
    config.json中配置
    '''
    requests.post(
        api_base+'/reset_question',
        data={
            'ChallengeID': q['challengeID'],
            'type': 2
        },
        auth=('student07', '')
    )