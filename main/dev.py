#encoding:utf-8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

def insertflow(**kw):
    u = obj(table_id=22,user_id=current_user.id,date=datetime.datetime.now())
    for k,v in kw.items():
        setattr( u, k, v)
    insert("flow",u)

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
    files = request.files.to_dict()
    r = obj(result="404",fun="dev/devcreate")

    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")
    if "clss" not in form or form["clss"]=="":
        return toret(r,msg="clss不正确")

    id = QueryObj("select max(id) as max from dev")[0].max+1
    fmt = "./uploads/dev_{fd}/dev_{id}{ext}"
    for k,v in files.items():
        if k in ["face","img"]:
            fname = fmt.format(id=id, fd=k, ext=os.path.splitext(v.filename)[1] )
            v.save("./static/"+fname)
            form[k]=fname

    conn.execute(toinsert("dev",form))
    r.data = QueryObj("select * from dev where id="+str(id))
    return toret(r,result=200)

#/dev/devmodify?id=
@app.route("/dev/devmodify",methods=['POST'])
@login_required
def devmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    files = request.files.to_dict()
    r = obj(result="404",fun="dev/devmodify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "code" in form and form["code"]=="":
        return toret(r,msg="code不正确")
    if "clss" in form and form["clss"]=="":
        return toret(r,msg="clss不正确")

    fmt = "./uploads/dev_{fd}/dev_{id}{ext}"
    for k,v in files.items():
        if k in ["face","img"]:
            fname = fmt.format(id=u.id, fd=k, ext=os.path.splitext(v.filename)[1] )
            v.save("./static/"+fname)
            form[k]=fname

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

    id = params["id"]
    if querycount("devwork",obj(dev_id=id)) > 0:
        return toret(r,msg="已产生设备调用，不能删除")

    conn.execute(todelete("dev", obj(id=id)))
    return toret(r,result=200)


#/dev/devworkcreate
@app.route("/dev/devworkcreate",methods=['POST'])
@login_required
def devworkcreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="devwork/devworkcreate")

    if "fault_id" not in form or form["fault_id"]=="":
        return toret(r,msg="fault_id不正确")
    if "guide_id" not in form or form["guide_id"]=="":
        return toret(r,msg="guide_id不正确")
    if "winder_id" not in form or form["winder_id"]=="":
        return toret(r,msg="winder_id不正确")
    if "clss" not in form or form["clss"]=="":
        return toret(r,msg="clss不正确")
    del form["winder_addr"]
    form["status"]=0
    form["timelen"]=atoi(form["timelen"])

    conn.execute(toinsert("devwork",form))
    r.data = QueryObj("select * from devwork where id in (select max(id) from devwork)")[0]
    insertflow(record_id=r.data.id,status=0,remark="创建调用单")
    return toret(r,result=200)

#/dev/devworkmodify?id=
@app.route("/dev/devworkmodify",methods=['POST'])
@login_required
def devworkmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="devwork/devworkmodify")

    if "fault_id" not in form or form["fault_id"]=="":
        return toret(r,msg="fault_id不正确")
    if "guide_id" not in form or form["guide_id"]=="":
        return toret(r,msg="guide_id不正确")
    if "winder_id" not in form or form["winder_id"]=="":
        return toret(r,msg="winder_id不正确")
    if "clss" not in form or form["clss"]=="":
        return toret(r,msg="clss不正确")

    del form["winder_addr"]
    form["timelen"]=atoi(form["timelen"])

    id=params["id"]
    conn.execute(toupdate("devwork", form, obj(id=id)))
    insertflow(record_id=id,remark="修改调用单")
    r.data = QueryObj("select * from devwork where id=%s"%id)
    return toret(r,result=200)

#/dev/devworkremove?id=
@app.route("/dev/devworkremove")
@login_required
def devworkremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/dev/devworkremove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    id = params["id"]
    conn.execute(todelete("devwork", obj(id=id)))
    conn.execute(todelete("flow", obj(table_id=22,record_id=id)))
    return toret(r,result=200)

#读取任务单列表
@app.route("/dev/devworkquery")
@login_required
def devworkquery():
    params = request.args.to_dict()
    r = obj(result="404",fun="/dev/devworkquery")

    sql = '''select devwork.*, dev.code as dev_code, user.name as driver_name, winder.name as winder_name, winder.addr as winder_addr, fault.code as fault_code 
            from winder, fault,devwork left join dev on dev_id=dev.id left join user on devwork.driver_id=user.id
            where fault.id=fault_id and devwork.winder_id=winder.id '''
    if "fault_id" in params: #根据案件查
        if params["fault_id"]=="":
            return toret(r,msg="fault_id不正确")
        sql+=" and fault_id="+params["fault_id"]
    elif "devwh_id" in params:#根据驻地查
        if params["devwh_id"]=="":
            return toret(r,msg="devwh_id不正确")
        sql+=" and devwork.devwh_id="+params["devwh_id"]+" and devwork.status>0"
    elif "driver_id" in params:#根据司机查
        if params["driver_id"]=="":
            return toret(r,msg="driver_id不正确")
        sql+=" and devwork.driver_id="+params["driver_id"]+" and devwork.status>0"
    else:
        return toret(r,msg="缺少必须的参数")
    sql+=" order by devwork.status,devwork.id desc"

    r.data= QueryObj(sql)
    r.maxid = atoi(QueryObj("select max(id) as maxid from flow where table_id=22 and record_id in ("+",".join([str(x.id) for x in r.data])+")")[0].maxid)
    if "maxid" in params and atoi(r.maxid) == atoi(params["maxid"]):
        r.data=[]
        return toret(r,result=200, msg="没有新数据")

    r.fields=QueryObj(select(base.sl).where(base.c.table=="devwork"))
    return toret(r,result=200)

#读取任务单详细信息
@app.route("/dev/devworkdetail")
@login_required
def devworkdetail():
    params = request.args.to_dict()
    r = obj(result="404",fun="/dev/devworkdetail")
    if "id" not in params or params["id"]=="":
        return toret(r,msg="缺少参数id")
    id=params["id"]
    r.devwork= QueryObj("select * from devwork where id="+id)
    if (len(r.devwork)==0):
        return toret(r,msg="id不正确")

    r.devwork=r.devwork[0]
    r.flows= QueryObj("select * from flow where table_id=22 and record_id="+id+" order by id desc")
    r.winder= QueryObj("select * from winder where id="+str(r.devwork.winder_id))[0]
    r.fault= QueryObj("select * from fault where id="+str(r.devwork.fault_id))[0]
    userids = [x.user_id for x in r.flows ]
    if r.devwork.driver_id != "":
        userids.append(r.devwork.driver_id)
    if r.devwork.dev_id != "":
        r.dev= QueryObj("select * from dev where id="+str(r.devwork.dev_id))[0]
    r.users= QueryObj("select id,name,face,profile,sex,job,depart_id from user where id in ("+ ",".join([str(x) for x in userids]) +")")
    r.maxid=r.flows[0].id
    return toret(r,result=200)



#/matout/chgstatus?id=
@app.route("/dev/devworkchgstatus",methods=['POST'])
@login_required
def devworkchgstatus():
    form =request.form.to_dict()
    r = obj(result="404",fun="/dev/devworkchgstatus")
    if "id" not in form or form["id"]=="":
        return toret(r,msg="缺少参数id")
    if "status" not in form or form["status"]=="":
        return toret(r,msg="缺少参数status")
    if "maxid" not in form or form["maxid"]=="":
        return toret(r,msg="缺少参数maxid")

    maxid = atoi(QueryObj("select max(id) as maxid from flow where table_id=22 and record_id="+form["id"])[0].maxid)
    if maxid != atoi(form["maxid"]):
        return toret(r,result="405",msg="调用单已变更")
    u = QueryObj("select * from devwork where id="+ form["id"])
    if (len(u) == 0 ):
        return toret(r,msg="id不存在")
    u=u[0]


    '''{{ "id": "",  "name": "新建" },
    { "id": "0", "bid":"", "name":"未提交" },
    { "id": "1", "bid":"0","name":"已提交" },
    { "id": "2", "bid":"1","name":"前往现场" },
    { "id": "3", "bid":"2","name":"到达现场" },
    { "id": "4", "bid":"3","name":"任务完成" },
    { "id": "-1","bid":"1","name":"退回" },}'''

    tab={"提交":{"oldstatus":"0","newstatus":"1","remark":"提交调用单"},
         "撤回":{"oldstatus":"1","newstatus":"0","remark":"撤回调用单"},
         "接单":{"oldstatus":"1","newstatus":"2","remark":"审批调用单"},
         "退回":{"oldstatus":"1","newstatus":"-1","remark":"退回调用单"},
         "确认到达":{"oldstatus":"2","newstatus":"3","remark":"确认到达现场"},
         "任务结束":{"oldstatus":"3","newstatus":"4","remark":"确认任务完成"}}
    if form["action"] not in tab:
        return toret(r,msg="不认识的操作类型")
    action = tab[form["action"]]
    newdata=obj(status=action["newstatus"])
    if u.status != int(action["oldstatus"]) or (newdata.status=="1" and u.status != -1 ):
        return toret(r,result="405",msg="调用单不合要求")

    if form["action"] == "提交":
        if u.clss =="":
            return toret(r,msg="未指定设备分类")
        if u.devwh_id =="":
            return toret(r,msg="未指定设备驻地")
    if form["action"] == "接单":
        if "dev_id" not in form or form["dev_id"]=="":
            return toret(r,msg="缺少参数dev_id")
        if "driver_id" not in form or form["driver_id"]=="":
            return toret(r,msg="缺少参数driver_id")
        newdata.dev_id=form["dev_id"]
        newdata.driver_id=form["driver_id"]
        newdata.deal_id=current_user.id
        newdata.dealdt=datetime.datetime.now()
        conn.execute(toupdate( "dev", obj(driver_id=form["driver_id"]), obj(id=form["dev_id"])))

    conn.execute(toupdate( "devwork", newdata, obj(id=form["id"])))
    insertflow(record_id=form["id"],status=action["newstatus"],remark=action["remark"])
    return toret(r,result=200)
