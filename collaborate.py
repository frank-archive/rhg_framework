from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import json
import time

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
    )


@app.route('/vuls/<name>')
def vul_detail(name):
    return render_template(
        'vul_detail.html',
        vul_list=config['vuls'].keys()
    )


@app.route('/vuls/<name>/create')
def vuls_create(name):
    if name in [i['name'] for i in config['vuls']]:
        return '已存在名为'+name+'的漏洞'+back_button
    config['vuls'][name] = {
        'matcher': [],
        'exploit': [],
        'fix': []
    }
    update_config()
    return '添加成功'+back_button


@app.route('/vuls/<vul_name>/upload/<directory>/<script_name>', )
def vuls_upload(vul_name, directory, script_name, methods=['POST']):
    '''
    POST {
        "script": the script to save
    }
    '''
    if(len(script_name) == 0):
        return '文件名为空'
    if directory not in ['exploit', 'fix', 'recognizer']:
        return ''  # maybe hack
    fn = secure_filename(script_name)
    with open(directory+'/'+fn, 'w') as f:
        f.write(request.form['script'])
    config['vuls'][vul_name][directory].append(directory+'/'+script_name)
    update_config()
    return 'saved to '+directory+'/'+fn+back_button


if __name__ == '__main__':
    app.run('0.0.0.0', debug=False, port=80)
