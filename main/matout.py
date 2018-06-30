#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

#新建出库单列表
@app.route("/matout/create",methods=['POST'])
@login_required
def matoutcreate():
    form =request.form.to_dict()
    files = request.files.to_dict()
    r = obj(result="404",fun="matout/create")

    if "code" not in form or form["code"]=="":
        return toret(r,msg="缺少参数code")

    [form.pop(k) for k in list(form.keys()) if k.startswith("img_") ] #去掉空的图片
    now = datetime.datetime.now()
    u=insert("matout",form)[0]
    conn.execute(toinsert("flow",obj(table_id=28,record_id=u.id,status=u.status,user_id=current_user.id,date=now, remark="创建出库单")))

    # 1. 保存附件
    addits = []
    idx = 0
    fmt = "./uploads/matout_image/matout_{id}_{idx}{ext}"
    for k,v in files.items(): 
        fname = fmt.format(id=u.id, idx=idx, ext=os.path.splitext(v.filename)[1] )
        addits.append(obj(type="matout_img",ref_id=u.id,name=fname,user_id=current_user.id, date=now))
        v.save("./static/"+fname)
        idx += 1
    if len(addits)>0:
        conn.execute(toinsert("addit",addits))
    r.data = [u]
    return toret(r,result=200)


#/matout/modify?id=
@app.route("/matout/modify",methods=['POST'])
@login_required
def matoutmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="matout/modify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    id=params["id"]
    [form.pop(k) for k in list(form.keys()) if k.startswith("img_") ] #去掉空的图片
    conn.execute(toupdate("matout", form, obj(id=id)))
    r.data = QueryObj("select * from matout where id=%s"%id)
    return toret(r,result=200)

#/matout/remove?id=
@app.route("/matout/remove")
@login_required
def matoutremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/matout/remove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    id = params["id"]
    conn.execute(todelete("matout", obj(id=id)))
    conn.execute(todelete("matoutrec", obj(matout_id=id)))
    conn.execute(todelete("flow", obj(table_id=28,record_id=id)))
    return toret(r,result=200)


#/matout/reccreate
@app.route("/matout/reccreate",methods=['POST'])
@login_required
def matoutreccreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="matout/reccreate")

    if "matout_id" not in params or params["matout_id"]=="":
        return toret(r,msg="matout_id不能为空")
    if "matinrec_id" not in form or form["matinrec_id"]=="":
        return toret(r,msg="材料不能为空")
    if "num" not in form or form["num"]=="" or form["num"]=="0":
        return toret(r,msg="数量不能为空")

    num_in = QueryObj("SELECT num FROM matinrec where id="+form["matinrec_id"])[0].num
    num_out = QueryObj("SELECT sum(num) as num FROM matoutrec where matinrec_id="+form["matinrec_id"])[0].num
    if atoi(form["num"])+atoi(num_out) > num_in:
        return toret(r,msg="出库数量不能大于可用数量")

    #del form["code"]
    #del form["type"]
    #del form["unit"]
    form["matout_id"]=params["matout_id"]
    r.data = insert("matoutrec",form)
    return toret(r,result=200)

#/matout/recmodify?id=
@app.route("/matout/recmodify",methods=['POST'])
@login_required
def matoutrecmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="matout/recmodify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "matinrec_id" not in form or form["matinrec_id"]=="":
        return toret(r,msg="材料不能为空")
    if "num" not in form or form["num"]=="" or form["num"]=="0":
        return toret(r,msg="数量不能为空")

    id=params["id"]
    num_in = QueryObj("SELECT num FROM matinrec where id="+form["matinrec_id"])[0].num
    num_out = QueryObj("SELECT sum(num) as num FROM matoutrec where id!={0} and matinrec_id={1}".format( id,form["matinrec_id"]))[0].num
    if atoi(form["num"])+atoi(num_out) > num_in:
        return toret(r,msg="出库数量不能大于可用数量")

    #del form["code"]
    #del form["type"]
    #del form["unit"]
    conn.execute(toupdate("matoutrec", form, obj(id=id)))
    r.data = QueryObj("select * from matoutrec where id=%s"%id)
    return toret(r,result=200)

#/matout/recremove?id=
@app.route("/matout/recremove")
@login_required
def matoutrecremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/matout/recremove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    id = params["id"]
    conn.execute(todelete("matoutrec", obj(id=id)))

    return toret(r,result=200)


#读取用户的未完成出库单列表
@app.route("/matout/cards")
@login_required
def matoutcards():
    r = obj(result="404",fun="/matout/cards")
    #未完成的出库单且关联备货人的列（注意不是创建人）
    matout = '''
            select matout.*,
                creater.user_id as creater_id, 
                creater.date as creater_dt, 
                stocker.user_id as stocker_id 
            from matout 
                left join flow as creater on (matout.id=creater.record_id and creater.table_id=28 and creater.status=0) 
                left join flow as stocker on (matout.id=stocker.record_id and stocker.table_id=28 and stocker.status=2)
            where matout.status <6 '''
    inrec = '''
            select matoutrec.*, matinrec.mat_id 
            from matoutrec, matout, matinrec,flow as stocker
            where matout.status <6
                and matout_id=matout.id
                and matout_id=stocker.record_id and stocker.table_id=28 and stocker.status=2
                and matinrec_id=matinrec.id '''
    #0编辑(正在签收) 1等待审批 2等待入库 3完成 -1退回
    if current_user.job==8: #仓库主管(查询所在仓库所有未完成的出库单)
        matout += "and matout.matwh_id=%d"%current_user.depart_id
        inrec += "and matout.matwh_id=%d"%current_user.depart_id
    elif current_user.job==9: #仓库管理员(查询创建者为自己，且未完成的出库单)
        matout += "and stocker.user_id=%d"%current_user.id
        inrec += "and stocker.user_id=%d"%current_user.id
    else:
        return toret( r, msg="用户职业不对！")
    r.matouts= QueryObj(matout)
    recs= QueryObj(inrec)
    for x in r.matouts:
        x.subs=[ y for y in recs if y.matout_id == x.id]
    r.mfields = QueryObj(select(base.sl).where(base.c.table=="matout"))
    r.sfields = QueryObj(select(base.sl).where(base.c.table=="matoutrec"))
    return toret(r,result=200)

#读取出库单记录详细信息
@app.route("/matout/recdetail")
@login_required
def matoutrecdetail():
    params = request.args.to_dict()
    r = obj(result="404",fun="/matout/recdetail")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    r.data= QueryObj('''
                    select matoutrec.*,matinrec.mat_id, 
                        matinrec.specs as in_specs, 
                        matinrec.vender_id as in_vender_id,
                        matinrec.producedt as in_producedt,
                        matinrec.expiredt as in_expiredt,
                        matinrec.remark as in_remark 
                    from matoutrec,matinrec 
                    where matinrec_id=matinrec.id and matout_id='''+params["id"])
    return toret(r,result=200)

#更新matout状态，并产生flow记录
def chgmatout( status, form, remark ):
    conn.execute(toupdate( "matout", obj(status=status), obj(id=form["id"])))
    now = datetime.datetime.now()
    conn.execute(toinsert("flow",obj(table_id=28,record_id=form["id"],status=status,user_id=current_user.id,date=now, remark=remark+" "+form["note"])))

#/matout/chgstatus?id=
@app.route("/matout/chgstatus",methods=['POST'])
@login_required
def matoutchgstatus():
    form =request.form.to_dict()
    r = obj(result="404",fun="/matout/chgstatus")
    if "id" not in form or form["id"]=="":
        return toret(r,msg="缺少参数id")
    if "status" not in form or form["status"]=="":
        return toret(r,msg="缺少参数status")
    
    rs = QueryObj("select * from matout where id="+ form["id"])
    if (len(rs) == 0 ):
        return toret(r,msg="id不存在")
    if form["action"] == "submit":
        if rs[0].status != 0 and rs[0].status != -1:
            return toret(r,msg="出库单状态已变更")
        chgmatout( 1, form, "提交备货 ")
    elif form["action"] == "store":
        if rs[0].status != 1:
            return toret(r,msg="出库单状态已变更")
        chgmatout( 2, form, "开始备货 ")
    elif form["action"] == "storeT":
        if rs[0].status != 2:
            return toret(r,msg="出库单状态已变更")
        chgmatout( 3, form, "备货完成 ")
    elif form["action"] == "storeF":
        if rs[0].status != 2:
            return toret(r,msg="出库单状态已变更")
        chgmatout( -1, form, "备货不成功 ")
    elif form["action"] == "recall":
        if rs[0].status != 3:
            return toret(r,msg="出库单状态已变更")
        chgmatout( 2, form, "撤回 ")
    elif form["action"] == "checkT":
        if rs[0].status != 3:
            return toret(r,msg="出库单状态已变更")
        chgmatout( 4, form, "审批通过 ")
    elif form["action"] == "checkF":
        if rs[0].status != 3:
            return toret(r,msg="出库单状态已变更")
        chgmatout( -1, form, "审批不通过 ")
    elif form["action"] == "outwhT":
        if rs[0].status != 4:
            return toret(r,msg="出库单状态已变更")
        chgmatout( 5, form, "出库完成 ")
    elif form["action"] == "outwhT":
        if rs[0].status != 4:
            return toret(r,msg="出库单状态已变更")
        chgmatout( -1, form, "出库不成功 ")
    elif form["action"] == "confirm":
        if rs[0].status != 5:
            return toret(r,msg="出库单状态已变更")
        chgmatout( 6, form, "确认收货 ")
    else:
        return toret(r,msg="不认识的操作类型")
    return toret(r,result=200)
