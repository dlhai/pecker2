#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
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
    writings=QueryObj("select writing.*,user.face, user.name from writing,user where writing.user_id==user.id and board=%s order by date desc limit %d,10"%(ar[ls],pos))
    pgn=pagnition("/blog/%s"%ls+"?pos=%d",pos,"select count(*) as count from writing where board=%s"%ar[ls],10)
    return render_template("list_writings.html",writings=writings,pgn=pgn)

@app.route('/blog/view_writing')
def view_writing():
    param = request.args.to_dict()
    if "id" not in param:
        return '{result:404,msg:"缺少参数 ls"}'
    pos=0
    if "pos" in param:
        pos=atoi(param["pos"])
    writing=QueryObj("select * from writing where writing.id=%s"%param["id"])[0]
    user = QueryObj("select * from user where id=%s"%writing.user_id)[0]
    recents=QueryObj("select id,title from writing where writing.user_id=%s order by date desc limit 0,30"%writing.user_id)
    replays=QueryObj("select writing.*,user.face, user.name from writing,user where writing.user_id==user.id and writing.writing_id=%s order by date desc limit %d,20"%(param["id"],pos))
    pgn=pagnition("/blog/view_writing?id=%s"%param["id"]+"&pos=%d",pos,"select count(*) as count from writing where writing.writing_id=%s"%param["id"])
    return render_template("view_writing.html",user=user,recents=recents,writing=writing, replays=replays, pgn=pgn, me=current_user)

@app.route('/blog/view_user')
def view_user():
    param = request.args.to_dict()
    if "id" not in param:
        return '{result:404,msg:"缺少参数 ls"}'
    pos=0
    if "pos" in param:
        pos=atoi(param["pos"])
    user = QueryObj("select * from user where id=%s"%param["id"])[0]
    writings=QueryObj("select * from writing where user_id=%s order by date desc limit 0,10"%param["id"])
    pgn=pagnition("/blog/view_writing?id=%s"%param["id"]+"&pos=%d",pos,"select count(*) as count from writing where writing.user_id=%s"%param["id"],10)
    return render_template("view_user.html",user=user,writings=writings,pgn=pgn)

#关注某人
@app.route("/follow")
@login_required
def follow():
    param = request.args.to_dict()
    if "user_id" not in param:
        return '{result:404,msg:"缺少参数 user_id"}'

    sql = "insert into follow(fans_id,idol_id,date) values({0},{1},'{2}')".format(current_user.id, param["user_id"],datetime.datetime.now())
    conn.execute(sql)
    current_user.idols += [param["user_id"]]
    ret = obj(result="200",fun="follow")
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
 
