#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

def additinsert(tbl,field, id, files):
    addits = []
    idx = 0
    now = datetime.datetime.now()
    fmt = "uploads/{tbl}_{field}/{tbl}{id}_{field}{idx}{ext}"
    for k,v in files.items(): 
        name = fmt.format(tbl=tbl,field=field,id=id, idx=idx, ext=os.path.splitext(v.filename)[1] )
        addits.append(obj(type="{tbl}_{field}".format(tbl=tbl,field=field),ref_id=id,name=name,user_id=current_user.id, date=now))
        v.save("./static/"+name)
        idx += 1
    if len(addits)>0:
        conn.execute(toinsert("addit",addits))

def additupdate(tbl,field, id, files):
    addits = []
    now = datetime.datetime.now()
    fmt = "uploads/{tbl}_{field}/{tbl}{id}_{field}{idx}{ext}"
    imgs = QueryObj("select * from addit where type='{tbl}_{field}' and ref_id={id}".format(tbl=tbl,id=id, field=field))
    for k,v in files.items(): 
        idx = k.split("_")[1]
        name = fmt.format(tbl=tbl,id=id, field=field,idx=idx, ext=os.path.splitext(v.filename)[1] )
        if int(idx) >= len(imgs):
            addits.append(obj(type="{tbl}_{field}".format(tbl=tbl,field=field),ref_id=id,name=name,user_id=current_user.id, date=now))
        v.save("./static/"+name)
    if len(addits)>0:
        conn.execute(toinsert("addit",addits))

def additremove(tbl,field,id):
    imgs = QueryObj("select * from addit where type='{tbl}_{field}' and ref_id={id}".format(tbl=tbl,id=id, field=field))
    conn.execute(todelete("addit",obj(type="{tbl}_{field}".format(tbl=tbl,field=field), ref_id=id)))
    for x in imgs:
        try:
            os.remove('./static/'+x.name)
        except FileNotFoundError:
            pass

#/case/createfault
@app.route("/case/faultcreate",methods=['POST'])
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
    [form.pop(k) for k in list(form.keys()) if k.startswith("image_") ]
    form["status"]=0 # 状态默认为0

    u = insertq("fault",form)[0]
    conn.execute(toinsert("link",[obj( x, a_id=u.id) for x in devices]))
    insert("flow",obj(table_id=19,record_id=u.id,status=0,user_id=current_user.id,date=now, remark="创建报修单"))
    additinsert("fault", "image", u.id, files);

    return toret(r,result=200)

#/case/faultmodify?id=
@app.route("/case/faultmodify",methods=['POST'])
@login_required
def faultmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    files = request.files.to_dict()
    r = obj(result="404",fun="fault/faultmodify")

    if "id" not in params or params["id"]=="":
        return toret(r,msg="缺少参数id")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    [form.pop(k) for k in list(form.keys()) if k.startswith("image_") ]
    del form["devices"]
    now = datetime.datetime.now()

    id=params["id"]
    conn.execute(toupdate("fault", form, obj(id=id)))
    additupdate("fault", "image", id, files)
    insert("flow",obj(table_id=19,record_id=id,status=0,user_id=current_user.id,date=now, remark="修改报修单"))

    return toret(r,result=200)

#/case/faultremove?id=
@app.route("/case/faultremove")
@login_required
def faultremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/case/faultremove")
    if "id" not in params or params["id"] == "":
        return toret(r,msg="缺少参数id")

    id=params["id"]
    fault=QueryObj('''select * from fault where id='''+id)
    if len(fault) == 0:
        return toret(r,msg="id不存在")
    fault = fault[0]
    if fault.status >= 2:
        return toret(r,msg="报修单已受理，不能删除！")

    conn.execute("delete from fault where id="+id)
    conn.execute("delete from link where (type='faultefan' or type='faultefan' or type='faultleaf') and a_id="+id)
    conn.execute("delete from flow where table_id=19 and record_id="+id)
    additremove("fault", "image",id )
    return toret(r,result=200)

@app.route("/case/rdfault")
def rdfault():
    r = obj(result="404",fun="/case/rdfault")
    params = request.args.to_dict()
    sql='''select fault.*,user.name as report_name, winder.name as winder_name 
           from fault,winder,user 
           where fault.report_id=user.id and fault.winder_id=winder.id and fault.status<5 '''

    if current_user.job == 2 or current_user.job == 3:# 2风场长、3驻场：本风场所有
        sql += " and winder_id="+str(current_user.depart_id)
    elif current_user.job == 11:# 11调度长：取所有已提交
        sql += " and fault.status>=1"
    elif current_user.job == 12:# 12调度：取自己的接单的 + 聊天含自己的
        sql += ''' and fault.status>=1 and ( fault.guide_id='''+str(current_user.id)+''' or fault.id in (select a_id from link where type="chatman" and b_id='''+str(current_user.id)+"))"
    elif current_user.job == 14:# 14专家：取专家列表中含自己、聊天含自己的
        sql += ''' and fault.status>=2 and fault.id in (select a_id from link where (type="chatman" or type="f_experts") and b_id='''+str(current_user.id)+")"
    elif current_user.job == 16 or current_user.job == 17:# 16队长、17技工：取施工队中含自己、聊天含自己的
        sql += ''' and fault.status>=2 and fault.id in (select a_id from link where (type="chatman" or type="f_team") and b_id='''+str(current_user.id)+")"
    sql += " order by fault.status,reporttime desc" # 越接近处理完成，排序越靠后

    r.data=QueryObj(sql)
    r.maxid = atoi(QueryObj("select max(id) as maxid from flow where table_id=19 and record_id in("+",".join([str(x.id) for x in r.data])+")")[0].maxid)
    if "maxid" in params:
        if r.maxid == atoi(params["maxid"]):
            r.data=[]
            return toret(r,result=200,msg="没有新数据")
    r.fields=QueryObj(select(base.sl).where(base.c.table=="fault"))
    r.ls="fault"
    r.result=200
    return Response(tojson(r), mimetype='application/json')

#/case/detail
@app.route("/case/detail")
@login_required
def casedetail():
    r = obj(result="404",fun="/case/detail")
    params = request.args.to_dict()
    if "id" not in params or params["id"]=="":
        return toret(r,msg="案件不能为空")

    id = params["id"]
    r.fault=QueryObj('''select fault.*,user.name as report_name, winder.name as winder_name 
           from fault,winder,user 
           where fault.report_id=user.id and fault.winder_id=winder.id and fault.id='''+id);
    if len(r.fault)==0:
        return toret(r,msg="案件ID不正确")
    r.fault=r.fault[0]
    r.maxid = atoi(QueryObj("select max(id) as maxid from flow where table_id=19 and record_id="+id)[0].maxid)
    r.fault.efans = QueryObj("select * from efan where id in( select b_id from link where type='faultefan' and a_id="+id+")")
    r.fault.leafs = QueryObj("select * from leaf where id in( select b_id from link where type='faultleaf' and a_id="+id+")")
    r.fault.imgs = QueryObj("select * from addit where type='fault_image' and ref_id="+id)
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

    #组件聊天数据
    sql = "select id,name,face,profile,sex,job,depart_id from user where"
    sql += " (depart_table=15 and depart_id="+str(r.fault.winder_id)+")" #风场所有人
    sql += " or job=11" #11调度长
    if r.fault.guide_id != "": #接单调度
        sql += " or id="+str(r.fault.guide_id)
    sql += " or id in ( select b_id from link where type='chatman' and a_id="+id+")" #聊天列表
    r.chatmen = QueryObj(sql)+r.experts+r.engineers
    r.speechlist= QueryObj("select * from chat where fault_id="+id)

    return toret(r,result=200)

#/case/chgstatus?id=
@app.route("/case/chgstatus",methods=['POST'])
@login_required
def casechgstatus():
    form =request.form.to_dict()
    r = obj(result="404",fun="/case/chgstatus")
    if "id" not in form or form["id"]=="":
        return toret(r,msg="缺少参数id")
    if "status" not in form or form["status"]=="":
        return toret(r,msg="缺少参数status")
    if "maxid" not in form or form["maxid"]=="":
        return toret(r,msg="缺少参数maxid")
    
    maxid = atoi(QueryObj("select max(id) as maxid from flow where table_id=19 and record_id="+form["id"])[0].maxid)
    if maxid != atoi(form["maxid"]):
        return toret(r,result="405",msg="报修单状态已变更")

    #更新matout状态，并产生flow记录
    def chgstatus( status, form, remark ):
        conn.execute(toupdate( "fault", obj(status=status), obj(id=form["id"])))
        now = datetime.datetime.now()
        conn.execute(toinsert("flow",obj(table_id=19,record_id=form["id"],status=status,user_id=current_user.id,date=now, remark=remark+" "+form["note"])))

    rs = QueryObj("select * from fault where id="+ form["id"])
    if (len(rs) == 0 ): 
        return toret(r,msg="id不存在")
    if form["action"] == "btn_submit": #0未提交 -1退回
        if rs[0].status != 0 and rs[0].status != -1:
            return toret(r,msg="报修单状态已变更")
        chgstatus( 1, form, "提交")
    elif form["action"] == "btn_recall": #1已提交 
        if rs[0].status != 1:
            return toret(r,msg="报修单状态已变更")
        chgstatus( 0, form, "撤回")
    elif form["action"] == "btn_accept":#2已受理(正在评估) 
        if rs[0].status != 1:
            return toret(r,msg="报修单状态已变更")
        chgstatus( 2, form, "受理")
    elif form["action"] == "btn_decline":
        if rs[0].status != 1:
            return toret(r,msg="报修单状态已变更")
        chgstatus( -1, form, "退回")
    #3正在维修（维修方案完成）
    #...
    #4即将完成(开始编写维修报告) 
    #...
    elif form["action"] == "btn_finish":#5完工(维修报告完成) 
        if rs[0].status != 2:
            return toret(r,msg="报修单状态已变更")
        chgstatus( 5, form, "完工")
    #6提醒付款
    #...
    elif form["action"] == "btn_frozen": #7冻结 
        if rs[0].status != 5:
            return toret(r,msg="报修单状态已变更")
        chgstatus( 7, form, "冻结")
    else:
        return toret(r,msg="不认识的操作类型")
    return toret(r,result=200)

def addchat(fault_id, users):
    chatmen= QueryObj("select b_id from link where type='chatman' and a_id="+id)
    chatmen=[x.b_id for x in chatmen]
    users=[x for x in users if x not in chatmen]
    insert("link",[obj(type='chatman', a_id=id,b_id=x,date=now) for x in team ])


@app.route("/case/setexpert",methods=['POST'])
@login_required
def casesetexpert():
    form =request.form.to_dict()
    r = obj(result="404",fun="/case/setexpert")
    if "id" not in form or form["id"]=="":
        return toret(r,msg="缺少参数id")
    if "expert" not in form or form["expert"]=="":
        return toret(r,msg="缺少参数expert")

    experts = form["expert"].split(",")
    now = datetime.datetime.now()
    id=form["id"]
    conn.execute("delete from link where type='f_experts' and a_id="+id)
    insert("link",[obj(type="f_experts", a_id=id,b_id=x,date=now) for x in experts ])
    insert("flow",obj(table_id=19,record_id=id,user_id=current_user.id,date=now, remark="更新案件专家列表"))
    return toret(r,result=200)

@app.route("/case/setteam",methods=['POST'])
@login_required
def casesetteam():
    form =request.form.to_dict()
    r = obj(result="404",fun="/case/setexpert")
    if "id" not in form or form["id"]=="":
        return toret(r,msg="缺少参数id")
    if "leader" not in form or form["leader"]=="":
        return toret(r,msg="缺少参数leader")

    team = [form["leader"]]
    if "engineers" in form:
        team+=form["engineers"].split(",")
    now = datetime.datetime.now()
    id=form["id"]
    conn.execute("delete from link where type='f_team' and a_id="+id)
    insert("link",[obj(type="f_team", a_id=id,b_id=x,date=now) for x in team ])
    insert("flow",obj(table_id=19,record_id=id,user_id=current_user.id,date=now, remark="更新施工队列表"))
    return toret(r,result=200)
