# rhg_framework

## 比赛中需要修改的文件:

|文件名|说明|
|:-:|:-:|
|vulnerabilities.json|请按照vulnerabilities_comment.jsonc的说明进行修改|
|judge_utils.py|修改提交flag，调用心跳等接口的实现细节|
|exploit/*.py|编写vulnerabilities中提到的exp，**请务必不要在stdout中输出不是flag的内容**|

## 对各部分的说明

### exploit

对所有的exp，都将以popen的形式进行执行。程序将接受一组参数，其描述如下：  
//TODO

exp**只应当**向STDOUT输出flag，多个flag间以"\n"间隔，**日志请输出到STDERR**

### recognizer

recognizer用于识别题目中是否含有对应的漏洞，同样以popen的形式执行。程序将接受一组参数，其描述如下：  
//TODO

对于每个可能出现的漏洞，都应当编写一个recognizer，并且填写到vulnerabilities.json中  
**在题目可能含有对应漏洞时STDOUT中应当含有vulnerable字样，没有时*不应*含有vulnerable**
