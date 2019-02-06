from flask import Flask
from flask_socketio import SocketIO
app = Flask(__name__)
sio = SocketIO(app)

import web.controller
