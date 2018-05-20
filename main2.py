#encoding:utf8
from flask import Flask,request, Response, jsonify
from flask_sockets import Sockets
from werkzeug.utils import secure_filename
from flask_login import (LoginManager, login_required, login_user,
                             logout_user, UserMixin,current_user)
#flask_sqlalchemy方式的使用
#from flask_sqlalchemy import SQLAlchemy
#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///./db/pecker.db'
#app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"]=True
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True
#db = SQLAlchemy(app)
#@app.route("/aa")
#def index():
#    result = db.get_engine().execute("select * from user where id<100").paginate()
#    return app.send_static_file('frame2.html')


import os.path
import json
import pdb

app = Flask(__name__)
sockets = Sockets(app)
app.secret_key = '1The2quick3brown4fox5jumps6over7the8lazy9dog0'
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/static/login.json'
login_manager.init_app(app)

from main.tools import *
from main.model import *

#权限检查
def check(js,th):
    return obj(result="200")

#首页
@app.route("/")
def index():
    return app.send_static_file('frame2.html')

############## kindedit功能 ###############################################
@app.route("/kedit", methods=['GET', 'POST'])
def kedit():
    params = request.args.to_dict()
    files = request.files.to_dict()
    dic =request.form.to_dict()

    if "m" not in param:
        return '{"error" : 1,"message" : "缺少参数m"}'

    ret =obj();
    for k,v in files.items(): 
        fname = "./uploads/{m}/{id}{ext}".format(params["m"],id=rndstr(),ext=os.path.splitext(v.filename)[1] )
        dic[k]=fname
        v.save("./static/"+fname)
        ret.error = 0
        ret.url = fname

    r = '{"error" : 0,"url" : "'+fname+'"}'
    return r


############## websocket功能 ###############################################

#@sockets.route('/echo')
#def echo_socket(ws):
#    while not ws.closed:
#        message = ws.receive()             
#        ws.send("replay:"+message+"!")

#############################################################

from main.auth import *
from main.views import *
from main.blog import *
from main.user import *

class CLog:
    def write(data):
        print(data)
    def writelines(data):
        print(data)
    def flush():
        pass

if __name__ == "__main__":
    newdir(["./static/uploads","./static/uploads/user_face","./static/uploads/user_idimg","./static/uploads/certif_image",
            "./static/uploads/employ_image", "./static/uploads/edu_image1", "./static/uploads/edu_image2"]);
    app.config['JSON_AS_ASCII'] = False
    #app.config['DEBUG'] = True
    print( app.url_map )
    app.run( host="0.0.0.0" )
    #from gevent import pywsgi
    #from geventwebsocket.handler import WebSocketHandler
    #log = CLog();
    #server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler, log=log,error_log=log)
    #server.serve_forever()

#暂未限制Query对User的查询
#添加QueryUser接口，密码处理，所在单位处理
#风场面板中还没有相关人员显示。

