from flask import Flask,request, Response, jsonify
from flask_login import login_required,current_user
import json
from main2 import app,login_manager,check
from main.model import *

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
        if "id" not in params:
            return toret(obj(result=404,msg="缺少参数 id"))

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

