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
from main.mat import *
from main.matin import *
from main.matout import *
from main.case import *

class CLog:
    def write(data):
        print(data)
    def writelines(data):
        print(data)
    def flush():
        pass

if __name__ == "__main__":
    ar = ["","user_face","user_idimg","certif_image", "employ_image", "edu_image1", "edu_image2", 
          "fault_image","dev_face","dev_img", "matin_image", "matout_image"]
    newdir(["./static/uploads/"+x for x in ar])
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
#    主框架√
#       首页
#       全局搜索
#       消息√
#       个人信息√
#       单位信息
#       切换用户√
#    { "id": "18", "name": "博客超级帐号", modules: []},
#    { "id": "19", "name": "公众", modules: [
#       { name: "文章列表", url: "coord.html" },  
#       { name: "用户文章", url: "repairlog.html" }] },文章中支持图片功能 
#       { name: "消息", url: "repairlog.html" }] },
#    ]},
#var db_roles = [
#    {
#        "id": "1", "type": "winder", "name": "叶片超级帐号", modules: [
#            { name: "地图", url: "windersumap.html" },√
#            { name: "风场", url: "windersu.html" },√
#            { name: "人员", url: "user_list2.html" },√ 改变职业、改变所在单位、从公众添加、新建用户、不同角色显示字段不同、
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
#            { name: "地图", url: "devmap.html" },√
#            { name: "驻地", url: "devsu.html" },√
#            { name: "人员", url: "user_list2.html" },√
#            { name: "厂家", url: "devvender.html" }]√
#    },
#    {
#        "id": "5", "type": "dev", "name": "驻地主管", modules: [
#            { name: "地图", url: "devmap.html" },√
#            { name: "驻地", url: "devwh.html" },√
#            { name: "人员", url: "user_list2.html" }]√
#    },
#    {
#        "id": "6", "type": "dev", "name": "设备司机", modules: [
#            { name: "设备", url: "devdriver.html" }]√
#    },
#    {
#        "id": "7", "type": "wh", "name": "仓库超级帐号", modules: [
#            { name: "地图", url: "matmap.html" },√
#            { name: "仓库", url: "matsu.html" },√
#            { name: "人员", url: "user_list2.html" },√
#            { name: "材料", url: "material.html" }]√
#    },
#    {
#        "id": "8", "type": "wh", "name": "仓库主管", modules: [
#            { name: "地图", url: "matmap.html" },√ 
#            { name: "入库", url: "matin.html" },√ 单据附图片还未实现
#            { name: "出库", url: "matout.html" },√ 1.从消息接受发货（来自案件）， 2.单据附图片还未实现 3.状态变更时，需要通知到调度,4.单据长时间不处理，自动设置为退回（例如出库单不退回则会占用库存）
#            { name: "查询", subs: [
#               { name: "库存", url: "matquery.html" }, √ 1.出入库单状态暂未考虑
#               { name: "入库", url: "matqueryin.html" }, √ 1.入库单状态暂未考虑
#               { name: "出库", url: "matqueryout.html" }]},√ 1.出库单状态暂未考虑
#            { name: "人员", url: "user_list2.html" }]
#    },
#    {
#        "id": "9", "type": "wh", "name": "仓库管理员", modules: [
#            { name: "地图", url: "matmap.html" },√
#            { name: "入库", url: "matin.html" },√
#            { name: "出库", url: "matout.html" },√
#            { name: "查询", subs: [
#               { name: "库存", url: "matquery.html" }, √
#               { name: "入库", url: "matqueryin.html" },√
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
#];

#chglog:
#2018/6/25
#1.main2.py:首行utf8 改为utf-8，utf8好似系统不认。在某些情况下，可能引起导入的库函数不能被识别，例如sqlalchemy的create_engine
#2.cube.css的x4Tree少点错误，问题现象：在coorddlg弹出树时，宽度不能随内容扩展问题
#3.修改list_writings.html、view_user.html显示brief
#4.在发表文章处，增加brief输入框
#5.发表文章成功时，刷新当前页面(即：location.reload())
#6.修正blog.js多处提示框"xx成功"未加result="200"判断
#7.在db.xlsx中，摘要生成改为choice(data("_songci").data)，这是为了避免采用rnditem:_songci长度被截断，再次生成数据时，需要验证是否有效。