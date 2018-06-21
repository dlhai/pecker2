#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

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
    u=insert("matin",form)[0]
    conn.execute(toinsert("flow",obj(table_id=26,record_id=u.id,status=u.status,user_id=current_user.id,date=now, remark="创建入库单")))

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
    [form.pop(k) for k in list(form.keys()) if k.startswith("img_") ] #去掉空的图片
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

    id = params["id"]
    conn.execute(todelete("matin", obj(id=id)))
    conn.execute(todelete("matinrec", obj(matin_id=id)))
    conn.execute(todelete("flow", obj(table_id=26,record_id=id)))
    return toret(r,result=200)


#/matin/reccreate
@app.route("/matin/reccreate",methods=['POST'])
@login_required
def matinreccreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="matin/reccreate")

    if "matwh_id" not in params or params["matwh_id"]=="":
        return toret(r,msg="matwh_id不能为空")
    if "matin_id" not in params or params["matin_id"]=="":
        return toret(r,msg="matin_id不能为空")
    if "mat_id" not in form or form["mat_id"]=="":
        return toret(r,msg="材料不能为空")
    if "num" not in form or form["num"]=="" or form["num"]=="0":
        return toret(r,msg="数量不能为空")

    del form["code"]
    del form["type"]
    del form["unit"]
    form["matwh_id"]=params["matwh_id"]
    form["matin_id"]=params["matin_id"]
    r.data = insert("matinrec",form)
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
    if "mat_id" not in form or form["mat_id"]=="":
        return toret(r,msg="材料不能为空")
    if "num" not in form or form["num"]=="" or form["num"]=="0":
        return toret(r,msg="数量不能为空")

    del form["code"]
    del form["type"]
    del form["unit"]
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

    id = params["id"]
    conn.execute(todelete("matinrec", obj(id=id)))
    return toret(r,result=200)


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
        matin += "and flow.user_id=%d"%current_user.id
        inrec += "and flow.user_id=%d"%current_user.id
    else:
        return toret( r, msg="用户职业不对！")
    r.matins= QueryObj(matin)
    recs= QueryObj(inrec)
    for x in r.matins:
        x.subs=[ y for y in recs if y.matin_id == x.id]
    r.mfields = QueryObj(select(base.sl).where(base.c.table=="matin"))
    r.sfields = QueryObj(select(base.sl).where(base.c.table=="matinrec"))
    return toret(r,result=200)

#更新matin状态，并产生flow记录
def chgmatin( status, form, remark ):
    conn.execute(toupdate( "matin", obj(status=status), obj(id=form["id"])))
    now = datetime.datetime.now()
    conn.execute(toinsert("flow",obj(table_id=26,record_id=form["id"],status=status,user_id=current_user.id,date=now, remark=remark+" "+form["note"])))

#/matin/chgstatus?id=
@app.route("/matin/chgstatus",methods=['POST'])
@login_required
def matinchgstatus():
    form =request.form.to_dict()
    r = obj(result="404",fun="/matin/chgstatus")
    if "id" not in form or form["id"]=="":
        return toret(r,msg="缺少参数id")
    if "status" not in form or form["status"]=="":
        return toret(r,msg="缺少参数status")
    
    rs = QueryObj("select * from matin where id="+ form["id"])
    if (len(rs) == 0 ):
        return toret(r,msg="id不存在")
    if form["action"] == "submit":
        if rs[0].status != 0 and rs[0].status != -1:
            return toret(r,msg="入库单状态已变更")
        chgmatin( 1, form, "提交审批 ")
    elif form["action"] == "recall":
        if rs[0].status != 1:
            return toret(r,msg="入库单状态已变更")
        chgmatin( 0, form, "撤回 ")
    elif form["action"] == "checkT":
        if rs[0].status != 1:
            return toret(r,msg="入库单状态已变更")
        chgmatin( 2, form, "审批通过 ")
    elif form["action"] == "checkF":
        if rs[0].status != 1:
            return toret(r,msg="入库单状态已变更")
        chgmatin( -1, form, "审批不通过 ")
    elif form["action"] == "inwhT":
        if rs[0].status != 2:
            return toret(r,msg="入库单状态已变更")
        chgmatin( 3, form, "入库完成 ")
    elif form["action"] == "inwhF":
        if rs[0].status != 2:
            return toret(r,msg="入库单状态已变更")
        chgmatin( -1, form, "入库不成功 ")
    else:
        return toret(r,msg="不认识的操作类型")
    return toret(r,result=200)
