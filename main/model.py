#encoding:utf8
from main.tools import *
from sqlalchemy import *
from flask import Response

engine = create_engine('sqlite:///./db/pecker.db')
#engine.echo = True
metadata = MetaData(engine)
conn = engine.connect()

db_job = [
    {"id":"1","sname":"su叶片","name":"叶片超级帐号","su":""},
    {"id":"2","sname":"风场长","name":"风场主管","su":"1"},
    {"id":"3","sname":"驻场","name":"驻场","su":"1"},
    {"id":"4","sname":"su设备","name":"设备超级帐号","su":""},
    {"id":"5","sname":"驻地长","name":"驻地主管","su":"4"},
    {"id":"6","sname":"司机","name":"设备司机","su":"4"},
    {"id":"7","sname":"su仓库","name":"仓库超级帐号","su":""},
    {"id":"8","sname":"仓库长","name":"仓库主管","su":"7"},
    {"id":"9","sname":"仓管","name":"仓库管理员","su":"7"},
    {"id":"10","sname":"su调度","name":"调度超级帐号","su":""},
    {"id":"11","sname":"调度长","name":"调度主管","su":"10"},
    {"id":"12","sname":"调度","name":"调度","su":"10"},
    {"id":"13","sname":"su专家","name":"专家超级帐号","su":""},
    {"id":"14","sname":"专家","name":"专家","su":"13"},
    {"id":"15","sname":"su技工","name":"技工超级帐号","su":""},
    {"id":"16","sname":"队长","name":"维修队长","su":"15"},
    {"id":"17","sname":"技工","name":"技工","su":"15"},
    {"id":"18","sname":"su博客","name":"博客超级帐号","su":""},
    {"id":"19","sname":"公众","name":"公众","su":"18"},
]
def getjob(id):
    id=str(id)
    return list(filter(lambda x: x["id"]==id, db_job))[0]

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
    user.idols = list(map( lambda x:x.idol_id,QueryObj( "select idol_id from follow where fans_id="+str(user.id))))
    return user

from math import ceil
class pagnition:
    #sql必须是select count(*) from ....
    def __init__( self,url,pos,sql, pagesize=20 ):
        self.curpage = pos//pagesize
        self.pagesize = pagesize
        self.url=url
        self.pagecount=ceil(QueryObj(sql)[0].count/self.pagesize)
        self.pagecount = self.pagecount if self.pagecount != 0 else 1

    def pageurl(self,page):
        if page=='cur':
            return self.url%(self.curpage*self.pagesize)
        elif page=='cur-1':
            p=self.curpage-1
            p=p if p >= 0 else 0 
            return self.url%(p*self.pagesize)
        elif page=='cur+1':
            p=self.curpage+1
            p=p if p < self.pagecount else self.pagecount-1 
            return self.url%(p*self.pagesize)
        elif page==-1:
            return self.url%((self.pagecount-1)*self.pagesize)
        else:
            return self.url%(page*self.pagesize)

    def pages(self):
        ar = [x+self.curpage -2 for x in range(5)]
        while ar[0] < 0: #位于开头时，后移
            ar = [ x+1 for x in ar]
        while ar[4] >= self.pagecount:#位于结尾时，前移
            ar = [ x-1 for x in ar]
        ar = [ x for x in ar if x >=0 ] #少于5页时
        return ar

def todict(p):
    d = p
    if type(p)!=type({}):
        d = p.__dict__
    return d

def toinsert(tbl,obj):
    if type(obj) == type([]):
        [delattr(u,"id") for u in obj if hasattr(u,"id")]
        d = todict(obj[0])
        fields=",".join(map( lambda x: "'"+x+"'", d.keys()))
        values = ",".join(["("+",".join(map( lambda x: "'"+str(x)+"'", u.__dict__.values()))+")" for u in obj ])
        sql = "insert into {0}({1}) values{2}".format(tbl, fields,values)
    else:
        d = todict(obj)
        if "id" in d:
            del d["id"]
        fields=",".join(map( lambda x: "'"+x+"'", d.keys()))
        values=",".join(map( lambda x: "'"+str(x)+"'", d.values()))
        sql = "insert into {0}({1}) values({2})".format(tbl, fields,values)
    return sql


def toupdate(tbl,values,where):
    dvals = todict(values)
    if "id" in dvals:
        del dvals["id"]
    vals=",".join([ k+"='"+str(v)+"'" for k,v in dvals.items()])
    whrs=" and ".join([ k+"='"+str(v)+"'" for k,v in todict(where).items()])
    sql = "update {0} set {1} where {2}".format(tbl, vals,whrs)
    return sql

def todelete(tbl,where):
    whrs=" and ".join([ k+"='"+str(v)+"'" for k,v in where.__dict__.items()])
    sql = "delete from {0} where {1}".format(tbl, whrs)
    return sql

def querycount(tbl,where):
    whrs=" and ".join([ k+"='"+str(v)+"'" for k,v in where.__dict__.items()])
    rs =QueryObj( "select count(*) as count from {0} where {1}".format(tbl, whrs) )
    return rs[0].count


def verifyface(user):
    if user.face == "":
        if user.sex == "1":
            user.face = "img/face_default_male.png"
        elif user.sex == "0":
            user.face = "img/face_default_female.png"
        else:
            user.face = "img/face_default.png"
