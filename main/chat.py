#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime,json
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

############## websocket功能 ###############################################
#@sockets.route('/echo')
#def echo_socket(ws):
#    while not ws.closed:
#        message = ws.receive()
#        ws.send("replay:"+message+"!")

############## websocket功能 ###############################################

#when  type       src      dst         table_id   row_id  jsn             say     readtime    result
#      0message   curuser touser                                          say
#      1notify    system  relationuser table_id   row_id                  say
#
#      5changejob curuser jobmanager                      {newjob:jobid}  say

#用户消息界面，好友列表
@app.route('/blog/chat')
@login_required
def chat():
    return render_template("chat.html")

@app.route('/blog/rdfriends')
@login_required
def rdfriends():
    r = obj(result="200",fun="msgcheck")
    r.fans = QueryObj("select id,name,face,profile,job,depart_id from user where id in (select fans_id from follow where idol_id=%s)"%current_user.id)
    r.idols = QueryObj("select id,name,face,profile,job,depart_id from user where id in (select idol_id from follow where fans_id=%s)"%current_user.id)
    [ setattr(x,"prof",getjob(x.job)["sname"]) for x in r.fans]
    [ setattr(x,"prof",getjob(x.job)["sname"]) for x in r.idols]
    return tojson(r)

#主界面，检查未读消息数量
@app.route('/msgcheck')
@login_required
def msgcheck():
    r = obj(result="200",fun="msgcheck")
    r.count = QueryObj("select count(*) as count from msg where readtime is null and dst=%s"%current_user.id)[0].count
    return tojson(r)

#消息界面，检查未读消息数量，精确到好友
@app.route('/msgcheckdetail')
@login_required
def msgcheckdetail():
    r = obj(result="200",fun="msgcheckdetail")
    r.fans = QueryObj("select fans_id as id from follow where idol_id=%s"%current_user.id)
    r.idols = QueryObj("select idol_id as id from follow where fans_id=%s"%current_user.id)

    newmsgs = QueryObj("select src as id,count(*) as count from msg where type=2 and readtime is null and dst=%s group by src"%current_user.id)
    r.strangers = []
    for x in newmsgs:
        t1 = list(filter( lambda y: y.id ==x.id, r.fans))
        if len(t1) > 0:
            t1[0].count = x.count
        t2 = list(filter( lambda y: y.id ==x.id, r.idols))
        if len(t2) > 0:
            t2[0].count = x.count
        if len(t1) + len(t2) > 0:
            continue
        r.strangers.append(x)
    r.fans = list(filter(lambda x:hasattr(x,"count"),r.fans))
    r.idols = list(filter(lambda x:hasattr(x,"count"),r.idols))

    r.sysmsgs = QueryObj("select src as id, count(*) as count,max(whn) as whn from msg where type!=2 and readtime is null and dst=%s group by src"%current_user.id)
    return tojson(r)


#给某人发消息
@app.route("/msgto", methods=['POST'])
@login_required
def msgto():
    params = request.args.to_dict()
    form =request.form.to_dict()
    rec = obj()
    r = obj(result="404",fun="msgto")

    if "type" not in params:
        r.msg="缺少参数 type"
        return tojson(r)
    rec.type = params["type"]

    if "user_id" not in params:
        r.msg="缺少参数 user_id"
        return tojson(r)
    rec.dst = params["user_id"]

    if rec.type == "5":#1changejob
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
    conn.execute(toinsert("msg",rec))
    r.result="200"
    return Response(tojson(r), mimetype='application/json')

#读取消息
@app.route("/rdmsg")
@login_required
def rdmsg():
    params = request.args.to_dict()

    r = obj(result="404",fun="rdmsg")
    if "type" not in params:
        r.msg="缺少参数 type"
        return tojson(r)
    if "user_id" not in params:
        r.msg="缺少参数 user_id"
        return tojson(r)
    if params["type"] == "sysmsgs":
        sql = "select * from msg where type!=0 and ((src={me} and dst={to}) or (src={to} and dst={me}))"
    else:
        sql = "select * from msg where type=0 and ((src={me} and dst={to}) or (src={to} and dst={me}))"
    r.data = QueryObj((sql+" order by whn limit 0,200").format(me=current_user.id, to=params["user_id"]))
    [ setattr(x,"whn",x.whn[5:16]) for x in r.data]
    r.result="200"

    vals = obj(readtime=datetime.datetime.now())
    whrs = obj(dst=current_user.id,src=params["user_id"], type= 1 if params["type"]=="sysmsgs" else 0)
    conn.execute(toupdate("msg",vals,whrs))

    return Response(tojson(r), mimetype='application/json')


#处理需要批准的消息
@app.route("/msgdeal")
@login_required
def msgdeal():
    params = request.args.to_dict()
    r = obj(result="404",fun="msgdeal")

    if "id" not in params:
        r.msg="缺少参数 id"
        return tojson(r)

    if "result" not in params:
        r.msg="缺少参数 result"
        return tojson(r)

    rec = QueryObj( "select * from msg where id="+params["id"] )
    if len(rec) != 1:
        r.msg="id 不正确"
        return tojson(r)
    rec = rec[0]
    if rec.result != "":
        r.msg="id 不正确"
        return tojson(r)

    if rec.type == 5:
        vals = obj(readtime=datetime.datetime.now(),result=params["result"])
        whrs = obj(id=params["id"])
        conn.execute(toupdate("msg",vals,whrs))

        jsn = json.loads(rec.jsn.replace("'", '"'))
        msg = obj(type=2,whn=datetime.datetime.now(),src=current_user.id,dst=rec.src)
        msg.whn = datetime.datetime.now()
        if vals.result == "1":
            msg.say ="您于【%s】发起的职业变更申请被批准了，您的职业已经变更为【%s】"%( rec.whn[5:16], getjob(jsn["newjob"])["sname"])
        else:
            msg.say ="您于【%s】发起的职业变更申请被拒绝了。"%rec.whn[5:16]
        conn.execute(toinsert("msg",msg))

    r.result="200"
    return Response(tojson(r), mimetype='application/json')