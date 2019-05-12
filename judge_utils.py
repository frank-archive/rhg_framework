import requests


class Question:
    def __init__(self, json):
        return


def get_questions(api_base) -> list(Question):
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
        ret.append(Question(i))
    return ret


def submit_flag(api_base, q: Question, flag) -> bool:
    """
    此函数用于调用提交flag接口
    返回flag是否正确
    其中q为提交的题目信息
    """
    return requests.post(
        api_base+"/sub_answer",
        data={"answer": flag}
    ).json()['status'] == 1

