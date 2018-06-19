#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

#读取用户的未完成入库单列表
@app.route("/matin/cards")
@login_required
def matincards():
    r = obj(result="404",fun="/matin/cards")
    matin = "select matin.*,flow.user_id from matin,flow where matin.status in (-1,0,1,2) and matin.id=flow.record_id and flow.table_id=26 and flow.status=0 "
    inrec = "select matinrec.* from matinrec, matin,flow where matin.status in (-1,0,1,2) and matin.id=flow.record_id and flow.table_id=26 and flow.status=0 and matin.id=matinrec.matin_id "
    #0编辑(正在签收) 1等待审批 2等待入库 3完成 -1退回
    if current_user.job==8: #仓库主管(查询所在仓库所有未完成的入库单)
        matin += "and matin.matwh_id=%d"%current_user.depart_id
        inrec += "and matin.matwh_id=%d"%current_user.depart_id
    elif current_user.job==9: #仓库管理员(查询创建者为自己，且未完成的入库单)
        matin += "and matin.matwh_id=%d"%current_user.id
        inrec += "and matin.matwh_id=%d"%current_user.id
    else:
        return toret( r, msg="用户职业不对！")
    r.matins= QueryObj(matin)
    recs= QueryObj(inrec)
    for x in r.matins:
        x.subs=[ y for y in recs if y.matin_id == x.id]
    r.mfields = QueryObj(select(base.sl).where(base.c.table=="matin"))
    r.sfields = QueryObj(select(base.sl).where(base.c.table=="matinrec"))
    return toret(r,result=200)


#新建入库单列表
@app.route("/matin/create",methods=['POST'])
@login_required
def matincreate():
    form =request.form.to_dict()
    files = request.files.to_dict()
    r = obj(result="404",fun="matin/create")

    if "code" not in form or form["code"]=="":
        return toret(r,msg="缺少参数code")

    [form.pop(k) for k in list(form.keys()) if k.startswith("img_") ] #去掉空的图片
    now = datetime.datetime.now()
    u=insert("matin",form)
    conn.execute(toinsert("flow",obj(table_id=26,record_id=u.id,status=u.status,user_id=current_user.id,date=now)))
  

    # 1. 保存附件
    addits = []
    idx = 0
    fmt = "./uploads/matin_image/matin_{id}_{idx}{ext}"
    for k,v in files.items(): 
        fname = fmt.format(id=u.id, idx=idx, ext=os.path.splitext(v.filename)[1] )
        addits.append(obj(type="matin_image",ref_id=u.id,name=fname,user_id=current_user.id, date=now))
        v.save("./static/"+fname)
        idx += 1
    if len(addits)>0:
        conn.execute(toinsert("addit",addits))
    r.data = [u]
    return toret(r,result=200)


#/matin/modify?id=
@app.route("/matin/modify",methods=['POST'])
@login_required
def matinmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="matin/modify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    id=params["id"]
    conn.execute(toupdate("matin", form, obj(id=id)))
    r.data = QueryObj("select * from matin where id=%s"%id)
    return toret(r,result=200)

#/matin/remove?id=
@app.route("/matin/remove")
@login_required
def matinremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/matin/remove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("xxx",obj(xxx="xxx",id=params["id"])) > 0:
        return toret(r,msg="已xxx，不能删除")

    id = params["id"]
    conn.execute(todelete("matin", obj(id=id)))
    return toret(r,result=200)




#/matin/reccreate
@app.route("/matin/reccreate",methods=['POST'])
@login_required
def matinreccreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="matin/reccreate")

    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    conn.execute(toinsert("matinrec",form))
    r.data = QueryObj("select * from matinrec where id in (select max(id) from matinrec)")
    return toret(r,result=200)

#/matin/recmodify?id=
@app.route("/matin/recmodify",methods=['POST'])
@login_required
def matinrecmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="matin/recmodify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    id=params["id"]
    conn.execute(toupdate("matinrec", form, obj(id=id)))
    r.data = QueryObj("select * from matinrec where id=%s"%id)
    return toret(r,result=200)

#/matin/recremove?id=
@app.route("/matin/recremove")
@login_required
def matinrecremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/matin/recremove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("xxx",obj(xxx="xxx",id=params["id"])) > 0:
        return toret(r,msg="已xxx，不能删除")

    id = params["id"]
    conn.execute(todelete("matinrec", obj(id=id)))
    return toret(r,result=200)

