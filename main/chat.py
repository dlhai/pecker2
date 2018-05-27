#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
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
#      1changejob curuser jobmanager                      {newjob:jobid}  say
#      2message   curuser touser                                          say
#      3notify    system  relationuser table_id   row_id                  say

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

    r.sysmsgs = QueryObj("select src as id, count(*) as count from msg where type!=2 and readtime is null and dst=%s group by src"%current_user.id)
    return tojson(r)

#用户消息界面，好友列表
@app.route('/blog/view_msg')
@login_required
def view_msg():
    param = request.args.to_dict()
    fans = QueryObj("select id,name,face,profile from user where id in (select fans_id from follow where idol_id=%s)"%current_user.id)
    idols = QueryObj("select id,name,face,profile from user where id in (select idol_id from follow where fans_id=%s)"%current_user.id)

    #news = QueryObj("select src,user.name,user.face,user.profile,count(*) as count from msg,user where msg.src=user.id and type=2 and readtime is null and dst=%s group by src"%current_user.id)
    strangers = []
    #for x in news:
    #    t = filter( lambda y: y.id ==x.src, fans)
    #    if len(t) > 0:
    #        t[0].count = x.count
    #        continue
    #    t = filter( lambda y: y.id ==x.src, idols)
    #    if len(t) > 0:
    #        t[0].count = x.count
    #        continue
    #    strangers.append(x)

    sysmsgs = []#QueryObj("select src,user.name,user.profile,count(*) as count from msg,user where msg.src=user.id and type!=2 and readtime is null and dst=%s group by src"%current_user.id)
    return render_template("chat.html",fans=fans,idols=idols,strangers=strangers,sysmsgs=sysmsgs, me=current_user)


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
    conn.execute(toinsert("msg",rec))
    r.result="200"
    return Response(tojson(r), mimetype='application/json')

#读取消息
#1.mtd=check 读取书签之后的未读消息(检测新消息)
#2.mtd=chat&user_id= 读取与某人的最新聊天记录(打开聊天窗口时)
#3.mtd=chatlog&user_id=&pos= 读取与某人的小于某id的一页消息(聊天窗口向前翻一页)
@app.route("/rdmsg")
@login_required
def rdmsg():
    params = request.args.to_dict()
    form =request.form.to_dict()
    rec = obj()
    r = obj(result="404",fun="rdmsg")

    if "mtd" not in params:
        r.msg="缺少参数 mtd"
        return tojson(r)
    mtd = params["mtd"]
   
    #1.mtd=check 读取书签之后的未读消息(检测新消息)
    if mtd == "check":
        r.data = QueryObj("select src, user.name,user.face,user.job,count(*) as count from msg,user where msg.src=user.id and dst={me} group by src".format(me=current_user.id))
        if ( len(r.data)>0):
            m=obj(user_id=current_user.id, type=1,whn=r.data[0].whn)
            conn.execute(toinsert("mark",m))
        else:
            m = m[0]
            r.data = QueryObj("select msg.*, user.name,user.face,user.job from msg,user where msg.src=user.id and (src={me} or dst={me}) and whn>'{whn}' order by whn limit 0,200".format(me=current_user.id,whn=m.whn))
            r.end = (len(r.data) < 200)
            if ( len(r.data)>0):
                m.whn=r.data[0].whn
                sql = "update mark set whn={whn} where id={id}".format(m)
                conn.execute(sql)
        r.result="200"
        return Response(tojson(r), mimetype='application/json')

    #2.mtd=chat&user_id= 读取与某人的最新聊天记录(打开聊天窗口时，从首条未读消息开始向后翻)
    elif mtd == "chat":
        if "user_id" not in params:
            r.msg="缺少参数 user_id"
            return tojson(r)
        r.data = QueryObj("select msg.*, user.name,user.face,user.job from msg,user where msg.src=user.id and ((src={me} and dst={to}) or (src={to} and dst={me})) order by whn limit 0,200".format(me=current_user.id, to=params["user_id"]))
        r.result="200"
        return Response(tojson(r), mimetype='application/json')
    
    #3.mtd=chatlog&user_id=&pos= 读取与某人的小于某id的一页消息(聊天窗口向前翻一页)
    elif mtd == "chatlog":
        if "user_id" not in params:
            r.msg="缺少参数 user_id"
            return tojson(r)
        if "pos" not in params:
            r.msg="缺少参数 pos"
            return tojson(r)
        r.data = QueryObj("select msg.*, user.name,user.face,user.job from msg,user where msg.src=user.id and (src={me} and dst={to}) or (src={to} and dst={me}) order by whn limit {pos},200".format(me=current_user.id, to=params["user_id"], pos=params["pos"]))
        r.result="200"
        return Response(tojson(r), mimetype='application/json')

    r.msg="不能识别的mtd="+params["mtd"]
    return tojson(r)
