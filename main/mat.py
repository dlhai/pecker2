#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

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

    return query5("rdmatins",mfields=select(base.sl).where(base.c.table=="matin"),mdata = sqlmatin,
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

    return query5("rdmatouts",mfields=select(base.sl).where(base.c.table=="matoutview"),mdata = sqlmatout,
                 rfields=select(base.sl).where(base.c.table=="matoutrecview"),rdata = sqlmatoutrec,)

#读取库存列表(已被/mat/store代替，二者除接口外完全相同)
#测试链接 http://127.0.0.1:5000/rdstore?matwh_id=?
@app.route("/rdstore")
def rdstore():
    param = request.args.to_dict()
    if "matwh_id" not in param:
        return '{result:404,msg:"缺少参数 matwh_id"}'
    sql='''select * from mat left join ( select mat_id, sum(num) as allin, sum(outnum) as allout from store_view 
        where matwh_id={0} group by mat_id ) as store on mat.id = store.mat_id order by mat_id '''
    return query5("rdstore",fields=select(base.sl).where(base.c.table=="mat"),data = sql.format(param["matwh_id"]))



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
    return query5("rdstoredetail",fields=select(base.sl).where(base.c.table=="inrecview"),\
        inrecs = inrecs.format(user.depart_id,param["mat_id"]),outrecs = outrecs.format(user.depart_id,param["mat_id"]))


#/mat/provcreate
@app.route("/mat/matprovcreate",methods=['POST'])
@login_required
def matprovcreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="mat/matprovcreate")

    if "name" not in form or form["name"]=="":
        return toret(r,msg="name不正确")

    conn.execute(toinsert("matprov",form))
    r.data = QueryObj("select * from matprov where id in (select max(id) from matprov)")
    return toret(r,result=200)

#/mat/provmodify?id=
@app.route("/mat/matprovmodify",methods=['POST'])
@login_required
def matprovmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="mat/matprovmodify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "name" not in form or form["name"]=="":
        return toret(r,msg="name不正确")

    id=params["id"]
    conn.execute(toupdate("matprov", form, obj(id=id)))
    r.data = QueryObj("select * from matprov where id=%s"%id)
    return toret(r,result=200)

#/mat/provremove?id=
@app.route("/mat/matprovremove")
@login_required
def matprovremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/mat/matprovremove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("matwh",obj(matprov_id=params["id"])) > 0:
        return toret(r,msg="省区不为空，不能删除")

    id = params["id"]
    conn.execute(todelete("matprov", obj(id=id)))
    return toret(r,result=200)


#/mat/whcreate
@app.route("/mat/matwhcreate",methods=['POST'])
@login_required
def matwhcreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="mat/matwhcreate")

    if "name" not in form or form["name"]=="":
        return toret(r,msg="name不正确")

    conn.execute(toinsert("matwh",form))
    r.data = QueryObj("select * from matwh where id in (select max(id) from matwh)")
    return toret(r,result=200)

#/mat/whmodify?id=
@app.route("/mat/matwhmodify",methods=['POST'])
@login_required
def matwhmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="mat/matwhmodify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "name" not in form or form["name"]=="":
        return toret(r,msg="name不正确")

    id=params["id"]
    conn.execute(toupdate("matwh", form, obj(id=id)))
    r.data = QueryObj("select * from matwh where id=%s"%id)
    return toret(r,result=200)

#/mat/whremove?id=
@app.route("/mat/matwhremove")
@login_required
def matwhremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/mat/matwhremove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("matin",obj(matwh_id=params["id"])) > 0:
        return toret(r,msg="已产生入库，不能删除")
    if querycount("matout",obj(matwh_id=params["id"])) > 0:
        return toret(r,msg="已产生出库，不能删除")

    id = params["id"]
    conn.execute(todelete("matwh", obj(id=id)))
    return toret(r,result=200)

#/mat/create
@app.route("/mat/create",methods=['POST'])
@login_required
def matcreate():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="mat/create")

    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    conn.execute(toinsert("mat",form))
    r.data = QueryObj("select * from mat where id in (select max(id) from mat)")
    return toret(r,result=200)

#/mat/modify?id=
@app.route("/mat/modify",methods=['POST'])
@login_required
def matmodify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="mat/modify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")
    if "name" not in form or form["name"]=="":
        return toret(r,msg="name不正确")

    id=params["id"]
    conn.execute(toupdate("mat", form, obj(id=id)))
    r.data = QueryObj("select * from mat where id=%s"%id)
    return toret(r,result=200)

#/mat/remove?id=
@app.route("/mat/remove")
@login_required
def matremove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/mat/remove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("matinrec",obj(mat_id=params["id"])) > 0:
        return toret(r,msg="已产生入库，不能删除")

    id = params["id"]
    conn.execute(todelete("mat", obj(id=id)))
    return toret(r,result=200)

#查询某材料的库存情况（新建、编辑出库记录时用作参考）
#/mat/store?matwh_id=&mat_id=&matoutrec_id=
#matoutrec_id参数是要忽略的出库记录，在出库单编辑时，当前行占用的数量也应计算为可用数量，不应统计为占用数量
#r.mat_recs 入库记录清单（由于sqlite不能处理null数据，需要在外部对确定）
#r.mat_num_in #入库总数量，仅包含已完成的
#r.mat_num_out #出库总数量，退回状态除外，但包含未完成的
@app.route("/mat/storeavailable")
@login_required
def matstoreavailable():
    params = request.args.to_dict()
    r = obj(result="404",fun="/mat/remove")
    if "mat_id" not in params or params["mat_id"]=="":
        return toret(r,msg="code不正确")
    if "matwh_id" not in params or params["matwh_id"]=="":
        return toret(r,msg="name不正确")

    matoutrec_id ="" if "matoutrec_id" not in params or params["matoutrec_id"]=="" else "and matoutrec.id!="+ params["matoutrec_id"]
    sql_recs='''
        SELECT *
          FROM (
                   SELECT matinrec.*,matin.source as matin_source, matin.code as matin_code
                     FROM matinrec,
                          matin
                    WHERE matinrec.matin_id = matin.id AND 
                          matin.status = 3 and matin.matwh_id={matwh_id} and matinrec.mat_id={mat_id}
               )
               AS inrec
               LEFT JOIN
               (
                   SELECT matinrec_id,
                          sum(num) AS outnum
                     FROM matoutrec,
                          matout
                    WHERE matoutrec.matout_id = matout.id AND 
                          matout.status != -1 {matoutrec_id}
                    GROUP BY matinrec_id
               )
               AS outrec ON inrec.id = outrec.matinrec_id;'''.format(matwh_id=params["matwh_id"], mat_id=params["mat_id"], matoutrec_id=matoutrec_id)

    sql_in='''select sum(num) as mat_num_in from matin,matinrec where matin.id = matinrec.matin_id 
            and matin.status=3 and mat_id={mat_id} and matin.matwh_id={matwh_id}'''.format(matwh_id=params["matwh_id"], mat_id=params["mat_id"])
    sql_out='''select sum(matoutrec.num) as mat_num_out from matoutrec,matout, matinrec 
        where matout.id = matoutrec.matout_id and matinrec_id = matinrec.id 
        and matout.status!=-1 and mat_id={mat_id} and matout.matwh_id={matwh_id} {matoutrec_id}
        '''.format(matwh_id=params["matwh_id"], mat_id=params["mat_id"],matoutrec_id=matoutrec_id)

    r.mat_recs = QueryObj(sql_recs)
    r.mat_recs = list(filter(lambda x: x.num > atoi(x.outnum), r.mat_recs) )
    r.mat_num_in = QueryObj(sql_in)[0].mat_num_in 
    r.mat_num_out = QueryObj(sql_out)[0].mat_num_out 
    return toret(r,result=200)

#读取库存列表
#测试链接 http://127.0.0.1:5000/mat/store?matwh_id=?
@app.route("/mat/store")
def matstore():
    param = request.args.to_dict()
    if "matwh_id" not in param:
        return '{result:404,msg:"缺少参数 matwh_id"}'
    sql='''select * from mat left join ( select mat_id, sum(num) as allin, sum(outnum) as allout from store_view 
        where matwh_id={0} group by mat_id ) as store on mat.id = store.mat_id order by mat_id '''.format(param["matwh_id"])
    return query5("matstore",fields=select(base.sl).where(base.c.table=="mat"),data = sql)

#读取库存明细
#测试链接 http://127.0.0.1:5000/mat/storedetail?mat_id=?
@app.route("/mat/storedetail")
def matstoredetail():
    param = request.args.to_dict()
    if "mat_id" not in param:
        return '{result:404,msg:"缺少参数 mat_id"}'

    #查询入库记录的、查询出库记录的
    inrecs='''select matinrec.*, matin.code,matin.source, flow.date as creater_dt, flow.user_id as creater_id 
              from matinrec,matin,flow 
              where matinrec.matin_id=matin.id and matin.status >=3
                and matinrec.matin_id=flow.record_id and flow.table_id=26 and flow.status=0
                and matin.matwh_id={0} and mat_id={1} order by id'''.format(current_user.depart_id,param["mat_id"])

    outrecs='''select matoutrec.*, matout.code,matout.usage, matout.recver,matout.status, flow.date as creater_dt, flow.user_id as creater_id
                from matoutrec,matinrec,matout,flow 
                where matoutrec.matout_id=matout.id and matout.status >=5
                    and matoutrec.matinrec_id=matinrec.id
                    and matoutrec.matout_id=flow.record_id and flow.table_id=28 and flow.status=0 
                    and matout.matwh_id={0} and mat_id={1} order by id'''.format(current_user.depart_id,param["mat_id"])
    return query5("storedetail",fields=select(base.sl).where(base.c.table=="inrecview"),inrecs = inrecs,outrecs = outrecs)
