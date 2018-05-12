#encoding:utf8
from main.tools import *
from sqlalchemy import *
from flask import Response

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
    { "id": "26", "name": "matin", "title": "入库单" },
    { "id": "27", "name": "matinrec", "title": "入库记录" },
    { "id": "28", "name": "matout", "title": "出库单" },
    { "id": "29", "name": "matoutrec", "title": "出库记录" },
    { "id": "30", "name": "chat", "title": "聊天记录" },
]

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
    'chat':Table('chat', metadata,autoload=True),
    }
base=tables["base"]
base.sl = [base.c.title, base.c.name, base.c.forder, base.c.ftype, base.c.twidth, base.c.tstyle]
organ = { "root": "winderco", "winderco": "winderprov", "winderprov": "winder", "winder":"winderarea","winderarea":"efan" } #定义上下级结构关系

def QueryObj( sql ):
    result = conn.execute(sql).fetchall()
    ret = []
    for row in result:
        r = obj();
        for t in row.items():
            if t[1] == None:
                setattr( r, t[0], "")
            else:
                setattr( r, t[0], t[1])
        ret.append(r)
    return ret;

def query5(ls,**kw):
    r=obj(result=200,ls=ls)
    for k,v in kw.items():
        setattr(r,k,QueryObj(v))
    return Response(tojson(r), mimetype='application/json')

def loaduser(where):
    ret = QueryObj( "select * from user where "+where)
    if len(ret) <= 0:
        return
    #找到用户的所在单位，若所在单位是风场，则需要读取风区列表
    user = ret[0]
    if atoi(user.depart_table) != 0: 
        tbl = gettbl(user.depart_table)
        user.depart = QueryObj( "select id, name from "+tbl["name"]+" where id="+str(user.depart_id))[0]
        if tbl["name"] == "winder":
            user.sub = QueryObj( "select id, name from winderarea where winder_id="+str(user.depart_id))
    return user

class pagnition:
    def __init__( table,where, curpage ):
        sql= "select count(*) from "+ table + " " + where
        self.curpage = curpage


