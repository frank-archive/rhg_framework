from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import json
import time
import subprocess
import threading

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
log_thread = None


def start_py_with_log(pyfile):
    global process, log_queue, log_thread
    if process is not None and isinstance(process, subprocess.Popen):
        process.kill()
    process = subprocess.Popen(['python3', pyfile],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    log_queue = []
    log_thread = threading.Thread(target=write_log)
    log_thread.start()


def write_log():
    global log_queue, process
    while process.returncode == None:
        log_queue.append(process.communicate()[1].decode())
        time.sleep(1)
    try:
        log_queue.append(process.communicate()[1].decode())
    except:
        None
    log_queue.append('process finished')


@app.route('/run/<target>/<action>')
def run_target(target, action):
    global process, log_thread
    if target == 'main':
        if action == 'start':
            start_py_with_log('main.py')
            return 'success'
        elif action == 'stop':
            process.kill()
            if log_thread.is_alive():
                log_thread.join()
            log_thread = None
            process = None
            return 'success'
        elif action == 'log':
            if len(log_queue) > 0:
                ret = ''
                while len(log_queue) > 0:
                    ret += log_queue.pop(0)
                return ret.replace('\n', '<br>').replace(' ', '&nbsp;')
            return ''
        else:
            return 'wrong action'
    elif target == 'panel':
        if action == 'show':
            return 'not implemented yet'  # run_panel.html
    return 'error target'



@app.route('/pyrender/<directory>/<script>', methods=['GET', 'POST'])
def render(directory, script):
    if directory not in ['exploit', 'fix', 'recognizer']:
        return ''
    if request.method == 'POST':
        with open(directory+'/'+secure_filename(script), 'w') as f:
            f.write(request.data.decode())
        return 'success'
    else:
        with open(directory+'/'+secure_filename(script), 'r') as f:
            return render_template('pyrender.html', code=f.read())


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=80)
