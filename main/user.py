#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

#申请转换职业
#/userbrief?id=
@app.route("/userbrief")
@login_required
def userbrief():
    param = request.args.to_dict()
    r = obj(result="404",fun="userbrief")
    if "id" not in param:
        r.msg = "缺少参数 id"
        return tojson(r)

    r.user = QueryObj("select id,name,face,profile,job from user where id=%s"%params["id"])
    if len(r.user)==0:
        r.msg = "id不存在"
        return tojson(r)
    r.user = r.user[0]
    r.user.jobname = getjob(r.user.job).sname
    return tojson(r)

#申请转换职业
#Reqdata("/reqjob?newjob="+jobid )
@app.route("/reqjob")
@login_required
def chgjob():
    param = request.args.to_dict()
    r = obj(result="404",fun="reqjob")
    if "newjob" not in param:
        r.msg = "缺少参数 newjob"
        return tojson(r)
    newjob=params["newjob"]

    rec = obj()
    rec.type = params["type"]
    rec.src = current_user.id
    rec.dst = getjob(newjob).su
    if rec.dst =="":
        r.msg = "newjob不是有效值"
        return tojson(r)
    rec.jsn="{newjob:%s}"%newjob
    rec.say = ""
    rec.whn = datetime.datetime.now()

    conn.execute(toinsert("msg",rec))
    return Response(tojson(obj(result="200",fun="reqjob")), mimetype='application/json')

