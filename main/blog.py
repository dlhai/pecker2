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
    fans = QueryObj("select id,name from user where id in (select fans_id from follow where idol_id=%s)"%writing.user_id)
    idols = QueryObj("select id,name from user where id in (select idol_id from follow where fans_id=%s)"%writing.user_id)
    recents=QueryObj("select id,title from writing where writing.user_id=%s order by date desc limit 0,30"%writing.user_id)
    replays=QueryObj("select writing.*,user.face, user.name from writing,user where writing.user_id==user.id and writing.writing_id=%s order by date desc limit %d,20"%(param["id"],pos))
    pgn=pagnition("/blog/view_writing?id=%s"%param["id"]+"&pos=%d",pos,"select count(*) as count from writing where writing.writing_id=%s"%param["id"])
    au=addup(current_user.id, writing_id)
    if au.me == None:
        sql = "insert into footmark(user_id,writing_id,type,date) values({0},{1},0,'{2}')".format(current_user.id, writing_id,datetime.datetime.now())
        conn.execute(sql)
        au.read += 1
    return render_template("view_writing.html",user=user,fans=fans,idols=idols,recents=recents,writing=writing, au=au,replays=replays, pgn=pgn, me=current_user)

#用户博文列表
@app.route('/blog/view_user')
def view_user():
    param = request.args.to_dict()
    if "id" not in param:
        return '{result:404,msg:"缺少参数 ls"}'
    pos=0
    if "pos" in param:
        pos=atoi(param["pos"])
    user_id = param["id"]
    user = QueryObj("select * from user where id=%s"%user_id)[0]
    fans = QueryObj("select id,name from user where id in (select fans_id from follow where idol_id=%s)"%user_id)
    idols = QueryObj("select id,name from user where id in (select idol_id from follow where fans_id=%s)"%user_id)
    writings=QueryObj("select * from writing where user_id=%s order by date desc limit %d,10"%(user_id,pos))
    pgn=pagnition("/blog/view_user?id=%s"%user_id+"&pos=%d",pos,"select count(*) as count from writing where writing.user_id=%s"%user_id,10)
    return render_template("view_user.html",user=user,fans=fans,idols=idols,writings=writings,pgn=pgn,me=current_user)

#用户消息记录
@app.route('/blog/view_msg')
def view_msg():
    param = request.args.to_dict()
    fans = QueryObj("select id,name,face,profile from user where id in (select fans_id from follow where idol_id=%s)"%current_user.id)
    idols = QueryObj("select id,name,face,profile from user where id in (select idol_id from follow where fans_id=%s)"%current_user.id)
    return render_template("message.html",fans=fans,idols=idols,me=current_user)

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

    def GetItem(ar, key, val ):
        sub = list(filter(lambda x: getattr(x,key)==val, ar))
        if len(sub)==0:
            return 0
        tt = getattr(sub[0],"count")
        return getattr(sub[0],"count")

    sql = "update footmark set type={0},date='{1}' where writing_id={2} and user_id={3}".format(param["type"], datetime.datetime.now(),param["writing_id"],current_user.id)
    conn.execute(sql)
    rs = QueryObj("select type,count(*) as count from footmark where writing_id={0} group by type".format(param["writing_id"]))
    ret = obj(result="200",fun="praise")
    ret.praise= GetItem(rs,"type",1)
    ret.blame= GetItem(rs,"type",-1)
    ret.read= GetItem(rs,"type",0)
    return Response(tojson(ret), mimetype='application/json')

#回复、发表文章
@app.route("/publish", methods=['POST'])
@login_required
def publish():
    params = request.args.to_dict()
    form =request.form.to_dict()
    rec = obj()
    r = obj(result="404",fun="publish")

    if "board" not in params:
        r.msg="缺少参数 board"
        return tojson(r)
    rec.board = params["board"]

    htm = form["body"]
    rec.body = htm.replace("'", "''") #sql字符串边界转义
    if rec.board != "4":
        if "title" not in form:
            r.msg="缺少参数 title"
            return tojson(r)
        rec.title = form["title"]
        if rec.title == "":
            r.msg="标题不能为空"
            return tojson(r)

        if "label" not in form:
            r.msg="缺少参数 label"
            return tojson(r)
        rec.label = form["label"]
        if rec.label == "":
            r.msg="缺少参数 label"
            return tojson(r)
        if len(rec.body) < 50:
            r.msg="内容不能少于50字节"
            return tojson(r)
    else:
        if "writing_id" not in form:
            r.msg="缺少参数 writing_id"
            return tojson(r)
        rec.writing_id = form["writing_id"]
        if rec.writing_id == "":
            r.msg="writing_id不能为空"
            return tojson(r)
        if len(rec.body) < 20:
            r.msg="内容不能少于20字节"
            return tojson(r)

    rec.section = ""
    rec.user_id = current_user.id
    rec.date = datetime.datetime.now()
    conn.execute(tosql("writing",rec))
    return Response(tojson(obj(result="200",fun="publish")), mimetype='application/json')

#给某人发消息
@app.route("/msgto", methods=['POST'])
@login_required
def msgto():
    params = request.args.to_dict()
    form =request.form.to_dict()
    rec = obj()
    r = obj(result="404",fun="msgto")

    #when  type       frm     to           table_id   row_id  jsn             say     readtime    result
    #      1changejob curuser jobmanager                      {newjob:jobid}  say
    #      2message   curuser touser                                          say
    #      3notify    system  relationuser table_id   row_id                  say
    
    if "type" not in params:
        r.msg="缺少参数 type"
        return tojson(r)
    rec.type = params["type"]

    if "user_id" not in params:
        r.msg="缺少参数 user_id"
        return tojson(r)
    rec.dst = params["user_id"]

    if rec.type == "1":#1changejob
        rec.jsn=form["jsn"]

    htm = form["body"]
    rec.say = htm.replace("'", "''") #sql字符串边界转义
    if len(rec.say) < 2:
        r.msg="内容不能少于2字节"
        return tojson(r)
    if len(rec.say) > 2048:
        r.msg="内容大于少于2048字节"
        return tojson(r)

    rec.src = current_user.id
    rec.whn = datetime.datetime.now()
    conn.execute(tosql("msg",rec))
    r.result="200"
    return Response(tojson(r), mimetype='application/json')

#读取消息
@app.route("/rdmsg")
@login_required
def rdmsg():
    params = request.args.to_dict()
    form =request.form.to_dict()
    rec = obj()
    r = obj(result="404",fun="rdmsg")
    if "user_id" in params:
        r.data = QueryObj("select msg.*, user.name,user.face,user.job from msg,user where msg.src=user.id and (src={me} and dst={to}) or (src={to} and dst={me}) order by whn desc limit 0,200".format(me=current_user.id, to=params["user_id"]))
    r.result="200"
    return Response(tojson(r), mimetype='application/json')
