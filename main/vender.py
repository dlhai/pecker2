#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

#/vender/create
@app.route("/vender/create",methods=['POST'])
@login_required
def vendercreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="vender/create")
    if "type" not in params:
        return toret(r,msg="缺少参数type")
    if params["type"] not in ["17","18","21","25"]:
        return toret(r,msg="type不正确")

    for x in ["name","atten","tel"]:
        if x not in form or form[x]=="":
            return toret(r,msg="缺少参数"+x)

    form["type"] = params["type"]
    conn.execute(toinsert("vender",form))
    return toret(r,result=200)

#/vender/modify?id=
@app.route("/vender/modify",methods=['POST'])
@login_required
def vendermodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="/vender/modify")
    if "id" not in params:
        return toret(r,msg="缺少参数id")
    for x in ["name","atten","tel"]:
        if x not in form or form[x]=="":
            return toret(r,msg="缺少参数"+x)
    conn.execute(toupdate("vender", form, obj(id=params["id"])))
    return toret(r,result=200)

#/vender/remove?id=
@app.route("/vender/remove")
@login_required
def venderremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/vender/remove")
    if "id" not in params:
        r.msg = "缺少参数 id"
        return tojson(r)
    u = QueryObj("select * from vender where id="+params["id"])
    if len(u) == 0:
        return toret(r,msg="id不存在")

    lnktbl=gettbl(u[0].type)["name"]
    if lnktbl != "mat":
        if querycount( gettbl(u[0].type)["name"],obj(vender_id=params["id"]))>0:
            return toret(r,msg="已经使用")
    else:
        if querycount( "matinrec",obj(vender_id=params["id"]))>0:
            return toret(r,msg="已经使用")

    conn.execute(todelete("vender", obj(id=params["id"])))
    return toret(r,result=200)
