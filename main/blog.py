from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
from main2 import app,login_manager,check
from main.model import *
from main.tools import *


#各博客页面
@app.route('/blog/<ls>')
def blog(ls):
    ar = {"news":"1", "writtings":"2", "docs":"3" }
    if ls not in ar:
        return 404
    sql="select opus.*,user.face, user.name from opus,user where opus.user_id==user.id and board=%s"%(ar[ls])
    return render_template("blogbase.html",writtings=QueryObj(sql))

@app.route('/blog/<bdir>/<bfile>')
def bfile(bdir,bfile):
    return app.send_static_file(bdir+"/"+bfile)

@app.route('/blog/<bdir1>/<bdir2>/<bfile>')
def bfile2(bdir1,bdir2,bfile):
    return app.send_static_file(bdir1+"/"+bdir2+"/"+bfile)

@app.route('/blog/writting')
def writting(bdir,bfile):
    return app.send_static_file(bdir+"/"+bfile)

#发表文章、评论/回复、发消息
@app.route("/publish")
@login_required
def publish():
    ret = QueryObj( "select * from user where id="+str(current_user.id))
    if len(ret) <= 0:
        return '{"roleuser":"'+param['account']+'","result":404}\n'
    user = ret[0]
    del user.pwd

    #找到用户的所在单位，若所在单位是风场，则需要读取风区列表
    if atoi(user.depart_table) != 0: 
        tbl = gettbl(user.depart_table)
        user.depart = QueryObj( "select id, name from "+tbl["name"]+" where id="+str(user.depart_id))[0]
        if tbl["name"] == "winder":
            user.sub = QueryObj( "select id, name from winderarea where winder_id="+str(user.depart_id))
    ret=obj()
    ret.fun="curuserinf"
    ret.result = "200"
    ret.data = user
    ret.fields=QueryObj(select(base.sl).where(base.c.table=="user"))
    return Response(tojson(ret), mimetype='application/json')

#推荐、关注 
@app.route('/recom', methods=['POST'])
@login_required
def recom():
    jsn = json.loads(request.data)
    ret=obj(fun="chgpwd", result="200")
    if current_user.id != int(jsn["id"]):
        ret.result = "1002"
        ret.msg = "你不能修改别人的密码"
    if current_user.pwd != jsn["pwd"]:
        ret.result = "1002"
        ret.msg = "旧密码不正确"
    if ret.result == "200":
        sql = "update user set pwd='{0}' where id={1}".format(jsn["newpwd"], jsn["id"])
        conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')
 
