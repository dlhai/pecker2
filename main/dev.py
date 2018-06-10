#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

#/dev/devwhcreate
@app.route("/dev/devwhcreate",methods=['POST'])
@login_required
def devwhcreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="devwh/devwhcreate")

    if "name" not in form or form["name"]=="":
        return toret(r,msg="name不能为空")

    conn.execute(toinsert("devwh",form))
    r.data = QueryObj("select * from devwh where id in (select max(id) from devwh)")
    return toret(r,result=200)

#/dev/devwhmodify?id=
@app.route("/dev/devwhmodify",methods=['POST'])
@login_required
def devwhmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="devwh/devwhmodify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "name" not in form or form["name"]=="":
        return toret(r,msg="name不能为空")

    id=params["id"]
    conn.execute(toupdate("devwh", form, obj(id=id)))
    r.data = QueryObj("select * from devwh where id=%s"%id)
    return toret(r,result=200)

#/dev/devwhremove?id=
@app.route("/dev/devwhremove")
@login_required
def devwhremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/dev/devwhremove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("dev",obj(devwh_id=params["id"])) > 0:
        return toret(r,msg="驻地设备不为空，不能删除")

    id = params["id"]
    conn.execute(todelete("devwh", obj(id=id)))
    return toret(r,result=200)

#/dev/devcreate
@app.route("/dev/devcreate",methods=['POST'])
@login_required
def devcreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="dev/devcreate")

    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    conn.execute(toinsert("dev",form))
    r.data = QueryObj("select * from dev where id in (select max(id) from dev)")
    return toret(r,result=200)

#/dev/devmodify?id=
@app.route("/dev/devmodify",methods=['POST'])
@login_required
def devmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="dev/devmodify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    id=params["id"]
    conn.execute(toupdate("dev", form, obj(id=id)))
    r.data = QueryObj("select * from dev where id=%s"%id)
    return toret(r,result=200)

#/dev/devremove?id=
@app.route("/dev/devremove")
@login_required
def devremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/dev/devremove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("xxx",obj(xxx="xxx",id=params["id"])) > 0:
        return toret(r,msg="已xxx，不能删除")

    id = params["id"]
    conn.execute(todelete("dev", obj(id=id)))
    return toret(r,result=200)

