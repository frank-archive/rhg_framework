from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import json
import time
import subprocess

app = Flask(__name__)

with open('config.json') as f:
    config = json.loads(f.read())
back_button = '<input type="button" name="submit" value="返回" onclick="javascript:history.back()" />'


def update_config():
    with open('config.json', 'w') as f:
        f.write(json.dumps(config, indent=4, sort_keys=True))


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', time=time.asctime())


@app.route('/vuls')
def vuls_index():
    return render_template(
        'vuls_index.html',
        vul_list=config['vuls'].keys()
    )


@app.route('/vuls/<name>')
def vul_detail(name):
    if(name not in config['vuls'].keys()):
        return '漏洞不存在'
    return render_template(
        'vul_detail.html',
        vul_name=name,
        exp_list=config['vuls'][name]['exploit'],
        fix_list=config['vuls'][name]['fix'],
        matcher=config['vuls'][name]['matcher']
    )


@app.route('/vuls/<name>/create')
def vuls_create(name):
    if name in config['vuls'].keys():
        return '已存在名为'+name+'的漏洞'+back_button
    config['vuls'][name] = {
        'matcher': "",
        'exploit': [],
        'fix': []
    }
    update_config()
    return '添加成功'+back_button


@app.route('/vuls/<vul_name>/upload/<directory>', methods=['POST'])
def vuls_upload(vul_name, directory):
    if 'file' not in request.files or request.files['file'].filename == '':
        return '上传内容为空'
    file = request.files['file']
    if file.filename[-3:] != '.py':
        return '上传python脚本'
    if directory not in ['exploit', 'fix', 'recognizer']:
        return ''  # maybe hack
    if vul_name not in config['vuls'].keys():
        return '没有此漏洞条目'
    file.save(directory+'/'+secure_filename(file.filename))
    config['vuls'][vul_name][directory].append(
        directory+'/'+secure_filename(file.filename))
    update_config()
    return 'saved to '+directory+'/'+secure_filename(file.filename)+back_button


@app.route('/run')
def run_index():
    return render_template('run_index.html')


log_queue = []
process = None
@app.route('/run/<target>/<action>')
def run_target(target, action):
    global log_queue, process
    if target == 'main':
        if action == 'start':
            if process is not None and isinstance(process, subprocess.Popen):
                process.kill()
            process = subprocess.Popen(['python3', 'main.py'],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            log_queue = []
            log_queue.append(process.communicate()[1].decode())
            return 'success'
        elif action == 'stop':
            process.kill()
            process = None
            return 'success'
        else:
            return 'wrong action'
    return '? not implemented'


@app.route('/run/log/<name>')
def log(name):
    global log_queue
    if len(log_queue) > 0:
        ret = ''
        while len(log_queue) > 0:
            ret += log_queue.pop(0)
        return ret.replace('\n', '<br>').replace(' ', '&nbsp;')
    return ''


@app.route('/pyrender/<directory>/<script>')
def render(directory, script):
    if directory not in ['exploit', 'fix', 'recognizer']:
        return ''
    with open(directory+'/'+secure_filename(script), 'r') as f:
        return render_template('pyrender.html', code=f.read())


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=80)
