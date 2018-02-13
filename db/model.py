#encoding:utf8
from sqlalchemy import *
from vdgt import *
from buildarea import dobj,rndarea
import time,os

setdata(loadpkl('rawdata.pkl'))
prov=loadpkl('areadata.pkl')

if os.path.isfile('./pecker.db'):
    os.remove('./pecker.db')
engine = create_engine('sqlite:///./pecker.db')
engine.echo = True
metadata = MetaData(engine)

tbl_base=Table('base', metadata,
	Column('id',Integer,primary_key=True),
	Column('table',String(64)),
	Column('title',String(64)),
	Column('name',String(64)),
	Column('forder',String(64)),
	Column('ftype',String(64)),
	Column('twidth',String(64)),
	Column('tstyle',String(64)),
	Column('dtype',String(64)),
	Column('drule',String(64)),
	Column('remark',String(2048)))

tbl_link=Table('link', metadata,
	Column('id',Integer,primary_key=True),
	Column('a_field',String(32)),
	Column('a_id',Integer),
	Column('b_field',String(32)),
	Column('b_id',Integer),
	Column('name',String(32)))

tbl_addit=Table('addit', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(64)),
	Column('table',String(32)),
	Column('field',Integer),
	Column('remark',String(32)),
	Column('user',Integer),
	Column('date',Date))

tbl_config=Table('config', metadata,
	Column('id',Integer,primary_key=True),
	Column('type',String(32)),
	Column('name',String(32)))

tbl_admarea=Table('admarea', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(16)),
	Column('name',String(32)),
	Column('parent',String(16)),
	Column('sname',String(16)),
	Column('lng',Float),
	Column('lat',Float),
	Column('grade',Integer))

tbl_vender=Table('vender', metadata,
	Column('id',Integer,primary_key=True),
	Column('type',Integer),
	Column('name',String(32)),
	Column('fname',String(64)),
	Column('atten',String(32)),
	Column('tel',String(32)),
	Column('leader',String(32)),
	Column('fax',String(32)),
	Column('addr',String(128)))

tbl_user=Table('user', metadata,
	Column('id',Integer,primary_key=True),
	Column('account',String(32)),
	Column('pwd',String(32)),
	Column('face',String(32)),
	Column('depart_id',Integer),
	Column('depart_table',Integer),
	Column('job',Integer),
	Column('skill',String(64)),
	Column('name',String(32)),
	Column('code',String(32)),
	Column('sex',Integer),
	Column('ethnic',String(16)),
	Column('birth',String(16)),
	Column('origin',String(64)),
	Column('idimg',String(64)),
	Column('phone',String(32)),
	Column('qq',String(32)),
	Column('mail',String(32)),
	Column('wechat',String(32)),
	Column('addr',String(64)))

tbl_winderco=Table('winderco', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(64),unique=True),
	Column('remark',String(2048)))

tbl_winderprov=Table('winderprov', metadata,
	Column('id',Integer,primary_key=True),
	Column('winderco_id',Integer,ForeignKey('winderco.id')),
	Column('name',String(64)),
	Column('remark',String(2048)))

tbl_winder=Table('winder', metadata,
	Column('id',Integer,primary_key=True),
	Column('winderprov_id',Integer,ForeignKey('winderprov.id')),
	Column('winderco_id',Integer,ForeignKey('winderco.id')),
	Column('name',String(64)),
	Column('scale',String(16)),
	Column('position',String(64)),
	Column('fax',String(16)),
	Column('addr',String(64)),
	Column('natural',String(2048)),
	Column('remark',String(2048)))

tbl_winderarea=Table('winderarea', metadata,
	Column('id',Integer,primary_key=True),
	Column('winder_id',Integer,ForeignKey('winder.id')),
	Column('name',String(64)),
	Column('remark',String(2048)),
	Column('position',String(64)))

tbl_efan=Table('efan', metadata,
	Column('id',Integer,primary_key=True),
	Column('winderarea_id',Integer,ForeignKey('winderarea.id')),
	Column('winder_id',Integer,ForeignKey('winder.id')),
	Column('code',String(32)),
	Column('type',String(32)),
	Column('efanvender_id',Integer),
	Column('position',String(64)))

tbl_leaf=Table('leaf', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(32)),
	Column('winderarea_id',Integer,ForeignKey('winderarea.id')),
	Column('winder_id',Integer,ForeignKey('winder.id')),
	Column('efan_id',Integer,ForeignKey('efan.id')),
	Column('leafvender_id',Integer),
	Column('mat',String(32)),
	Column('producedate',Date),
	Column('putondate',Date))

tbl_fault=Table('fault', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(32)),
	Column('fault_id',String(32)),
	Column('report_id',Integer),
	Column('reporttime',Date),
	Column('phone',String(16)),
	Column('winder_id',Integer),
	Column('remark',String(2048)),
	Column('status',Integer),
	Column('guide_id',Integer),
	Column('guidetime',Date))

tbl_devwh=Table('devwh', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(32)),
	Column('fname',String(32)),
	Column('position',String(32)),
	Column('addr',String(2048)),
	Column('remark',String(128)))

tbl_dev=Table('dev', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(32)),
	Column('clss',Integer),
	Column('type',String(32)),
	Column('face',String(32)),
	Column('img',String(32)),
	Column('devwh_id',Integer),
	Column('position',String(32)),
	Column('status',Integer),
	Column('driver_id',Integer),
	Column('remark',String(2048)),
	Column('vender_id',Integer),
	Column('producedate',Date),
	Column('buydate',Date),
	Column('checkdate',Date))

tbl_devwork=Table('devwork', metadata,
	Column('id',Integer,primary_key=True),
	Column('status',Integer),
	Column('fault_id',Integer),
	Column('guide_id',Integer),
	Column('guidedt',Date),
	Column('clss',Integer),
	Column('devwh_id',Integer),
	Column('timelen',Integer),
	Column('winder_id',Integer),
	Column('addr',String(128)),
	Column('remark',String(2048)),
	Column('deal_id',Integer),
	Column('dealdt',Date),
	Column('dev_id',Integer),
	Column('driver_id',Integer))

tbl_matprov=Table('matprov', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(64)),
	Column('remark',String(2048)))

tbl_matwh=Table('matwh', metadata,
	Column('id',Integer,primary_key=True),
	Column('matprov_id',Integer,ForeignKey('winderprov.id')),
	Column('name',String(16)),
	Column('position',String(64)),
	Column('addr',String(64)),
	Column('scale',String(16)),
	Column('base',String(64)),
	Column('manager',String(16)),
	Column('clerks',String(64)),
	Column('remark',String(2048)))

tbl_mat=Table('mat', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(16)),
	Column('name',String(32)),
	Column('type',String(16)),
	Column('unit',String(16)),
	Column('alarm',Integer),
	Column('essential',Integer),
	Column('matbase',Integer),
	Column('remark',String(2048)))


metadata.create_all(engine)
conn = engine.connect()

def QueryAll(tbl):
    data=conn.execute(select([tbl])).fetchall()
    adddata(tbl.name,data)

def QueryData(name,tbl,field,value):
    q = select([tbl]).where(tbl.c[field]==value)
    data=conn.execute(q).fetchall()
    adddata(name,data)

def dict_base(x):
    return dict(table=x.table,title=x.title,name=x.name,forder=x.forder,ftype=x.ftype,twidth=x.twidth,tstyle=x.tstyle,dtype=x.dtype,drule=x.drule,remark=x.remark)
conn.execute(tbl_base.insert(),[dict_base(x) for x in data("_fields")])

def dict_link(x,y):
    return dict(a_field="",a_id="",b_field="",b_id="",name="")

def dict_addit(x,y):
    return dict(name="",table="",field="",remark="",user="",date="")

def dict_config(type,name):
    return dict(type=type,name=name)

def dict_admarea(x):
    return dict(code=x.编号,name=x.名称,parent=x.父级,sname=x.简称,lng=x.经度,lat=x.纬度,grade=x.等级)
conn.execute(tbl_admarea.insert(),[dict_admarea(x) for x in data("_全国行政区编号")])

def dict_vender(x,type):
    p1=rnditem("_person")
    p2=rnditem("_station")
    return dict(type=type,name=x.name,fname=x.fname,atten=p1.name,tel=str(int(p1.phone)),leader=p1.name,fax=p2.phone,addr=p1.origin)

def dict_user(depart_id,depart_table,job,skill):
    person=rnditem("_person")
    mail=rndmail(person)
    return dict(account=person.pinyin,pwd=person.pinyin,face=rnditem("_faceimage"),depart_id=depart_id,depart_table=str(int(getitembyname("_tbl",depart_table).id)),job=job,skill=skill,name=person.name,code=person.id,sex=id2sex(person.id),ethnic=rnditem("_ethnic"),birth=id2birth(person.id),origin=person.origin,idimg=rndaddition("身份证"),phone=str(int(person.phone)),qq=str(int(person.qq)),mail=mail,wechat=rndwechat(person,mail),addr=rnditem("_麦当劳门店").门店地址)

conn.execute(tbl_vender.insert(),[dict_vender(x,17) for x in data("_efan_vender")])
conn.execute(tbl_vender.insert(),[dict_vender(x,18) for x in data("_leaf_vender")])
QueryData("efanvender",tbl_vender,"type",17)
QueryData("leafvender",tbl_vender,"type",18)
def dict_winderco(x):
    return dict(name=x.name,remark=rnditem("_songci"))
conn.execute(tbl_winderco.insert(),[dict_winderco(x) for x in data("_winderco")])
QueryAll(tbl_winderco)

def dict_winderprov(x,y):
    return dict(winderco_id=x.id,name=y.name,remark=rnditem("_songci"))
conn.execute(tbl_winderprov.insert(),[dict_winderprov(x,y) for x in data("winderco") for y in rndarea(prov,3,6)])
QueryAll(tbl_winderprov)

def dict_winder(x,y):
    return dict(winderprov_id=y.id,winderco_id=y.winderco_id,name=x.name+"风场",scale=rnditem("_scale"),position=str(x.lng)+" "+str(x.lat),fax=rnditem("_station").phone,addr=rnditem("_person").origin,natural=rnditem("_songci"),remark=rnditem("_songci"))
conn.execute(tbl_winder.insert(),[dict_winder(x,y) for y in data("winderprov") for x in rndarea(prov[y.name],3,6)])
QueryAll(tbl_winder)

def dict_winderarea(x,y):
    return dict(winder_id=y.id,name=x.name+"风区",remark=rnditem("_songci"),position=rndgpsarea(y.position,0.3,0.27))
conn.execute(tbl_winderarea.insert(),[dict_winderarea(x,y) for y in data("winder") for x in rndarea(prov[getitem("winderprov",y.winderprov_id).name][y.name[:-2]],2,5)])
QueryAll(tbl_winderarea)

def dict_efan(x,y):
    return dict(winderarea_id=x.id,winder_id=x.winder_id,code=rndqq(),type=rndtype("efan"),efanvender_id=rnditem("efanvender").id,position=rndgps(x.position))
conn.execute(tbl_efan.insert(),[dict_efan(x,y) for x in data("winderarea") for y in range(rndnum(30,50))])
QueryAll(tbl_efan)

def dict_leaf(x,y):
    pdt=rnddate(4*365,5*365)
    a="abc"
    return dict(code=x.code+a[y],winderarea_id=x.winderarea_id,winder_id=x.winder_id,efan_id=x.id,leafvender_id=rnditem("leafvender").id,mat=rnditem("_mainmat"),producedate=pdt,putondate=rnddatespan(pdt,30,365))
conn.execute(tbl_leaf.insert(),[dict_leaf(x,y) for x in data("efan") for y in range(3)])
QueryAll(tbl_leaf)

def dict_fault(report):
    return dict(code=rndqq(),fault_id=random.choice( ["风化脱漆","叶片断裂", "电机起火", "电路故障"]),report_id=report.id,reporttime=rnddate(30,60),phone=report.phone,winder_id=report.depart_id,remark=rnditem("_songci"),status="0",guide_id="0",guidetime=rnddate(1,1))

conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","1","")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"winder","2","") for x in data("winder")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"winder","3","") for x in data("winder") for y in range(rndnum(2,3))])
conn.execute(tbl_config.insert(),[dict_config("ethnic",x[0]) for x in data("_ethnic").data])
conn.execute(tbl_vender.insert(),[dict_vender(x,21) for x in data("_dev_vender")])
QueryData("devvender",tbl_vender,"type",21)
def dict_devwh(x):
    return dict(name=x.name,fname=x.fname,position=x.position,addr=x.addr,remark=x.remark)
conn.execute(tbl_devwh.insert(),[dict_devwh(x) for x in data("_devwh")])
QueryAll(tbl_devwh)

def dict_dev(x,y,z):
    dt=rnddate(4*365,5*365)
    person=rnditem("_person")
    return dict(code=rndtype("car"),clss=y.id,type=rnditem("_devtype"),face="img/"+y.name+".png",img=rnditem("_devimg"),devwh_id=x.id,position=rndgps(x.position),status="0",driver_id="0",remark=rnditem("_songci"),vender_id=rnditem("devvender").id,producedate=dt,buydate=rnddatespan(dt,30,365),checkdate=rnddatespan(dt,30,365))
conn.execute(tbl_dev.insert(),[dict_dev(x,y,z) for x in data("devwh") for y in data("_devclss") for z in range(rndnum(1,3))])
QueryAll(tbl_dev)

def dict_devwork():
    return dict(status="0",fault_id="0",guide_id="0",guidedt="0",clss="0",devwh_id="0",timelen="0",winder_id="0",addr="0",remark="0",deal_id="0",dealdt="0",dev_id="0",driver_id="0")

conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","4","")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"devwh","5","") for x in data("devwh")])
conn.execute(tbl_user.insert(),[dict_user(x.devwh_id,"devwh","6","") for x in data("dev")])
def dict_matprov(x):
    return dict(name=x.name,remark=rnditem("_songci"))
conn.execute(tbl_matprov.insert(),[dict_matprov(x) for x in rndarea(prov,3,6)])
QueryAll(tbl_matprov)

def dict_matwh(x,y):
    return dict(matprov_id=x.id,name=y.name+"仓库",position=str(y.lng)+" "+str(y.lat),addr=rnditem("_person").origin,scale=rnditem("_matwhscale").id,base=rndnum(1,10),manager=rnditem("_station").phone,clerks=rnditem("_person").origin,remark=rnditem("_songci"))
conn.execute(tbl_matwh.insert(),[dict_matwh(x,y) for x in data("matprov") for y in rndarea(prov[x.name],3,6)])
QueryAll(tbl_matwh)

def dict_mat(x):
    return dict(code=x.code,name=x.name,type=x.type,unit=x.unit,alarm=x.alarm,essential=rnditem("_essential").id,matbase=x.matbase,remark=x.remark)
conn.execute(tbl_mat.insert(),[dict_mat(x) for x in data("_mat")])
QueryAll(tbl_mat)

conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","7","")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"matwh","8","") for x in data("matwh")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"matwh","9","") for x in data("matwh") for y in range(rndnum(2,5))])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","10","")])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","11","")])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","12","") for x in range(rndnum(5,10))])

#为每个设备设置司机
data1=conn.execute("select id,devwh_id from dev").fetchall()
data2=conn.execute("select id,name,depart_id from user where job=6").fetchall()
if len(data1) == len(data2):
    ll = len(data1)
    for i in range(len(data1)):
        if data1[i].devwh_id != data2[i].depart_id:
            break;
        sql = "update dev set driver_id=" +str(data2[i].id)+ " where id="+ str(data1[i].id)
        conn.execute(sql)
