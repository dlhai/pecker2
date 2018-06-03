#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

#删除用户
#/user/remove?id=
@app.route("/user/remove")
@login_required
def userremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="user/remove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    user = QueryObj("select * from user where id=%s"%params["id"])
    if len(user)==0:
        return toret(r,msg="id不存在")
    if user.depart_id != 0:
        return toret(r,msg="所属单位不为空")
    
    #仅清除用户关注和粉丝（避免在他人用户好友列表中出现），其他如发表文章和参与事物不做处理
    conn.execute(todelete("follow",obj(idols=user.id)))
    conn.execute(todelete("follow",obj(fans=user.id)))
    conn.execute(toupdate("user",obj(status=-1),obj(id=user.id)))
    return toret(r,result=200)


#用户摘要，用来显示头像标签等
#/user/brief?id=
@app.route("/user/brief")
@login_required
def userbrief():
    params = request.args.to_dict()
    r = obj(result="404",fun="userbrief")
    if "id" not in params:
        r.msg = "缺少参数 id"
        return tojson(r)

    r.user = QueryObj("select id,name,face,profile,sex,job,depart_id from user where id=%s"%params["id"])
    if len(r.user)==0:
        r.msg = "id不存在"
        return tojson(r)
    r.user = r.user[0]
    r.user.prof = getjob(r.user.job)["sname"]
    verifyface(r.user)

    r.result=200
    return tojson(r)

#申请转换职业
#Reqdata("/user/reqjob?newjob="+jobid )
@app.route("/user/reqjob")
@login_required
def reqjob():
    params = request.args.to_dict()
    r = obj(result="404",fun="reqjob")
    if "newjob" not in params:
        r.msg = "缺少参数 newjob"
        return tojson(r)
    newjob=params["newjob"]

    rec = obj()
    rec.type = 5 #1changejob
    rec.src = current_user.id
    rec.dst = getjob(newjob)["su"]
    if rec.dst =="":
        r.msg = "newjob不是有效值"
        return tojson(r)
    rec.jsn="{'newjob':'%s'}"%newjob
    rec.say = ""
    rec.whn = datetime.datetime.now()

    conn.execute(toinsert("msg",rec))
    return Response(tojson(obj(result="200",fun="reqjob")), mimetype='application/json')

