#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

#/case/createfault
@app.route("/case/createfault",methods=['POST'])
@login_required
def casecreatefault():
    params = request.args.to_dict()
    form =request.form.to_dict()
    files = request.files.to_dict()

    r = obj(result="404",fun="/case/createfault")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="缺少参数code")

    if "devices" not in form or form["devices"]=="":
        return toret(r,msg="报修设备不能为空")

    now = datetime.datetime.now()
    devices = [obj( type="faultefan",b_id=x,date=now) for x in form["devices"].split(",")]
    del form["devices"]
    [form.pop(k) for k in list(form.keys()) if k.startswith("img_") ]

    conn.execute(toinsert("fault",form))
    u = QueryObj("select * from fault where id in (select max(id) from fault)")[0]
    conn.execute(toinsert("link",[obj( x, a_id=u.id) for x in devices]))

    # 1. 保存附件
    addits = []
    idx = 0
    fmt = "./uploads/fault_image/fault_{id}_{idx}{ext}"
    for k,v in files.items(): 
        fname = fmt.format(id=u.id, idx=idx, ext=os.path.splitext(v.filename)[1] )
        addits.append(obj(type="fault_image",ref_id=u.id,name=fname,user_id=current_user.id, date=now))
        v.save("./static/"+fname)
        idx += 1
    if len(addits)>0:
        conn.execute(toinsert("addit",addits))
    return toret(r,result=200)

#/case/listexpert
@app.route("/case/listexpert")
@login_required
def listexpert():
    r = obj(result="404",fun="/case/listexpert")
    params = request.args.to_dict()
    if "fault_id" not in params or params["fault_id"]=="":
        return toret(r,msg="案件不能为空")

    r.users = QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ( select b_id from link where type='f_experts' and a_id="+params["fault_id"]+")")
    return toret(r,result=200)

#/case/listengneer
@app.route("/case/listengneer")
@login_required
def listengneer():
    r = obj(result="404",fun="/case/listengneer")
    params = request.args.to_dict()
    if "fault_id" not in params or params["fault_id"]=="":
        return toret(r,msg="案件不能为空")

    r.users = QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ( select b_id from link where type='f_team' and a_id="+params["fault_id"]+")")
    return toret(r,result=200)