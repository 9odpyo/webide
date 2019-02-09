from web import app, sio
from flask import request, render_template, jsonify
from flask_socketio import join_room, emit
from mods.file_writer import write_file
from mods.file_runner import run_file


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/runCode', methods=['POST'])
def run_code():
    code = request.form[u"code"]
    print(code)
    file_path = write_file(code)
    return jsonify(file_path=file_path)


@sio.on('connect', namespace='/ide-py')
def connect():
    print('client connected..!')


@sio.on('handshake', namespace='/ide-py')
def handshake(data):
    print('handshake..! data: ', data)


@sio.on('disconnect', namespace='/ide-py')
def disconnect():
    print('client disconnected..!')


@sio.on('join_result', namespace='/ide-py')
def join_result(data):
    rid = data['rid']
    file_path = data['file_path']
    join_room(rid)
    emit('join_result', {'rid': rid, 'file_path': file_path}, json=True, room=rid, namespace='/ide-py')
    return jsonify({'rid': rid, 'file_path': file_path})


@sio.on('get_result', namespace='/ide-py')
def get_result(data):
    rid = data['rid']
    file_path = data['file_path']
    for line in run_file(file_path):
        if line != 0:
            emit('get_result', {'rid': rid, 'line': line}, json=True, room=rid, namespace='/ide-py')
    return jsonify({'is_success': True})
