#encoding:utf8
from flask import Flask,request, Response, jsonify
from flask_login import (LoginManager, login_required, login_user,
                             logout_user, UserMixin,current_user)
import json
from main2 import app,login_manager,check
from main.tools import *
from main.model import *


# user models
class User(UserMixin):
    def __init__(self,user ):
        self.__dict__ = user.__dict__
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    user = loaduser("id='%d'"%user_id)
    return User(user)

#注册
#测试链接 http://127.0.0.1:5000/cr
@app.route("/reg", methods=['GET', 'POST'])
def reg():
    js = json.loads(request.data)
    ret=check(js,"reg")
    if ret.result == "200":
        js["val"]["status"]="1"
        js["val"]["job"]="19"
        fields=",".join(map( lambda x: "'"+x+"'", js["val"].keys()))
        values=",".join(map( lambda x: "'"+x+"'", js["val"].values()))
        sql = "insert into user({0}) values({1})".format(fields,values)
        try:
            conn.execute(sql)
            user = loaduser("account='%s'"%js["val"]["account"])
            login_user(User(user))
        except Exception as e:
            if e.args[0].find( 'UNIQUE constraint failed: user.account' ) != -1:
                ret.result = 1001
                ret.msg = "用户名已存在"
            else:
                ret.result = 1000
                ret.msg = "其他错误"
    return Response(tojson(ret), mimetype='application/json')
 
@app.route('/login')
def login():
    param = request.args.to_dict()
    user = loaduser("account='%s'"%param["account"])
    r = obj(result="404",fun="login")
    if user is not None and user.pwd == param["pwd"]:
        if user.status == -1:
            return tojson(r)
        login_user(User(user))
        r.result = 200
        fmt = '{"login":"%s","result":"200","nexturl":"%s"}'
        if 0<user.status<6:
            r.nexturl='/static/user_init'+str(user.status)+'.html'
        else:
            r.nexturl='/static/portal.html'
    return tojson(r)

@app.route('/chgpwd', methods=['POST'])
@login_required
def chgpwd():
    jsn = json.loads(request.data)
    ret=obj(fun="chgpwd", result="200")
    if current_user.id != int(jsn["id"]):
        ret.result = "1002"
        ret.msg = "你不能修改别人的密码"
    if current_user.pwd != jsn["pwd"]:
        ret.result = "1002"
        ret.msg = "旧密码不正确"
    if ret.result == "200":
        sql = "update user set pwd='{0}' where id={1}".format(jsn["newpwd"], jsn["id"])
        conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')
 
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    ret=obj(fun="logout", result="200")
    return Response(tojson(ret), mimetype='application/json')

