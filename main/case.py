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
    form["status"]=0

    u = insertq("fault",form)[0]
    insert("link",obj(type="chatman", a_id=u.id,b_id=current_user.id)) #将自己加入到聊天列表中
    if current_user.job == 3: #将风场长加入到聊天列表中
        mgr=QueryObj("select id from user where job=2 and depart_id="+str(current_user.depart_id))[0]
        insert("link",obj(type="chatman", a_id=u.id,b_id=mgr.id)) 
    conn.execute(toinsert("link",[obj( x, a_id=u.id) for x in devices]))
    #insert("msg",obj(type=6,src=current_user.id,dst=1000,table_id=19,row_id=u.id))

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

# 驻场：取参与聊天成员包含自己的未完成的案件列表
# 风场长：取本风场所有未完成的案件列表
# 调度：取参与聊天成员包含自己的未完成的案件列表
# 调度长：取所有未完成的案件列表
# 专家：取参与聊天成员包含自己的未完成的案件列表
# 队长：取参与聊天成员包含自己的未完成的案件列表
# 技工：取参与聊天成员包含自己的未完成的案件列表
# 为了统一起见，使所有人都“取参与聊天成员包含自己的未完成的案件列表”，做如下设定：
#   1.驻场创建后就自动添加自己和风场长在列表中
#   2.调度在接收案件时，自动添加自己和调度长在列表中
# 这样做还有以下好处：
#   1.驻场可以邀请其他驻场进入列表协助工作
#   2.调度可以邀请其他调度进入列表协助工作
# 也就是避免了对创建的驻场和接收的调度产生完全的依赖。
@app.route("/case/rdfault")
def rdfault():
    r = obj(result="404",fun="/case/rdfault")
    params = request.args.to_dict()
    sql='''select fault.*,user.name as report_name, winder.name as winder_name 
           from fault,winder,user 
           where fault.report_id=user.id and fault.winder_id=winder.id and fault.status<5 
           and (fault.id in (select a_id from link where type="chatman" and b_id='''+str(current_user.id)+")"
    if current_user.job == 11 or current_user.job == 11:#调度长和调度可以看到已提交的
        sql += " or fault.status=1"
    sql += ") order by fault.status,reporttime desc" # 越接近处理完成，排序越靠后
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
    r.fault_imgs = QueryObj("select * from addit where type='fault_image' and ref_id="+id)
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