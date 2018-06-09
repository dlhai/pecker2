#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

def check(ls,form):
    if ls == "winderprov":
        if "winderco_id" not in form or form["winderco_id"]=="":
            return False,"winderco_id不正确"
    elif ls == "winder":
        if "winderprov_id" not in form or form["winderprov_id"]=="":
            return False,"winderprov_id不正确"
        if "winderco_id" not in form or form["winderco_id"]=="":
            return False,"winderco_id不正确"
    elif ls == "winderarea":
        if "winder_id" not in form or form["winder_id"]=="":
            return False,"winder_id不正确"
    return True,"";

#/winder/create?ls=
@app.route("/winder/create",methods=['POST'])
@login_required
def windercreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="winder/create")
    if "ls" not in params:
        return toret(r,msg="缺少参数ls")
    if params["ls"] not in ["winderco","winderprov","winder","winderarea"]:
        return toret(r,msg="ls不正确")
    #.....
    result,msg = check(params["ls"],form)
    if not result:
        return toret(r,msg=msg)
    r.ls = params["ls"]
    conn.execute(toinsert(r.ls,form))
    r.data = QueryObj("select * from {ls} where id in (select max(id) from {ls})".format(ls=r.ls))

    return toret(r,result=200)

#/winder/modify?ls=&id=
@app.route("/winder/modify",methods=['POST'])
@login_required
def windermodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="/winder/modify")
    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "ls" not in params:
        return toret(r,msg="缺少参数ls")
    if params["ls"] not in ["winderco","winderprov","winder","winderarea"]:
        return toret(r,msg="ls不正确")

    result,msg = check(params["ls"],form)
    if not result:
        return toret(r,msg=msg)
    
    r.ls = params["ls"]
    conn.execute(toupdate(params["ls"], form, obj(id=params["id"])))
    r.data = QueryObj("select * from {ls} where id in (select max(id) from {ls})".format(ls=r.ls))

    return toret(r,result=200)

#/winder/remove?ls=&id=
@app.route("/winder/remove")
@login_required
def winderremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/winder/remove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "ls" not in params:
        return toret(r,msg="缺少参数ls")
    if params["ls"] not in ["winderco","winderprov","winder","winderarea"]:
        return toret(r,msg="ls不正确")
    if params["ls"] == "winderco" and querycount("winderprov", obj(winderco_id=params["id"]))>0:
        return toret(r,msg="下级省区不空")
    if params["ls"] == "winderprov" and querycount("winder", obj(winderprov_id=params["id"]))>0:
        return toret(r,msg="下级风场不空")
    if params["ls"] == "winder":
        if querycount("efan", obj(winder_id=params["id"]))>0:
            return toret(r,msg="下级风电机不空")
        if querycount("user", obj(depart_id=params["id"],depart_table=15))>0:
            return toret(r,msg="风场人员不空")

    conn.execute(todelete(params["ls"], obj(id=params["id"])))
    return toret(r,result=200)

#/winder/efancreate
@app.route("/winder/efancreate",methods=['POST'])
@login_required
def efancreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="winder/efancreate")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    efan = obj()
    leafs = [obj(),obj(),obj()]
    for k,v in form.items():
        if k[0] == "0": setattr( leafs[0], k[1:], v)
        elif k[0] == "1": setattr( leafs[1], k[1:], v)
        elif k[0] == "2": setattr( leafs[2], k[1:], v)
        else:setattr( efan, k, v)
    conn.execute(toinsert("efan",efan))
    id = QueryObj("select max(id) as max from efan")[0].max
    [setattr(x,"efan_id", id) for x in leafs ]
    conn.execute(toinsert("leaf",leafs))

    r.data = QueryObj("select * from efan where id in (select max(id) from efan)")
    r.data[0].leafs = QueryObj("select * from leaf where efan_id=%d"%r.data[0].id)
    return toret(r,result=200)

#/winder/efanmodify?id=
@app.route("/winder/efanmodify",methods=['POST'])
@login_required
def efanmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="winder/efancreate")
    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    efan = obj()
    leafs = [obj(),obj(),obj()]
    for k,v in form.items():
        if k[0] == "0": setattr( leafs[0], k[1:], v)
        elif k[0] == "1": setattr( leafs[1], k[1:], v)
        elif k[0] == "2": setattr( leafs[2], k[1:], v)
        else:setattr( efan, k, v)
    
    id=params["id"]
    conn.execute(toupdate("efan", efan, obj(id=id)))
    [conn.execute(toupdate("leaf", leaf, obj(id=leaf.id))) for leaf in leafs]

    r.data = QueryObj("select * from efan where id =%s"%id)
    r.data[0].leafs = QueryObj("select * from leaf where efan_id=%s"%id)
    return toret(r,result=200)

#/winder/efanremove?id=
@app.route("/winder/efanremove")
@login_required
def efanremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/winder/efanremove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("link",obj(type="faultefan",id=params["id"])) > 0:
        return toret(r,msg="已产生案件，不能删除")
    for x in QueryObj( "select id from leaf where winder_id="+params["id"]):
        if querycount("link",obj(type="faultleaf",b_id=x.id)) > 0:
            return toret(r,msg="已产生案件，不能删除")
    id = params["id"]
    conn.execute(todelete("efan", obj(id=id)))
    conn.execute(todelete("leaf", obj(efan_id=id)))
    return toret(r,result=200)
