from flask import Flask,request, Response, jsonify
from flask_login import login_required,current_user
from main2 import app,login_manager,check
from main.model import *

#frame用来填用户角色组合框
@app.route("/roleuserall")
def roleuserall():
    user = QueryObj( "select min(id) as id, account, name, job, depart_id, depart_table, face from user group by job")
    for u in [x for x in user if atoi(x.depart_table) != 0]:
        tbl = gettbl(u.depart_table)
        u.depart = QueryObj( "select * from "+tbl["name"]+" where id="+str(u.depart_id))[0]
        if tbl["name"] == "winder":
            u.sub = QueryObj( "select id, name from winderarea where winder_id="+str(u.depart_id))
    ret=obj()
    ret.fun="roleuserall"
    ret.result = "200"
    ret.data = user
    return Response(tojson(ret), mimetype='application/json')

#id到名字的转换
@app.route("/id2name")
def id2name():
    r = {}
    for k,v in request.args.to_dict().items():
        ar = k.split("_")
        qa = conn.execute( "select name from " + ar[0] + ' where id="' + v+'"').fetchall()
        r[k+"_"+v]=qa[0][0]
    return jsonify(r)

@app.route("/upload",methods=['POST'])
def upload():
    d1 =request.files.to_dict(); 
    d2 =request.form.to_dict(); 

    f = request.files["file"]
    f.save("./uploads/" + f.filename)
    return f.filename

#新建
#测试链接 http://127.0.0.1:5000/cr
@app.route("/cr", methods=['GET', 'POST'])
@login_required
def cr():
    ret=check(request, wt)
    if ret.result != "200":
        return Response(tojson(ret), mimetype='application/json')

    if request.content_type == 'application/json':
        js = json.loads(request.data)
        fields=",".join(map( lambda x: "'"+x+"'", js["val"].keys()))
        values=",".join(map( lambda x: "'"+x+"'", js["val"].values()))
        sql = "insert into {0}({1}) values({2})".format(js["ls"], fields,values)
        conn.execute(sql)
    else:
        params = request.args.to_dict()
        files = request.files.to_dict()
        dic =request.form.to_dict()

        # 1. 保存附件
        max = QueryObj("select max(id) as max from "+params["ls"])[0].max
        ret.id = max + 1 if max != "" else 1
        fmt = "./uploads/{ls}_{fd}/{ls}_{fd}_{id}{ext}"
        for k,v in files.items(): 
            fname = fmt.format(ls=params["ls"],fd=k, id=ret.id,ext=os.path.splitext(v.filename)[1] )
            dic[k]=fname
            v.save("./static/"+fname)

        # 2. 保存字段数据
        fields=",".join(map( lambda x: "'"+x+"'", dic.keys()))
        values=",".join(map( lambda x: "'"+x+"'", dic.values()))
        sql = "insert into {0}({1}) values({2})".format(params["ls"], fields,values)
        conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')

#新建
#测试链接 http://127.0.0.1:5000/rm
@app.route("/rm", methods=['GET', 'POST'])
@login_required
def rm():
    param = request.args.to_dict()
    if "ls" not in param:
        return '{result:404,msg:"缺少参数 ls"}'
    if "id" not in param:
        return '{result:404,msg:"缺少参数 id"}'
    ret=check(request, "rm")
    if ret.result != "200":
        return Response(tojson(ret), mimetype='application/json')

    sql = "delete from {0} where id='{1}'".format(param["ls"], param["id"])
    conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')

#更新，使用formdata时，url必须携带ls和id参数
#测试链接 http://127.0.0.1:5000/wt
@app.route("/wt", methods=['POST'])
@login_required
def wt():
    ret=check(request, wt)
    if ret.result != "200":
        return Response(tojson(ret), mimetype='application/json')

    if request.content_type == 'application/json':
        js = json.loads(request.data)
        fdv = ",\n".join([ k + "='"+ v+"'" for k,v in js["val"].items()] )
        sql = "update {0} set {1} where id={2}".format(js["ls"], fdv, js["id"])
        conn.execute(sql)
    else:
        params = request.args.to_dict()
        files = request.files.to_dict()
        fields =request.form.to_dict()
        # 1. 保存附件
        fmt = "./uploads/{ls}_{fd}/{ls}_{fd}_{id}{ext}"
        for k,v in files.items(): 
            fname = fmt.format(ls=params["ls"],fd=k, id=params["id"],ext=os.path.splitext(v.filename)[1] )
            fields[k]=fname
            v.save("./static/"+fname)
        # 2. 保存字段数据
        fdv = ",\n".join([ k + "='"+ v+"'" for k,v in fields.items()] )
        sql = "update {0} set {1} where id={2}".format(params["ls"], fdv, params["id"])
        conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')

#查询
#测试链接 http://127.0.0.1:5000/rd?ls=[表名]&key1=val1&key2=val2....
@app.route("/rd")
@login_required
def rd():
    d = request.args.to_dict()
    ls = d["ls"]
    del d["ls"]

    # 限制对部分表的查询
    if ls== "base" or ls == "user":
        return '{result:404,msg:"'+ls+''' isn't callable!"}'''

    if ls== "scale" or ls == "mainmat" or ls== "job" or ls== "skill" or ls=="ethnic":
        d["type"]=ls
        ls = "config"

    sql = "select * from "+ls
    if len(d) > 0:
        sql += " where "+" and ".join([ To(k,v) for k,v in d.items()])
    return query5(ls,fields=select(base.sl).where(base.c.table==ls),data = sql)

#查询用户
#测试链接 http://127.0.0.1:5000/rduser?type=winder&key1=val1&key2=val2....
@app.route("/rduser")
def rduser():
    param = request.args.to_dict()
    if ("depart_name" in param ):
        type = db_tbl[param["depart_name"]]
        sql = "select "+type+".name as depart_name, user.id,user.account,user.face,user.depart_id,"\
            +"user.job,user.skill,user.name,user.code,user.sex,user.ethnic,user.birth,user.origin,"\
            +"user.idimg,user.phone,user.qq,user.mail,user.wechat,user.addr from user,"+type\
            +" where user.depart_id = "+type+".id and user.depart_table='"+tbl["id"]+"' and "
    else:
        sql = "select user.id,user.account,user.face,user.depart_id,"\
            +"user.job,user.skill,user.name,user.code,user.sex,user.ethnic,user.birth,user.origin,"\
            +"user.idimg,user.phone,user.qq,user.mail,user.wechat,user.addr from user"\
            +" where "
    sql +=" and ".join([ To(k,v) for k,v in param.items()])
    return query4("queryuser",fields=select(base.sl).where(base.c.table=="user"),data = sql)

#读取用户的未完成入库单列表
#测试链接 http://127.0.0.1:5000/rdmatins?user_id=?
@app.route("/rdmatins")
def rdmatins():
    param = request.args.to_dict()
    if "user_id" not in param:
        return '{result:404,msg:"缺少参数 user_id"}'
    users=QueryObj("select * from user where id="+str(param["user_id"]))
    if len(users) !=1:
        return '{result:404,msg:"用户不存在"}'
    user=users[0]

    #0编辑(正在签收) 1等待审批 2等待入库 3完成 -1退回
    if user.job==8: #仓库主管(查询所在仓库所有未完成的入库单)
        sqlbase = "select %s from matin where status in (-1,0,1,2) and matwh_id=%d"
        sqlmatin=sqlbase%("*",user.depart_id)
        sqlmatinrec="select * from matinrec where matin_id in (%s)"%(sqlbase%("id",user.depart_id))
    elif user.job==9: #仓库管理员(查询创建者为自己，且未完成的入库单)
        sqlmatin='''select matin.* from matin,flow where matin.id=flow.record_id and flow.table_id=26 
            and matin.status in (-1,0,1,2) and flow.status=0 and flow.user_id='''+str(user.id);
        sqlmatinrec='''select inrecview.* from inrecview,flow where matin_id=flow.record_id and
            flow.table_id=26 and matin_status in (-1,0,1,2) and flow.status=0 and flow.user_id='''+str(user.id);
    else:
        return '{result:404,msg:"用户职业不对！"}'

    return query4("rdmatins",mfields=select(base.sl).where(base.c.table=="matin"),mdata = sqlmatin,
                 rfields=select(base.sl).where(base.c.table=="matinrec"),rdata = sqlmatinrec,)

#读取用户的未完成出库单列表
#测试链接 http://127.0.0.1:5000/rdmatouts?user_id=?
@app.route("/rdmatouts")
def rdmatouts():
    param = request.args.to_dict()
    if "user_id" not in param:
        return '{result:404,msg:"缺少参数 user_id"}'
    users=QueryObj("select * from user where id="+str(param["user_id"]))
    if len(users) !=1:
        return '{result:404,msg:"用户不存在"}'
    user=users[0]

    #0编辑(调度创建) 1调度提交等待备货 2库管正在备货或库管创建) 3库管提交等待审批 4主管审批通过等待出库 5出库(发货) 6确认收货(完成) -1退回
    if user.job==8: #仓库主管(查询所在仓库所有未完成的出库单)
        sqlmatout="select * from matoutview where status in (2,3,4,5) and matwh_id="+str(user.depart_id)
        sqlmatoutrec="select matoutrecview.* from matoutrecview where matout_status in (2,3,4,5) and matwh_id="+str(user.depart_id)
    elif user.job==9: #仓库管理员(查询备货者为自己，且未完成的出库单) 这个sql还可以再优化下
        sqlmatout="select * from matoutview where status in (2,3,4,5) and stocker_id="+str(user.id)
        sqlmatoutrec='''select matoutrecview.* from matoutrecview,matoutview where matoutrecview.matout_id = matoutview.id 
            and matoutview.status in (2,3,4,5) and matoutview.stocker_id='''+str(user.id)
    else:
        return '{result:404,msg:"用户职业不对！"}'

    return query4("rdmatouts",mfields=select(base.sl).where(base.c.table=="matoutview"),mdata = sqlmatout,
                 rfields=select(base.sl).where(base.c.table=="matoutrecview"),rdata = sqlmatoutrec,)

#读取库存列表
#测试链接 http://127.0.0.1:5000/rdstore?matwh_id=?
@app.route("/rdstore")
def rdstore():
    param = request.args.to_dict()
    if "matwh_id" not in param:
        return '{result:404,msg:"缺少参数 matwh_id"}'
    sql='''select * from mat left join ( select mat_id, sum(num) as allin, sum(outnum) as allout from store_view 
        where matwh_id={0} group by mat_id ) as store on mat.id = store.mat_id order by mat_id '''
    return query4("rdstore",fields=select(base.sl).where(base.c.table=="mat"),data = sql.format(param["matwh_id"]))

#读取库存明细
#测试链接 http://127.0.0.1:5000/rdstoredetail?mat_id=?
@app.route("/rdstoredetail")
def rdstoredetail():
    param = request.args.to_dict()
    if "mat_id" not in param:
        return '{result:404,msg:"缺少参数 mat_id"}'
    if "user_id" not in param:
        return '{result:404,msg:"缺少参数 user_id"}'
    users=QueryObj("select * from user where id="+str(param["user_id"]))
    if len(users) !=1:
        return '{result:404,msg:"用户不存在"}'
    user=users[0]

    #查询入库记录的、查询出库记录的
    inrecs='''select inrecview.*,flow.date as date from inrecview,flow where inrecview.matin_id=flow.record_id 
        and flow.table_id=26 and flow.status=3 and matin_status >=3 and matwh_id={0} and mat_id={1} order by id'''
    outrecs='''select outrecview.*,flow.date as date from outrecview,flow where outrecview.matout_id=flow.record_id 
        and flow.table_id = 28 and flow.status=5 and matout_status >=5 and matwh_id={0} and mat_id={1} order by id'''
    return query4("rdstoredetail",fields=select(base.sl).where(base.c.table=="inrecview"),\
        inrecs = inrecs.format(user.depart_id,param["mat_id"]),outrecs = outrecs.format(user.depart_id,param["mat_id"]))

#测试链接 http://127.0.0.1:5000/rdstoredetail?user_id=?
@app.route("/rdfault")
def rdfault():
    param = request.args.to_dict()
    if "guide_id" not in param:
        return '{result:404,msg:"缺少参数 guide_id"}'

    #查询入库记录的、查询出库记录的
    sql='''select fault.*,user.name as report_name, winder.name as winder_name from fault,winder,user 
        where fault.report_id= user.id and fault.winder_id=winder.id and guide_id='''+param["guide_id"]
    return query4("rdfault",fields=select(base.sl).where(base.c.table=="fault"), data = sql)

#读取队长所带的技工列表
#测试链接 http://127.0.0.1:5000/rdteam?user_id=
@app.route("/rdteam")
def rdteam():
    param = request.args.to_dict()
    if "user_id" not in param:
        return '{result:404,msg:"缺少参数 user_id"}'
    users=QueryObj("select * from user where id="+str(param["user_id"]))
    if len(users) !=1:
        return '{result:404,msg:"用户不存在"}'
    user=users[0]

    #查询入库记录的、查询出库记录的
    sql='''select * from user where id in ( select b_id from link where type ='team' and a_id = {0})'''
    return query4("rdteam",fields=select(base.sl).where(base.c.table=="user"),data = sql.format(user.id))