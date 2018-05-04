#encoding:utf8
from flask import request,Response
import json
from model import *
from flask_login import (LoginManager, login_required, login_user,logout_user, UserMixin,current_user)

from flask import Blueprint
main = Blueprint('main', __name__)

class User(UserMixin):
    def __init__(self,user ):
        self.__dict__ = user.__dict__
    def get_id(self):
        return self.id
 
@main.route('/login')
def login():
    return '{"login":"sss","result":404}\n'

#查询
#测试链接 http://127.0.0.1:5000/rd?ls=[表名]&key1=val1&key2=val2....
@main.route("/rd")
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
    ol=query(ls,fields=select(base.sl).where(base.c.table==ls),data = sql)
    return Response(tojson(ol), mimetype='application/json')
