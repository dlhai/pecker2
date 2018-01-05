#encoding:utf8
from sqlalchemy import *
from flask import Flask,request, Response, jsonify
import pdb

app = Flask(__name__) 

engine = create_engine('sqlite:///./db/pecker.db')
#engine.echo = True
metadata = MetaData(engine)
conn = engine.connect()

table = {
    'base':Table('base', metadata,autoload=True),
    'user':Table('user', metadata,autoload=True),
    'leaf_vender':Table('leaf_vender', metadata,autoload=True),
    'efan_vender':Table('efan_vender', metadata,autoload=True),
    'winderco':Table('winderco', metadata,autoload=True),
    'winderprov':Table('winderprov', metadata,autoload=True),
    'winder':Table('winder', metadata,autoload=True),
    'winderarea':Table('winderarea', metadata,autoload=True),
    'efan':Table('efan', metadata,autoload=True),
    'leaf':Table('leaf', metadata,autoload=True)
    }
base=table["base"]
base.sl = [base.c.title, base.c.name, base.c.type, base.c.ftype, base.c.twidth, base.c.tstyle]
organ = { "root": "winderco", "winderco": "winderprov", "winderprov": "winder", "winder":"winderarea","winderarea":"efan" }

#def to_array( qa ):
#    return "["+ ",\n".join(["{"+",".join(['"'+str(t[0])+'":"'+str(t[1])+'"' for t in zip(row._parent.keys,row._row)])+"}" for row in qa ]) + "]"
def to_json( qa ):
    return "["+ ",\n".join(["{"+",".join(['"'+str(t[0])+'":"'+str(t[1])+'"' for t in zip(row._parent.keys,row._row)])+"}" for row in qa ]) + "]"
#def query(s1, s2, s3=None):
#    q1 = conn.execute(s1).fetchall()
#    q2 = conn.execute(s2).fetchall()
#    if s3 is not None:
#        q3 = conn.execute(s3).fetchall()
#        return '{"result":200,\n"fields":'+ to_json(q1) + ',\n"data":' + to_json(q2) + ',\n"addit":' + to_json(q3)+ "\n}\n";
#    return '{"result":200,\n"fields":'+ to_json(q1) + ',\n"data":' + to_json(q2) + "\n}\n";

#def query2(**kw):
#    r = '{"result":200,\n'
#    r += ",\n".join([ '"' + k + '":'+ to_json(conn.execute(v).fetchall()) for k,v in kw.items()] )
#    r += "\n}\n"
#    print("query2")
#    return r

def query3(**kw):
    r = '{"result":200,\n'
    r += ",\n".join([ '"' + k + '":'+ to_json(conn.execute(v).fetchall()) for k,v in kw.items()] )
    r += "\n}\n"
    return Response(r, mimetype='application/json')

#查询
#测试链接 http://127.0.0.1:5000/query?type=[表名]&key1=val1&key2=val2....
@app.route("/query")
def _query():
    d = request.args.to_dict()
    type = d["type"]
    del d["type"]
    sql = "select * from "+type
    if len(d) > 0:
        sql += " where "+"and ".join([ k+"="+v for k,v in d.items()])
    return query3(fields=select(base.sl).where(base.c.table==type),data = sql)

#leaf_su8设备sheet用
#测试链接 http://127.0.0.1:5000/itemdetail?type=winderco&id=1
@app.route("/itemdetail")
def itemdetail():
    type = request.args.get('type')
    id = request.args.get('id')
    tbl = table[type]
    return query3(fields=select(base.sl).where(base.c.table==type),\
        data=select([tbl]).where(tbl.c.id==id).order_by(tbl.c.id))

#leaf_su8子设备列表table用，type=root时，仅超级用户可用
#测试链接 http://127.0.0.1:5000/sublistdetail?type=root&id=1
#测试链接 http://127.0.0.1:5000/sublistdetail?type=winderco&id=1
#测试链接 http://127.0.0.1:5000/sublistdetail?type=winderarea&id=1
@app.route("/sublistdetail")
def sublistdetail():
    type = request.args.get('type')
    id = request.args.get('id')
    subtype = organ[type]
    tbl = table[subtype]
    s1 = select(base.sl).where(base.c.table==subtype).order_by(base.c.id)
    s2 = select([tbl]).order_by(tbl.c.id)
    if type != "root":
        s2 = select([tbl]).where(tbl.c[type+"_id"]==id).order_by(tbl.c.id)
    if subtype == "efan":
        sub = table["leaf"]
        s3 = select([sub]).where(sub.c.winderarea_id==id).order_by(sub.c.id)
        return query3(fields=s1,data=s2,addit=s3)
    else:
        return query3(fields=s1,data=s2)

#leaf_su8设备树用，【暂废：winder补充了position，用来在】
#测试链接 http://127.0.0.1:5000/sublist?type=root&id=1
#测试链接 http://127.0.0.1:5000/sublist?type=winderco&id=1
@app.route("/sublist")
def sublist():
    type = request.args.get('type')
    id = request.args.get('id')
    tbl = table[organ[type]]
    sel = ""
    if type =="root":
        sel = select([tbl.c.id, tbl.c.name]).order_by(tbl.c.id)
    #elif type == "winder":
    #    sel = select([tbl.c.id, tbl.c.name,tbl.c.position]).order_by(tbl.c.id).where(tbl.c[type+"_id"]==id)
    else:
        sel = select([tbl.c.id, tbl.c.name]).order_by(tbl.c.id).where(tbl.c[type+"_id"]==id)
    return to_json(conn.execute(sel).fetchall())

#leafmap用来显示地图上的风场地标和风区轮廓，考虑到调度，不限制权限，任何人可用
#测试链接 http://127.0.0.1:5000/winderlist?winder_id=0
#测试链接 http://127.0.0.1:5000/winderlist?winder_id=1
@app.route("/winderlist")
def winderlist():
    winder_id = request.args.get('winder_id') #为0仅su可用，表示获得全部风场
    tbl1 = table["winder"]
    tbl2 = table["winderarea"]

    if winder_id =="0":
        s1 = select([tbl1.c.id, tbl1.c.name,tbl1.c.position]).order_by(tbl1.c.id)
        s2 = select([tbl2.c.id, tbl2.c.name,tbl2.c.position]).order_by(tbl2.c.id)
        return query3(winder=s1,winderarea=s2)
    else:
        s1 = select([tbl1.c.id, tbl1.c.name,tbl1.c.position]).order_by(tbl1.c.id).where(tbl1.c.id==winder_id)
        s2 = select([tbl2.c.id, tbl2.c.name,tbl2.c.position]).order_by(tbl2.c.id).where(tbl2.c.winder_id==winder_id)
        return query3(winder=s1,winderarea=s2)

#leafmap用来显示地图上风电机分布，除su外，仅本风场人员可访问
#与sublist之区别是这是无下级叶片列表，仅efan, sublist无gps
#测试链接 http://127.0.0.1:5000/efanlist?winder_id=1
@app.route("/efanlist")
def efanlist():
    winder_id = request.args.get('winder_id')
    tbl = table["efan"]
    s = select([tbl.c.id, tbl.c.position]).where(tbl.c.winder_id==winder_id).order_by(tbl.c.id)
    return query3(efanlist=s)

#登录
@app.route("/")
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()
