#encoding:utf8
from sqlalchemy import *
from flask import Flask,request

app = Flask(__name__) 

engine = create_engine('sqlite:///./db/1514172619.db')
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

def to_array( qa ):
    return "["+ ",\n".join(["{"+",".join(['"'+str(t[0])+'":"'+str(t[1])+'"' for t in zip(row._parent.keys,row._row)])+"}" for row in qa ]) + "]"
def to_json( qa ):
    return "["+ ",\n".join(["{"+",".join(['"'+str(t[0])+'":"'+str(t[1])+'"' for t in zip(row._parent.keys,row._row)])+"}" for row in qa ]) + "]"
def query(s1, s2, s3=None):
    q1 = conn.execute(s1).fetchall()
    q2 = conn.execute(s2).fetchall()
    if s3 is not None:
        q3 = conn.execute(s3).fetchall()
        return '{"result":200,\n"fields":'+ to_json(q1) + ',\n"data":' + to_json(q2) + ',\n"addit":' + to_json(q3)+ "\n}\n";
    return '{"result":200,\n"fields":'+ to_json(q1) + ',\n"data":' + to_json(q2) + "\n}\n";

@app.route("/itemdetail")
def itemdetail():
    type = request.args.get('type')
    id = request.args.get('id')
    tbl = table[type]
    return query(select(base.sl).where(base.c.table==type),\
        select([tbl]).where(tbl.c.id==id).order_by(tbl.c.id))

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
        s3 = select(-[sub]).where(sub.c.winderarea_id==id).order_by(sub.c.id)
        return query(s1,s2,s3)
    else:
        return query(s1,s2)

@app.route("/sublist")
def sublist():
    type = request.args.get('type')
    id = request.args.get('id')
    subtype = organ[type]
    tbl = table[subtype]
    sel = select([tbl.c.id, tbl.c.name]).order_by(tbl.c.id)
    if type != "root":
        sel = select([tbl.c.id, tbl.c.name]).order_by(tbl.c.id).where(tbl.c[type+"_id"]==id)
    return to_json(conn.execute(sel).fetchall())

@app.route("/")
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run()

#测试链接
#http://127.0.0.1:5000/itemdetail?type=winderco&id=1
#http://127.0.0.1:5000/sublistdetail?type=root&id=1
#http://127.0.0.1:5000/sublistdetail?type=winderco&id=2
#http://127.0.0.1:5000/sublistdetail?type=winderarea&id=1
#http://127.0.0.1:5000/sublist?type=root&id=1
#http://127.0.0.1:5000/sublist?type=winderco&id=1
