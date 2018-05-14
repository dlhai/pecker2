#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

def addup(user_id,writing_id):
    ret=obj()
    ret.read=QueryObj("select count(*) as count from footmark where writing_id="+str(writing_id))[0].count
    ret.replay=QueryObj("select count(*) as count from writing where writing_id="+str(writing_id))[0].count
    ret.praise=QueryObj("select count(*) as count from footmark where type=1 and writing_id="+str(writing_id))[0].count
    ret.blame=QueryObj("select count(*) as count from footmark where type=-1 and writing_id="+str(writing_id))[0].count
    r=QueryObj("select type from footmark where user_id={0} and writing_id={1}".format(user_id, writing_id))
    if len(r)>0:
        ret.me= r[0].type
    else:
        ret.me=None
    return ret

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

#各板块页面
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

#博文页面
@app.route('/blog/view_writing')
def view_writing():
    param = request.args.to_dict()
    if "id" not in param:
        return '{result:404,msg:"缺少参数 ls"}'
    pos=0
    if "pos" in param:
        pos=atoi(param["pos"])
    writing_id=param["id"]
    writing=QueryObj("select * from writing where writing.id=%s"%param["id"])[0]
    user = QueryObj("select * from user where id=%s"%writing.user_id)[0]
    recents=QueryObj("select id,title from writing where writing.user_id=%s order by date desc limit 0,30"%writing.user_id)
    replays=QueryObj("select writing.*,user.face, user.name from writing,user where writing.user_id==user.id and writing.writing_id=%s order by date desc limit %d,20"%(param["id"],pos))
    pgn=pagnition("/blog/view_writing?id=%s"%param["id"]+"&pos=%d",pos,"select count(*) as count from writing where writing.writing_id=%s"%param["id"])
    au=addup(current_user.id, writing_id)
    if au.me == None:
        sql = "insert into footmark(user_id,writing_id,type,date) values({0},{1},0,'{2}')".format(current_user.id, writing_id,datetime.datetime.now())
        conn.execute(sql)
    return render_template("view_writing.html",user=user,recents=recents,writing=writing, au=au,replays=replays, pgn=pgn, me=current_user)

#用户博文列表
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

#取消关注某人
@app.route("/leave")
@login_required
def leave():
    param = request.args.to_dict()
    if "user_id" not in param:
        return '{result:404,msg:"缺少参数 user_id"}'

    user_id=atoi(param["user_id"])
    sql = "delete from follow where fans_id={0} and idol_id={1}".format(current_user.id, user_id)
    conn.execute(sql)
    current_user.idols = [x for x in current_user.idols if x != user_id]
    ret = obj(result="200",fun="leave")
    return Response(tojson(ret), mimetype='application/json')

#支持或反对文章
@app.route("/praise")
@login_required
def praise():
    param = request.args.to_dict()
    if "writing_id" not in param:
        return '{result:404,msg:"缺少参数 writing_id"}'
    if "type" not in param:
        return '{result:404,msg:"缺少参数 type"}'

    sql = "update footmark set type={0},date='{1}' where writing_id={2} and user_id={3}".format(param["type"], datetime.datetime.now(),param["writing_id"],current_user.id)
    conn.execute(sql)
    rs = QueryObj("select type,count(*) as count where writing_id={0}".format(param["writing_id"]))
    ret = obj(result="200",fun="praise")
    ret.praise=
    ret.blame=
    ret.read=
    return Response(tojson(ret), mimetype='application/json')

