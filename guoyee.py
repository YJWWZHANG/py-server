#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, abort, request, jsonify, send_from_directory, Response
import json, os, hashlib
from version import Version

app = Flask(__name__)

tasks = []

with open('./pinche/version.json', 'rb') as f:
    pincheVersion = json.loads(f.read(), object_hook=lambda d: Version(d['update'], d['new_version'],
        d['apk_file_url'], d['update_log'], d['target_size'], d['new_md5'], d['constraint']))

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>欢迎来到国业电子</h1>'

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.form and 'id' in request.form and 'info' in request.form:
        task = {
            'id': int(request.form.get('id')),
            'info': request.form.get('info')
        }
        tasks.append(task)
        return jsonify({'result': 'success'})
    else:
        abort(400)

@app.route('/get_task', methods=['GET'])
def get_task():
    if not request.args or 'id' not in request.args:
        return jsonify(tasks)
    else:
        task_id = request.args['id']
        task = list(filter(lambda t: t['id'] == int(task_id), tasks))
        return jsonify(task) if task else jsonify({'resule': 'not found'})

@app.route('/guoyee/pinche/version', methods=['GET'])
def check_update():
    return json.dumps(pincheVersion, default=lambda obj: obj.__dict__, ensure_ascii=False), {'Content-Type': 'application/json'}

@app.route('/guoyee/pinche/download/pinche.apk', methods=['GET'])
def download_file():
    return send_from_directory('pinche','pinche.apk',as_attachment=True)

@app.route('/guoyee/pinche/upload', methods=['POST'])
def upload():
    if 'new_version' in request.form and 'update' in request.form and 'constraint' in request.form and 'file' in request.files and 'update_log' in request.form:
        pincheVersion.new_version = request.form.get('new_version')
        pincheVersion.update = request.form.get('update')
        pincheVersion.constraint = request.form.get('constraint')
        pincheVersion.update_log = request.form.get('update_log')
        apkFile = request.files.get('file')
        apkFile.save('./pinche/pinche.apk')
        pincheVersion.target_size = '%.2fM' % (os.path.getsize('./pinche/pinche.apk') / 1024 / 1024 )
        with open('./pinche/pinche.apk', 'rb') as f:
            pincheVersion.new_md5 = hashlib.md5(f.read()).hexdigest()
        with open('./pinche/version.json', 'w') as f:
            f.write(json.dumps(pincheVersion, default=lambda obj: obj.__dict__, ensure_ascii=False))
        return jsonify({'result': 'success'})
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

