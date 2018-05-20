#encoding:utf8
from flask import Flask,request, Response,jsonify,render_template
from flask_login import login_required,current_user
import datetime
from main2 import app,login_manager,check
from main.model import *
from main.tools import *

#申请转换职业（这部分未完） 
@app.route("/user/reqjob")
@login_required
def chgjob():
    param = request.args.to_dict()
    if "user_id" not in param:
        return '{result:404,msg:"缺少参数 user_id"}'

    sql = "insert into follow(fans_id,idol_id,date) values({0},{1},'{2}')".format(current_user.id, param["user_id"],datetime.datetime.now())
    conn.execute(sql)
    current_user.idols += [param["user_id"]]
    ret = obj(result="200",fun="follow")
    return Response(tojson(ret), mimetype='application/json')

