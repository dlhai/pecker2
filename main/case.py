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

#/case/detail
@app.route("/case/detail")
@login_required
def casedetail():
    r = obj(result="404",fun="/case/detail")
    params = request.args.to_dict()
    if "id" not in params or params["id"]=="":
        return toret(r,msg="案件不能为空")

    id = params["id"]
    r.fault_imgs = QueryObj("select * from addit where type='fault_img' and ref_id="+id)
    r.experts = QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ( select b_id from link where type='f_experts' and a_id="+id+")")
    r.eval1rep = QueryObj("select * from addit where type='eval1rep' and ref_id="+id)
    r.eval2rep = QueryObj("select * from addit where type='eval2rep' and ref_id="+id)
    r.repairplan = QueryObj("select * from addit where type='repairplan' and ref_id="+id)
    if len(r.repairplan)>0:
        r.repairplan_sign = QueryObj("select * from link where type='sign' and a_id in("+",".join(map(lambda x:str(x.id),r.repairplan))+")")
        if len(r.repairplan_sign)>0:
            r.repairplan_signers = QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ("+",".join(map(lambda x:str(x.b_id),r.repairplan_sign))+")")
        else:
            r.repairplan_signers = []
    else:
        r.repairplan_sign = []
        r.repairplan_signers = []
    r.engineers = QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ( select b_id from link where type='f_team' and a_id="+id+")")

    r.matoutrecs = QueryObj('''
        select matoutrec.*, matinrec.mat_id, matout.matwh_id, matout.status
        from matoutrec, matout, matinrec
        where matoutrec.matout_id = matout.id and matoutrec.matinrec_id=matinrec.id 
        and matout.fault_id='''+id)
    r.devworks = QueryObj("select * from devwork where fault_id="+id)

    r.repairlog = QueryObj("select * from addit where type='repairlog' and ref_id="+id)
    if len(r.repairlog)>0:
        r.repairlog_imgs = QueryObj("select * from addit where type='repairpic' and ref_id in("+",".join(map(lambda x:str(x.id),r.repairlog))+")")
        r.repairlog_users = QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ("+",".join(map(lambda x:str(x.user_id),r.repairlog))+")")
    else:
        r.repairlog_imgs =[]
        r.repairlog_users = []

    r.repairrep = QueryObj("select * from addit where type='repairrep' and ref_id="+id)
    if len(r.repairrep)>0:
        r.repairrep_sign = QueryObj("select * from link where type='conform' and a_id in("+",".join(map(lambda x:str(x.id),r.repairrep))+")")
        if len(r.repairrep_sign)>0:
            r.repairrep_signers = QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ("+",".join(map(lambda x:str(x.b_id),r.repairrep_sign))+")")
        else:
            r.repairrep_sign = []
    else:
        r.repairrep_sign = []
        r.repairrep_signers = []

    r.chatmen= QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ( select b_id from link where type='chatman' and a_id="+id+")")
    r.speechlist= QueryObj("select * from chat where fault_id="+id)

    return toret(r,result=200)