from web import app, sio
from flask import request, render_template, jsonify
from flask_socketio import join_room, emit
from mods import CodeType
from mods.file_writer import write_file
from mods.file_runner import run_file


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/runCode', methods=['POST'])
def run_python_code():
    code_type = CodeType[request.form[u"codeType"].upper()]
    code_text = request.form[u"codeText"]
    print('Type: {}\n - Code - \n{}'.format(code_type.name, code_text))
    file_path = write_file(code_type, code_text)
    return jsonify(file_path=file_path)


@sio.on('connect', namespace='/ide-pyo')
def connect():
    print('client connected..!')


@sio.on('handshake', namespace='/ide-pyo')
def handshake(data):
    print('handshake..! data: ', data)


@sio.on('disconnect', namespace='/ide-pyo')
def disconnect():
    print('client disconnected..!')


@sio.on('join_result', namespace='/ide-pyo')
def join_result(data):
    rid = data['rid']
    file_path = data['file_path']
    join_room(rid)
    emit('join_result', {'rid': rid, 'file_path': file_path}, json=True, room=rid, namespace='/ide-pyo')
    return jsonify({'rid': rid, 'file_path': file_path})


@sio.on('get_result', namespace='/ide-pyo')
def get_result(data):
    rid = data['rid']
    file_path = data['file_path']
    code_type = CodeType[data['code_type'].upper()]
    for line in run_file(code_type, file_path):
        if line != 0:
            emit('get_result', {'rid': rid, 'line': line}, json=True, room=rid, namespace='/ide-pyo')
    return jsonify({'is_success': True})
