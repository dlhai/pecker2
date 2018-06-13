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

#frame用来填用户角色组合框，发布版要删掉
@app.route("/roleuserall")
def roleuserall():
    user = QueryObj( "select min(id) as id, account, name, job, depart_id, depart_table, face from user group by job")
    for u in [x for x in user if atoi(x.depart_table) != 0]:
        tbl = gettbl(u.depart_table)
        u.depart = QueryObj( "select * from "+tbl["name"]+" where id="+str(u.depart_id))[0]
        if tbl["name"] == "winder":
            u.sub = QueryObj( "select id, name from winderarea where winder_id="+str(u.depart_id))
    ret=obj()
    ret.fun="roleuserall"
    ret.result = "200"
    ret.data = user
    return Response(tojson(ret), mimetype='application/json')

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
from main.chat import *
from main.views import *
from main.blog import *
from main.user import *
from main.vender import *
from main.winder import *
from main.dev import *

class CLog:
    def write(data):
        print(data)
    def writelines(data):
        print(data)
    def flush():
        pass

if __name__ == "__main__":
    newdir(["./static/uploads","./static/uploads/user_face","./static/uploads/user_idimg","./static/uploads/certif_image",
            "./static/uploads/employ_image", "./static/uploads/edu_image1", "./static/uploads/edu_image2", 
            "./static/uploads/fault_image","./static/uploads/dev_face","./static/uploads/dev_img"]);
    app.config['JSON_AS_ASCII'] = False
    #app.config['DEBUG'] = True

    #print( app.url_map )
    urlmap = [" <Rule '{r}' {mtd} -> {ep} >,".format(r=x.rule,mtd=x.methods,ep=x.endpoint) for x in app.url_map._rules]
    urlmap.sort()
    [print(x) for x in urlmap]

    app.run( host="0.0.0.0" )
    #from gevent import pywsgi
    #from geventwebsocket.handler import WebSocketHandler
    #log = CLog();
    #server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler, log=log,error_log=log)
    #server.serve_forever()

#暂未限制Query对User的查询
#添加QueryUser接口，密码处理，所在单位处理
#风场面板中还没有相关人员显示。

#功能表：
#    主框架√ 缺单位信息，缺主页，缺搜索
#var db_roles = [
#    {
#        "id": "1", "type": "winder", "name": "叶片超级帐号", modules: [
#            { name: "地图", url: "windersumap.html" },√
#            { name: "风场", url: "windersu.html" },√
#            { name: "人员", url: "user_list2.html" },√
#            { name: "厂家", url: "vender.html" }]√
#    },
#    {
#        "id": "2", "type": "winder", "name": "风场主管", modules: [
#            { name: "地图", url: "windermap.html" },√
#            { name: "设备", url: "winder2.html" },√
#            { name: "案件", url: "coord.html" },
#            { name: "记录", url: "repairlog.html" },
#            { name: "人员", url: "user_list2.html" }]√
#    },
#    {
#        "id": "3", "type": "winder", "name": "驻场", modules: [
#            { name: "地图", url: "windermap.html" },√
#            { name: "设备", url: "winder2.html" },√
#            { name: "案件", url: "coord.html" },
#            { name: "记录", url: "repairlog.html" }]
#    },
#    {
#        "id": "4", "type": "dev", "name": "设备超级帐号", modules: [
#            { name: "地图", url: "devmap.html" },
#            { name: "驻地", url: "devsu.html" },√
#            { name: "人员", url: "user_list2.html" },√
#            { name: "厂家", url: "devvender.html" }]√
#    },
#    {
#        "id": "5", "type": "dev", "name": "驻地主管", modules: [
#            { name: "地图", url: "devmap.html" },
#            { name: "驻地", url: "devwh.html" },√
#            { name: "人员", url: "user_list2.html" }]
#    },
#    {
#        "id": "6", "type": "dev", "name": "设备司机", modules: [
#            { name: "设备", url: "devdriver.html" }]
#    },
#    {
#        "id": "7", "type": "wh", "name": "仓库超级帐号", modules: [
#            { name: "仓库", url: "matsu.html" },
#            { name: "人员", url: "user_list2.html" },
#            { name: "材料", url: "material.html" }]
#    },
#    {
#        "id": "8", "type": "wh", "name": "仓库主管", modules: [
#            { name: "入库", url: "matin.html" },
#            { name: "出库", url: "matout.html" },
#            { name: "查询", subs: [
#               { name: "库存", url: "matquery.html" }, 
#               { name: "入库", url: "matqueryin.html" }, 
#               { name: "出库", url: "matqueryout.html" }]},
#            { name: "人员", url: "user_list2.html" }]
#    },
#    {
#        "id": "9", "type": "wh", "name": "仓库管理员", modules: [
#            { name: "入库", url: "matin.html" },
#            { name: "出库", url: "matout.html" },
#            { name: "查询", subs: [
#               { name: "库存", url: "matquery.html" }, 
#               { name: "入库", url: "matqueryin.html" },
#               { name: "出库", url: "matqueryout.html" }] }],
#    },
#    { "id": "10", "type": "coord", "name": "调度超级帐号", modules: [
#       { name: "人员", url: "user_list2.html" }] },√
#    { "id": "11", "type": "coord", "name": "调度主管", modules: [
#       { name: "案件", url: "coord.html" }, 
#       { name: "记录", url: "repairlog.html" }] },
#    { "id": "12", "type": "coord", "name": "调度", modules: [
#       { name: "案件", url: "coord.html" }, 
#       { name: "记录", url: "repairlog.html" }] },
#    {"id": "13", "type": "expert", "name": "专家超级帐号", modules: [
#       { name: "专家", url: "user_list2.html" }]},
#    {
#        "id": "14", "type": "expert", "name": "专家", modules: [
#            { name: "案件", url: "coord.html" },
#            { name: "记录", url: "repairlog.html" }]
#    },
#    { "id": "15", "type": "repair", "name": "技工超级帐号", modules: [
#       { name: "技工", url: "user_list2.html" }] },
#    {
#        "id": "16", "type": "repair", "name": "维修队长", modules: [
#            { name: "案件", url: "coord.html" },
#            { name: "记录", url: "repairlog.html" },
#            { name: "人员", url: "user_list2.html" }]
#    },
#    { "id": "17", "name": "技工", modules: [
#       { name: "案件", url: "coord.html" }, 
#       { name: "记录", url: "repairlog.html" }] },
#    { "id": "18", "name": "博客超级帐号", modules: []},
#    { "id": "19", "name": "公众", modules: [
#       { name: "文章列表", url: "coord.html" },  
#       { name: "用户文章", url: "repairlog.html" }] },文章中支持图片功能 
#       { name: "消息", url: "repairlog.html" }] },
#    ]},
#];

