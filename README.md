# rhg_framework

## 对框架的一些说明

为了避免RHG比赛中出现“Python一时爽，队友火葬场”的情况，试图编写此框架。  
设计思路：

* 框架应保证每个脚本能够独立执行，并且在框架中自动化执行时保留相同的行为
* 避免/尽量不使用数据库，方便配置与修改
* 做到解题步骤与评测机交互操作完全分离，使代码逻辑清晰
* 赛前准备时只需要上传与修改脚本即可，不需要过多修改配置


## 比赛前/中需要修改的文件:

|文件名|说明|
|:-:|:-:|
|config.json|请按照config_comment.jsonc的说明进行修改**非必要时不必修改**|
|judge_utils.py|修改提交flag，调用心跳等接口的实现细节|
|exploit/*.py|编写config.json中提到的exp，**请务必不要在stdout中输出不是flag的内容**|

## 使用说明

比赛前在robot机上只需要执行`python3 main.py`启动即可  
请保证所有依赖都装好，框架自身依赖请`pip3 install -r requirements.txt`。  
每个脚本的行为应符合以下说明

## 对各部分的说明

### exploit

对所有的exp，都将以popen的形式进行执行。程序将从STDIN获取到题目的相关信息。  
一般来说，题目信息以JSON的格式给出

> 注：此处考虑到每次比赛题目的形式可能不一样，故没有给出题目的具体结构

exp**只应当**向STDOUT输出flag，多个flag间以"\n"间隔，**日志请输出到STDERR**

### fix

fix目录下为修复脚本，以popen形式执行。  
程序将从STDIN获取到题目相关信息, 与exp获取到的信息相同

对于出现的漏洞，编写能够修复漏洞的脚本，不需要向STDOUT输出，日志请输出到STDERR

### recognizer

recognizer用于识别题目中是否含有对应的漏洞，同样以popen的形式执行。  
程序将从STDIN获取到题目相关信息, 与exp获取到的信息相同

对于每个可能出现的漏洞，都应当编写一个recognizer，并且填写到config.json中  
**在题目可能含有对应漏洞时STDOUT中应当含有vulnerable字样，没有时*不应*含有vulnerable**

### logs

脚本运行生成的日志。对于每个脚本有单独的日志，也有合并的日志。

### static

用于上传exp, fix, recognizer等脚本的网页前端
