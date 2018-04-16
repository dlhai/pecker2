from flask import Flask,request, Response, jsonify
from flask_sockets import Sockets
app = Flask(__name__)
sockets = Sockets(app)
@sockets.route("/echo")
def echo_socket(ws):
    gLog.debug("ws=%s", ws)
    while not ws.closed:
        message = ws.receive()
        ws.send(message)
@app.route("/")
def hello():
    return "Hello World!"