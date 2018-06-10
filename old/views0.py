#encoding:utf8
from flask import request,Response,jsonify
import json
from model import *
from flask_login import (LoginManager, login_required, login_user,logout_user, UserMixin,current_user)

import pdb

from flask import Blueprint
main = Blueprint('main', __name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/static/login.json'
main.static_folder="static\\"

class User(UserMixin):
    def __init__(self,user ):
        self.__dict__ = user.__dict__
    def get_id(self):
        return self.id                                 
        
@login_manager.user_loader
def load_user(user_id):
    user = loaduser("id='%d'"%user_id)
    return User(user)
 
#首页
@main.route("/")
def index():
    return main.send_static_file('frame.html')

@main.route("/test")
def test():
    return 'haha!'

#注册
#测试链接 http://127.0.0.1:5000/cr
@main.route("/reg", methods=['GET', 'POST'])
def reg():
    js = json.loads(request.data)
    ret=check(js,"reg")
    if ret.result == "200":
        js["val"]["status"]="1"
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
 
@main.route('/login')
def login():
    param = request.args.to_dict()
    user = loaduser("account='%s'"%param["account"])
    if user is not None and user.pwd == param["pwd"]:
        login_user(User(user))
        fmt = '{"login":"%s","result":"200","nexturl":"%s"}'
        if 0<user.status<6:
            return fmt%(param['account'], '/static/user_init'+str(user.status)+'.html')
        else:
            return fmt%(param['account'], '/static/frame.html')
    else:
        return '{"login":"'+param['account']+'","result":404}\n'

#frame用来读取当前用户信息，需要所在单位名称、下级单位列表
@main.route("/curuserinf")
@login_required
def curuserinf():
    ret = QueryObj( "select * from user where id="+str(current_user.id))
    if len(ret) <= 0:
        return '{"roleuser":"'+param['account']+'","result":404}\n'
    user = ret[0]
    del user.pwd

    #找到用户的所在单位，若所在单位是风场，则需要读取风区列表
    if atoi(user.depart_table) != 0: 
        tbl = gettbl(user.depart_table)
        user.depart = QueryObj( "select id, name from "+tbl["name"]+" where id="+str(user.depart_id))[0]
        if tbl["name"] == "winder":
            user.subs = QueryObj( "select id, name from winderarea where winder_id="+str(user.depart_id))
    ret=obj()
    ret.fun="curuserinf"
    ret.result = "200"
    ret.data = user
    ret.fields=QueryObj(select(base.sl).where(base.c.table=="user"))
    return Response(tojson(ret), mimetype='application/json')

#查询
#测试链接 http://127.0.0.1:5000/rd?ls=[表名]&key1=val1&key2=val2....
@main.route("/rd")
def rd():
    d = request.args.to_dict()
    ls = d["ls"]
    del d["ls"]

    # 限制对部分表的查询
    if ls== "base" or ls == "user":
        return '{result:404,msg:"'+ls+''' isn't callable!"}'''

    if ls== "scale" or ls == "mainmat" or ls== "job" or ls== "skill" or ls=="ethnic":
        d["type"]=ls
        ls = "config"

    sql = "select * from "+ls
    if len(d) > 0:
        sql += " where "+" and ".join([ To(k,v) for k,v in d.items()])
    ol=query(ls,fields=select(base.sl).where(base.c.table==ls),data = sql)
    return Response(tojson(ol), mimetype='application/json')
