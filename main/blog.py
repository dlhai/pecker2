#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

@app.route('/blog/<bdir>/<bfile>')
def bfile(bdir,bfile):
    return app.send_static_file(bdir+"/"+bfile)
@app.route('/blog/<bdir1>/<bdir2>/<bfile>')
def bfile2(bdir1,bdir2,bfile):
    return app.send_static_file(bdir1+"/"+bdir2+"/"+bfile)
@app.route('/blog/<bdir1>/<bdir2>/<bdir3>/<bfile>')
def bfile3(bdir1,bdir2,bdir3,bfile):
    return app.send_static_file(bdir1+"/"+bdir2+"/"+bdir3+"/"+bfile)
@app.route('/blog/<bdir1>/<bdir2>/<bdir3>/<bdir4>/<bfile>')
def bfile4(bdir1,bdir2,bdir3,bdir4,bfile):
    return app.send_static_file(bdir1+"/"+bdir2+"/"+bdir3+"/"+bdir4+"/"+bfile)

#各博客页面
@app.route('/blog/<ls>')
def blog(ls):
    param = request.args.to_dict()
    ar = {"news":"1", "writings":"2", "docs":"3" }
    if ls not in ar:
        return 404
    pos=0
    if "pos" in param:
        pos=atoi(param["pos"])
    writtings=QueryObj("select writing.*,user.face, user.name from writing,user where writing.user_id==user.id and board=%s order by date desc limit %d,10"%(ar[ls],pos))
    pgn=pagnition("/blog/%s"%ls+"?pos=%d",pos,"select count(*) as count from writing where board=%s"%ar[ls],10)
    return render_template("list_writings.html",writtings=writtings,pgn=pgn)

@app.route('/blog/view_writing')
def view_writing():
    param = request.args.to_dict()
    if "id" not in param:
        return '{result:404,msg:"缺少参数 ls"}'
    pos=0
    if "pos" in param:
        pos=atoi(param["pos"])
    writting=QueryObj("select * from writing where writing.id=%s"%param["id"])[0]
    user = QueryObj("select * from user where id=%s"%writting.user_id)[0]
    recents=QueryObj("select id,title from writing where writing.user_id=%s order by date desc limit 0,30"%writting.user_id)
    replays=QueryObj("select writing.*,user.face, user.name from writing,user where writing.user_id==user.id and writing.writing_id=%s order by date desc limit %d,20"%(param["id"],pos))
    pgn=pagnition("/blog/view_writing?id=%s"%param["id"]+"&pos=%d",pos,"select count(*) as count from writing where writing.writing_id=%s"%param["id"])
    return render_template("view_writing.html",user=user,recents=recents,writting=writting, replays=replays, pgn=pgn)

@app.route('/blog/view_user')
def view_user():
    param = request.args.to_dict()
    if "id" not in param:
        return '{result:404,msg:"缺少参数 ls"}'
    pos=0
    if "pos" in param:
        pos=atoi(param["pos"])
    user = QueryObj("select * from user where id=%s"%param["id"])[0]
    writtings=QueryObj("select * from writing where user_id=%s order by date desc limit 0,10"%param["id"])
    pgn=pagnition("/blog/view_writing?id=%s"%param["id"]+"&pos=%d",pos,"select count(*) as count from writing where writing.user_id=%s"%param["id"],10)
    return render_template("view_user.html",user=user,writtings=writtings,pgn=pgn)

#发表文章、评论/回复、发消息
@app.route("/publish")
@login_required
def publish():
    ret = QueryObj( "select * from user where id="+str(current_user.id))
    if len(ret) <= 0:
        return '{"roleuser":"'+param['account']+'","result":404}\n'
    user = ret[0]
    del user.pwd

    #鎵惧埌鐢ㄦ埛鐨勬墍鍦ㄥ崟浣嶏紝鑻ユ墍鍦ㄥ崟浣嶆槸椋庡満锛屽垯闇��璇诲彇椋庡尯鍒楄〃
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

#鎺ㄨ崘銆佸叧娉�
@app.route('/recom', methods=['POST'])
@login_required
def recom():
    jsn = json.loads(request.data)
    ret=obj(fun="chgpwd", result="200")
    if current_user.id != int(jsn["id"]):
        ret.result = "1002"
        ret.msg = "浣犱笉鑳戒慨鏀瑰埆浜虹殑瀵嗙爜"
    if current_user.pwd != jsn["pwd"]:
        ret.result = "1002"
        ret.msg = "鏃у瘑鐮佷笉姝ｇ‘"
    if ret.result == "200":
        sql = "update user set pwd='{0}' where id={1}".format(jsn["newpwd"], jsn["id"])
        conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')
 
