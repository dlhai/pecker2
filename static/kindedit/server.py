#encoding:utf8
from sqlalchemy import *
from flask import Flask,request, Response, jsonify
from flask_sockets import Sockets
from werkzeug.utils import secure_filename
from flask_login import (LoginManager, login_required, login_user,
                             logout_user, UserMixin,current_user)
import os.path
import json
import pdb
import random

app = Flask(__name__)
sockets = Sockets(app)

def rndqq():
    return ''.join(random.sample("0123456789", 8))

class obj:
    def __init__(self,  **kw ):
        for k,v in kw.items():
            setattr( self, k, v)

def tojson(o):
    if type(o) == type([]):
        return "["+",".join([tojson(t) for t in o ])+"]\n";
    elif type(o) == type({}):
        return "{"+",".join(['"'+k+'":'+tojson(v) for k,v in o.items() ])+"}\n";
    elif type(o) == type(obj()):
        return tojson(o.__dict__)
    elif o == None:
        return '""'
    else:
        return '"'+str(o)+'"'


#首页
@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/tt")
def tt():
    return "ohoh!"


#新建
#测试链接 http://127.0.0.1:5000/cr
@app.route("/cr", methods=['GET', 'POST'])
def cr():
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
        ret =obj();
        for k,v in files.items(): 
            fname = "./uploads/{id}{ext}".format(id=rndqq(),ext=os.path.splitext(v.filename)[1] )
            dic[k]=fname
            v.save("./static/"+fname)
            ret.error = 0
            ret.url = fname
        aa = tojson(ret)

        bb = '{"error" : 0,"url" : "'+fname+'"}'
    return bb


if __name__ == "__main__":
	print("注意：需要把html和js放在static文件夹下")
    app.config['JSON_AS_ASCII'] = False
    app.run( host="0.0.0.0")
