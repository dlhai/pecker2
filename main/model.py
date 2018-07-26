#encoding:utf-8
from main.tools import *
from sqlalchemy import *
from flask import Response
import datetime

engine = create_engine('sqlite:///./db/pecker.db')
#engine.echo = True
metadata = MetaData(engine)
conn = engine.connect()

db_tbl = [
    { "id": "0", "name": "none", "title": "占位", },
    { "id": "1", "name": "base", "title": "定义", },
    { "id": "2", "name": "link", "title": "一对多引用", },
    { "id": "3", "name": "addit", "title": "附件", },
    { "id": "4", "name": "config", "title": "配置信息", },
    { "id": "5", "name": "admarea", "title": "行政区划", },
    { "id": "6", "name": "user", "title": "供应商", },
    { "id": "7", "name": "certif", "title": "人员", },
    { "id": "8", "name": "edu", "title": "证件信息", },
    { "id": "9", "name": "employ", "title": "受教育经历", },
    { "id": "10", "name": "opus", "title": "就业经历", },
    { "id": "11", "name": "vender", "title": "发表作品", },
    { "id": "12", "name": "wait", "title": "", },
    { "id": "13", "name": "winderco", "title": "风电企业", },
    { "id": "14", "name": "winderprov", "title": "省区", },
    { "id": "15", "name": "winder", "title": "风场", },
    { "id": "16", "name": "winderarea", "title": "风区", },
    { "id": "17", "name": "efan", "title": "风机", },
    { "id": "18", "name": "leaf", "title": "叶片", },
    { "id": "19", "name": "fault", "title": "报修", },
    { "id": "20", "name": "devwh", "title": "设备驻地", },
    { "id": "21", "name": "dev", "title": "设备", },
    { "id": "22", "name": "devwork", "title": "设备任务", },
    { "id": "23", "name": "matprov", "title": "仓库省区", },
    { "id": "24", "name": "matwh", "title": "仓库", },
    { "id": "25", "name": "mat", "title": "材料", },
    { "id": "26", "name": "matin", "title": "入库单", },
    { "id": "27", "name": "matinrec", "title": "入库记录", },
    { "id": "28", "name": "matout", "title": "出库单", },
    { "id": "29", "name": "matoutrec", "title": "出库记录", },
    { "id": "30", "name": "chat", "title": "聊天记录", },
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
            user.subs = QueryObj( "select id, name from winderarea where winder_id="+str(user.depart_id))
    user.idols = list(map( lambda x:x.idol_id,QueryObj( "select idol_id from follow where fans_id="+str(user.id))))
    getjob(user.job)["mark"].update(user)
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

def towhere(where):
    r = " and ".join([ k+"='"+str(v)+"'" for k,v in todict(where).items()])
    r =r.replace("='(", " in (")
    r =r.replace(")'", ")")
    return r

def toinsert(tbl,obj):
    if type(obj) == type([]):
        if len(obj)== 0:
            return ""
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

def insert(tbl,obj):
    sql=toinsert(tbl,obj)
    conn.execute(sql) if sql != "" else 0
def insertq(tbl,obj):
    sql=toinsert(tbl,obj)
    conn.execute(toinsert(tbl,obj)) if sql != "" else 0
    return QueryObj("select * from "+tbl+" where id in (select max(id) from "+tbl+")")
def delete(tbl,obj):
    conn.execute(todelete(tbl,obj))
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

class mark_type:
    checkdt=0
    annual=1
    expired=2
    lowstock=3
    urgepay=4
    def check(owner_id):
        now = datetime.datetime.now()
        rs = QueryObj('''select whn from mark where type="{0}" and owner_id={1}'''.format(mark_type.checkdt,owner_id))
        if len(rs):
            if rs[0].whn[0:10] == now.strftime("%Y-%m-%d"):
                return False
        insert("mark",obj(type=mark_type.checkdt, owner_id=owner_id, whn=now))
        return True

class mark_default:
    def update(user):
        pass
    def query(user):
        pass
    def read(user):
        pass

class mark_驻地长:
    def update(user):
        if not mark_type.check(user.id):
            return
        now = datetime.datetime.now()
        delete("mark", obj(type=mark_type.annual,owner_id=user.id))
        ar = QueryObj("select id from dev where checkdate between date('now','-30 day') and date('now')")
        insert("mark",[obj(type=mark_type.annual, obj_id=x.id, owner_id=user.id, whn=now) for x in ar ])
    def query(user):
        return querycount( "mark", obj(type=mark_type.annual, owner_id=user.id))
    def read(obj_id):
        delete("mark", obj(type=mark_type.annual, obj_id=obj_id)) #不设置owner_id，这样其他人的也可以删掉
        
class mark_司机:
    def update(user):
        if not mark_type.check(user.id):
            return
        now = datetime.datetime.now()
        delete("mark", obj(type=mark_type.annual,owner_id=user.id))
        ar = QueryObj("select id from dev where checkdate between date('now','-30 day') and date('now') and driver_id={0}".format(user.id))
        insert("mark",[obj(type=mark_type.annual, obj_id=x.id, owner_id=user.id, whn=now) for x in ar ])
    def query(user):
        return querycount( "mark", obj(type=mark_type.annual, owner_id=user.id))
    def read(obj_id):
        delete("mark", obj(type=mark_type.annual, obj_id=obj_id))#不设置owner_id，这样其他人的也可以删掉

class mark_仓库长:
    def update(user):
        if not mark_type.check(user.depart_id):
            return
        now = datetime.datetime.now()
        rec="matinrec left join ( select matinrec_id, sum(num) as numout from matout,matoutrec where matout.id=matoutrec.matout_id and matout.status >=3 group by matinrec_id) as rec on matinrec.id=matinrec_id"

        delete("mark", obj(type=mark_type.expired,owner_id=user.depart_id))
        sql="select matinrec.id, mat_id, alarm, matinrec.num as numin,rec.numout,expiredt from mat,matin, {0} where matinrec.matin_id=matin.id and matinrec.mat_id=mat.id and matin.status >=3 and matin.matwh_id={1}"
        ar = QueryObj(sql.format(rec,user.depart_id))
        def checkexpired(rec, days):#days是提前的天数
            nonlocal now
            return atoi(rec.numin)>atoi(rec.numout) and (datetime.datetime.strptime(rec.expiredt[0:10],"%Y-%m-%d") - datetime.timedelta(days=days)) > now
        aaa=[]
        for x in ar:
            if checkexpired(x, 30):
                aaa.append(obj(type=mark_type.expired, obj_id=x.id,owner_id=user.depart_id))
        insert("mark",[obj(type=mark_type.expired, obj_id=x.id,owner_id=user.depart_id) for x in ar if checkexpired(x, 30) ])

        delete("mark", obj(type=mark_type.lowstock,owner_id=user.depart_id))
        sql="select mat_id, sum(matinrec.num) as allin,sum(rec.numout) as allout from matin, {0} where matinrec.matin_id=matin.id and matin.matwh_id={1} and matin.status >=3 group by mat_id"
        ar = QueryObj(sql.format(rec,user.depart_id))
        lows= QueryObj("select b_id as mat_id,remark as line from link where type='low' and a_id="+str(user.depart_id))
        def checklow(rec,lows):
            for x in lows:
                if rec.mat_id == x.mat_id:
                    if rec.allin-rec.allout < x.line:
                        return True
            return False
        insert("mark",[obj(type=mark_type.lowstock, obj_id=x.id,owner_id=user.depart_id) for x in ar if checklow(x, lows) ])
    def query(user):
        count = querycount( "mark", obj(type=mark_type.expired, owner_id=user.depart_id))
        count += querycount( "mark", obj(type=mark_type.lowstock, owner_id=user.depart_id))
        return count
    def read(obj_id,type):
        if type=="expired":
            delete("mark", obj(type=mark_type.expired, obj_id=obj_id))
        else:
            delete("mark", obj(type=mark_type.lowstock, obj_id=obj_id))

class mark_仓管(mark_仓库长):#内容一样
    pass

class mark_调度长:
    def update(user):
        if not mark_type.check(user.id):
            return
        now = datetime.datetime.now()
        delete("mark", obj(type=mark_type.urgepay,owner_id=user.id))
        sql="select id from fault where status=6 and finish_dt between date('now','-10 year') and date('now','-60 day')"
        ar = QueryObj(sql)
        insert("mark",[obj(type=mark_type.urgepay, obj_id=x.id, owner_id=user.id, whn=now) for x in ar ])
    def query(user):
        return querycount( "mark", obj(type=mark_type.urgepay, owner_id=user.id))
    def read(obj_id):
        delete("mark", obj(type=mark_type.urgepay, obj_id=obj_id)) #不设置owner_id，这样其他人的也可以删掉

class mark_调度:
    def update(user):
        if not mark_type.check(user.id):
            return
        now = datetime.datetime.now()
        delete("mark", obj(type=mark_type.urgepay,owner_id=user.id))
        sql="select id from fault where status=6 and finish_dt between date('now','-10 year') and date('now','-60 day')"
        sql+="and ( guide_id={0} or fault.id in (select a_id from link where type=chatman and b_id={0}))" #与调度长区别仅此一行
        ar = QueryObj(sql)
        insert("mark",[obj(type=mark_type.urgepay, obj_id=x.id, owner_id=user.id, whn=now) for x in ar ])
    def query(user):
        return querycount( "mark", obj(type=mark_type.urgepay, owner_id=user.id))
    def read(obj_id):
        delete("mark", obj(type=mark_type.urgepay, obj_id=obj_id)) #不设置owner_id，这样其他人的也可以删掉

db_job = [
    {"id":"1","sname":"su叶片","name":"叶片超级帐号","su":"","mark":mark_default},
    {"id":"2","sname":"风场长","name":"风场主管","su":"1","mark":mark_default},
    {"id":"3","sname":"驻场","name":"驻场","su":"1","mark":mark_default},
    {"id":"4","sname":"su设备","name":"设备超级帐号","su":"","mark":mark_default},
    {"id":"5","sname":"驻地长","name":"驻地主管","su":"4","mark":mark_驻地长},
    {"id":"6","sname":"司机","name":"设备司机","su":"4","mark":mark_司机},
    {"id":"7","sname":"su仓库","name":"仓库超级帐号","su":"","mark":mark_default},
    {"id":"8","sname":"仓库长","name":"仓库主管","su":"7","mark":mark_仓库长},
    {"id":"9","sname":"仓管","name":"仓库管理员","su":"7","mark":mark_仓管},
    {"id":"10","sname":"su调度","name":"调度超级帐号","su":"","mark":mark_default},
    {"id":"11","sname":"调度长","name":"调度主管","su":"10","mark":mark_调度长},
    {"id":"12","sname":"调度","name":"调度","su":"10","mark":mark_调度},
    {"id":"13","sname":"su专家","name":"专家超级帐号","su":"","mark":mark_default},
    {"id":"14","sname":"专家","name":"专家","su":"13","mark":mark_default},
    {"id":"15","sname":"su技工","name":"技工超级帐号","su":"","mark":mark_default},
    {"id":"16","sname":"队长","name":"维修队长","su":"15","mark":mark_default},
    {"id":"17","sname":"技工","name":"技工","su":"15","mark":mark_default},
    {"id":"18","sname":"su博客","name":"博客超级帐号","su":"","mark":mark_default},
    {"id":"19","sname":"公众","name":"公众","su":"18","mark":mark_default},
]

def getjob(id):
    return list(filter(lambda x: x["id"]==str(id), db_job))[0]

