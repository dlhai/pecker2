#encoding:utf8
from sqlalchemy import *
from flask import Flask,request, Response, jsonify
from werkzeug.utils import secure_filename
import pdb

class obj:
    pass

def tojson(o):
    if type(o) == type([]):
        return "["+",".join([tojson(t) for t in o ])+"]\n";
    elif type(o) == type({}):
        return "{"+",".join(['"'+k+'":'+tojson(v) for k,v in o.items() ])+"}\n";
    elif type(o) == type(obj()):
        return tojson(o.__dict__)
    else:
        return '"'+str(o)+'"'

app = Flask(__name__) 

engine = create_engine('sqlite:///./db/pecker.db')
#engine.echo = True
metadata = MetaData(engine)
conn = engine.connect()

db_tbl = [
    { "id": "0", "name": "none", "title": "占位" },
    { "id": "1", "name": "base", "title": "定义" },
    { "id": "2", "name": "link", "title": "一对多引用" },
    { "id": "3", "name": "addit", "title": "附件" },
    { "id": "4", "name": "config", "title": "配置信息" },
    { "id": "5", "name": "admarea", "title": "行政区划" },
    { "id": "6", "name": "user", "title": "供应商" },
    { "id": "7", "name": "certif", "title": "人员" },
    { "id": "8", "name": "edu", "title": "证件信息" },
    { "id": "9", "name": "employ", "title": "受教育经历" },
    { "id": "10", "name": "opus", "title": "就业经历" },
    { "id": "11", "name": "vender", "title": "发表作品" },
    { "id": "12", "name": "wait", "title": "" },
    { "id": "13", "name": "winderco", "title": "风电企业" },
    { "id": "14", "name": "winderprov", "title": "省区" },
    { "id": "15", "name": "winder", "title": "风场" },
    { "id": "16", "name": "winderarea", "title": "风区" },
    { "id": "17", "name": "efan", "title": "风机" },
    { "id": "18", "name": "leaf", "title": "叶片" },
    { "id": "19", "name": "fault", "title": "报修" },
    { "id": "20", "name": "devwh", "title": "设备驻地" },
    { "id": "21", "name": "dev", "title": "设备" },
    { "id": "22", "name": "devwork", "title": "设备任务" },
    { "id": "23", "name": "matprov", "title": "仓库省区" },
    { "id": "24", "name": "matwh", "title": "仓库" },
    { "id": "25", "name": "mat", "title": "材料" },
]
branch = {
    "devwh": { "sub": "", "image": "img/devwh.png", },

    "root": { "sub": "winderco", "image": "", },
    "winderco": {"sub": "winderprov", "image": "img/diy/1_open.png" },
    "winderprov": { "sub": "winder", "image": "img/folder.gif" },
    "winder": { "sub": "winderarea", "image": "img/diy/3.png" },
    "winderarea": { "sub": "efan", "image": "img/page.gif" },
    "efan": { "sub": "leaf", "image": "" },
    "leaf": { "sub": "", "image": "" },
}

def gettbl( nameorid ):
    s = str(nameorid)
    for x in db_tbl:
        if x["name"] == s or x['id'] == s:
            return x
    raise KeyError

tables = {
    'base':Table('base', metadata,autoload=True),
    'config':Table('config', metadata,autoload=True),
    'link':Table('link', metadata,autoload=True),
    'user':Table('user', metadata,autoload=True),
    'addit':Table('addit', metadata,autoload=True),
    'vender':Table('vender', metadata,autoload=True),
    'winderco':Table('winderco', metadata,autoload=True),
    'winderprov':Table('winderprov', metadata,autoload=True),
    'winder':Table('winder', metadata,autoload=True),
    'winderarea':Table('winderarea', metadata,autoload=True),
    'efan':Table('efan', metadata,autoload=True),
    'leaf':Table('leaf', metadata,autoload=True),
    'fault':Table('fault', metadata,autoload=True),
    'devwh':Table('devwh', metadata,autoload=True),
    'dev':Table('dev', metadata,autoload=True),
    'devwork':Table('devwork', metadata,autoload=True),
    'matprov':Table('matprov', metadata,autoload=True),
    'matwh':Table('matwh', metadata,autoload=True),
    'mat':Table('mat', metadata,autoload=True),
    }
base=tables["base"]
base.sl = [base.c.title, base.c.name, base.c.forder, base.c.ftype, base.c.twidth, base.c.tstyle]
organ = { "root": "winderco", "winderco": "winderprov", "winderprov": "winder", "winder":"winderarea","winderarea":"efan" }

def QueryObj( sql ):
    result = conn.execute(sql).fetchall()
    ret = []
    for row in result:
        r = obj();
        for t in row.items():
            setattr( r, t[0], t[1])
        ret.append(r)
    return ret;

#def to_array( qa ):
#    return "["+ ",\n".join(["{"+",".join(['"'+str(t[0])+'":"'+str(t[1])+'"' for t in zip(row._parent.keys,row._row)])+"}" for row in qa ]) + "]"
#def to_json( qa ):
#    return "["+ ",\n".join(["{"+",".join(['"'+str(t[0])+'":"'+str(t[1])+'"' for t in zip(row._parent.keys,row._row)])+"}" for row in qa ]) + "]"

def To(k,v):
    if v[0] == "(":
        return k +" in ("+",".join( ["'"+i+"'" for i in v.strip("()").split(",")]) + ")"
    else:
        return k+"='"+v+"'"

#查询结果为json
def jquery(q):
    a = conn.execute(q).fetchall()
    seq=[]
    for r in a:
        row = ['"'+str(t[0])+'":"'+str(t[1])+'"' for t in zip(r._parent.keys,r._row)]
        seq.append("{"+",".join(row)+"}")
    return "["+",\n".join(seq)+"]"

def query3(type,**kw):
    r = '{"result":200,"type":"'+type+'","ls":"'+type+'",\n'
    r += ",\n".join([ '"' + k + '":'+ jquery(v) for k,v in kw.items()] )
    r += "\n}\n"
    return Response(r, mimetype='application/json')

def query4(ls,**kw):
    r = '{"result":200,"ls":"'+ls+'",\n'
    r += ",\n".join([ '"' + k + '":'+ jquery(v) for k,v in kw.items()] )
    r += "\n}\n"
    return Response(r, mimetype='application/json')

#登录表单
@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/login")
def login():
    param = request.args.to_dict()
    user = QueryObj( "select * from user where account='%s'"%param["account"])
    if len(user)>0 and hasattr( user[0], "account" ) and user[0].pwd == param["pwd"]:
        return '{"login":"'+param['account']+'","result":200}\n'
    else:
        return '{"login":"'+param['account']+'","result":404}\n'

#frame用来读取当前用户信息，需要所在单位名称、下级单位列表
@app.route("/roleuser") 
def roleuser():
    param = request.args.to_dict()
    
    ret = QueryObj( "select id,account,name,face,depart_id,depart_table,job from user where account='%s'"%(param["account"]))
    if len(ret) <= 0:
        return '{"roleuser":"'+param['account']+'","result":404}\n'
    user = ret[0]

    #找到用户的所在单位，若所在单位是风场，则需要读取风区列表
    if user.depart_table != 0: 
        tbl = gettbl(user.depart_table)
        user.depart = QueryObj( "select id, name from "+tbl["name"]+" where id="+str(user.depart_id))[0]
        if tbl["name"] == "winder":
            user.sub = QueryObj( "select id, name from winderarea where winder_id="+str(user.depart_id))
    else:
        user.depart_name = ""

    ret=obj()
    ret.fun="roleuser"
    ret.param=param
    ret.result = "200"
    ret.data = user
    return Response(tojson(ret), mimetype='application/json')

#frame用来填用户角色组合框
@app.route("/roleuserall") 
def roleuserall():
    user = QueryObj( "select min(id) as id, account, name, job, depart_id, depart_table, face from user group by job")
    for u in [x for x in user if x.depart_table != 0]:
        tbl = gettbl(u.depart_table)
        u.depart = QueryObj( "select * from "+tbl["name"]+" where id="+str(u.depart_id))[0]
        if tbl["name"] == "winder":
            u.sub = QueryObj( "select id, name from winderarea where winder_id="+str(u.depart_id))
    ret=obj()
    ret.fun="roleuserall"
    ret.result = "200"
    ret.data = user
    return Response(tojson(ret), mimetype='application/json')

#id到名字的转换
@app.route("/id2name")
def id2name():
    r = {}
    for k,v in request.args.to_dict().items():
        ar = k.split("_")
        qa = conn.execute( "select name from " + ar[0] + ' where id="' + v+'"').fetchall()
        r[k+"_"+v]=qa[0][0]
    return jsonify(r)

@app.route("/upload",methods=['POST'])
def upload():
    f = request.files["file"]
    f.save("./uploads/" + f.filename)
    return f.filename


#查询
#测试链接 http://127.0.0.1:5000/rd?ls=[表名]&key1=val1&key2=val2....
@app.route("/rd")
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
    return query4(ls,fields=select(base.sl).where(base.c.table==ls),data = sql)

#查询用户
#测试链接 http://127.0.0.1:5000/queryUser?type=winder&key1=val1&key2=val2....
@app.route("/queryuser")
def queryuser():
    param = request.args.to_dict()
    if ("depart_name" in param ):
        type = db_tbl[param["depart_name"]]
        sql = "select "+type+".name as depart_name, user.id,user.account,user.face,user.depart_id,"\
            +"user.job,user.skill,user.name,user.code,user.sex,user.ethnic,user.birth,user.origin,"\
            +"user.idimg,user.phone,user.qq,user.mail,user.wechat,user.addr from user,"+type\
            +" where user.depart_id = "+type+".id and user.depart_table='"+tbl["id"]+"' and "
    else:
        sql = "select user.id,user.account,user.face,user.depart_id,"\
            +"user.job,user.skill,user.name,user.code,user.sex,user.ethnic,user.birth,user.origin,"\
            +"user.idimg,user.phone,user.qq,user.mail,user.wechat,user.addr from user"\
            +" where "
    sql +=" and ".join([ To(k,v) for k,v in param.items()])
    return query4("queryuser",fields=select(base.sl).where(base.c.table=="user"),data = sql)

#-----------------------以下接口将被废弃-------------------------------

#查询(由于部分表有type字段与type参数作为表名冲突被废弃)
#测试链接 http://127.0.0.1:5000/query?type=[表名]&key1=val1&key2=val2....
@app.route("/query")
def _query():
    d = request.args.to_dict()
    type = d["type"]
    del d["type"]

    # 限制对部分表的查询
    if type== "base" or type == "user":
        return 404

    tbl = tables[type]
    sql = "select * from "+type
    if len(d) > 0:
        sql += " where "+" and ".join([ k+"='"+v+"'" for k,v in d.items()])
    return query3(type,fields=select(base.sl).where(base.c.table==type),data = sql)

#leaf_su8设备sheet用
#测试链接 http://127.0.0.1:5000/itemdetail?type=winderco&id=1
@app.route("/itemdetail")
def itemdetail():
    type = request.args.get('type')
    id = request.args.get('id')
    tbl = tables[type]
    return query3(type,fields=select(base.sl).where(base.c.table==type),\
        data=select([tbl]).where(tbl.c.id==id).order_by(tbl.c.id))

#leaf_su8子设备列表tables用，type=root时，仅超级用户可用
#测试链接 http://127.0.0.1:5000/sublistdetail?type=root&id=1
#测试链接 http://127.0.0.1:5000/sublistdetail?type=winderco&id=1
#测试链接 http://127.0.0.1:5000/sublistdetail?type=winderarea&id=1
@app.route("/sublistdetail")
def sublistdetail():
    type = request.args.get('type')
    id = request.args.get('id')
    subtype = organ[type]
    tbl = tables[subtype]
    s1 = select(base.sl).where(base.c.table==subtype).order_by(base.c.id)
    s2 = select([tbl]).order_by(tbl.c.id)
    if type != "root":
        s2 = select([tbl]).where(tbl.c[type+"_id"]==id).order_by(tbl.c.id)
    if subtype == "efan":
        sub = tables["leaf"]
        s3 = select([sub]).where(sub.c.winderarea_id==id).order_by(sub.c.id)
        return query3(type,fields=s1,data=s2,addit=s3)
    else:
        return query3(type,fields=s1,data=s2)

#leaf_su8设备树用，【暂废：winder补充了position，用来在】
#测试链接 http://127.0.0.1:5000/sublist?type=root&id=1
#测试链接 http://127.0.0.1:5000/sublist?type=winderco&id=1
@app.route("/sublist")
def sublist():
    type = request.args.get('type')
    id = request.args.get('id')
    tbl = tables[organ[type]]
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
    tbl1 = tables["winder"]
    tbl2 = tables["winderarea"]

    if winder_id =="0":
        s1 = select([tbl1.c.id, tbl1.c.name,tbl1.c.position]).order_by(tbl1.c.id)
        s2 = select([tbl2.c.id, tbl2.c.name,tbl2.c.position]).order_by(tbl2.c.id)
        return query3("winder",winder=s1,winderarea=s2)
    else:
        s1 = select([tbl1.c.id, tbl1.c.name,tbl1.c.position]).order_by(tbl1.c.id).where(tbl1.c.id==winder_id)
        s2 = select([tbl2.c.id, tbl2.c.name,tbl2.c.position]).order_by(tbl2.c.id).where(tbl2.c.winder_id==winder_id)
        return query3("winder", winder=s1,winderarea=s2)

#leafmap用来显示地图上风电机分布，除su外，仅本风场人员可访问
#与sublist之区别是这是无下级叶片列表，仅efan, sublist无gps
#测试链接 http://127.0.0.1:5000/efanlist?winder_id=1
@app.route("/efanlist")
def efanlist():
    winder_id = request.args.get('winder_id')
    tbl = tables["efan"]
    s = select([tbl.c.id, tbl.c.position]).where(tbl.c.winder_id==winder_id).order_by(tbl.c.id)
    return query3("efan", efanlist=s)

#---------------------以上接口将被废弃---------------------------------------
if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run()

#查询代表用户的sql
#select depart_id as c1, "" as c2, * from user where depart_table== "__sys__" union
#select min(depart_id) as c1, winder.name as c2, user.* from user,winder where depart_table== "winder" and depart_id == winder.id group by job

#暂未限制Query对User的查询
#添加QueryUser接口，密码处理，所在单位处理
#风场面板中还没有相关人员显示。

