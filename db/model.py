#encoding:utf8
from sqlalchemy import *
from vdgt import *
from buildarea import dobj,rndarea
import time

setdata(loadpkl('rawdata.pkl'))
prov=loadpkl('areadata.pkl')

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

tbl_user=Table('user', metadata,
	Column('id',Integer,primary_key=True),
	Column('account',String(32)),
	Column('pwd',String(32)),
	Column('face',String(32)),
	Column('depart_id',Integer),
	Column('depart_table',String(16)),
	Column('job',String(16)),
	Column('skill',String(64)),
	Column('name',String(32)),
	Column('idc',String(32)),
	Column('sex',String(8)),
	Column('ethnic',String(16)),
	Column('birth',String(16)),
	Column('origin',String(64)),
	Column('idimg',String(64)),
	Column('phone',String(32)),
	Column('qq',String(32)),
	Column('mail',String(32)),
	Column('wechat',String(32)),
	Column('addr',String(64)))

tbl_leafvender=Table('leafvender', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(32)),
	Column('fname',String(64)),
	Column('atten',String(32)),
	Column('tel',String(32)),
	Column('leader',String(32)),
	Column('fax',String(32)),
	Column('addr',String(128)))

tbl_efanvender=Table('efanvender', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(32)),
	Column('fname',String(64)),
	Column('atten',String(32)),
	Column('tel',String(32)),
	Column('leader',String(32)),
	Column('fax',String(32)),
	Column('addr',String(128)))

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
	Column('efanvender_id',Integer,ForeignKey('efanvender.id')),
	Column('position',String(64)))

tbl_leaf=Table('leaf', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(32)),
	Column('winderarea_id',Integer,ForeignKey('winderarea.id')),
	Column('winder_id',Integer,ForeignKey('winder.id')),
	Column('efan_id',Integer,ForeignKey('efan.id')),
	Column('leafvender_id',Integer,ForeignKey('leafvender.id')),
	Column('mat',String(32)),
	Column('producedate',Date),
	Column('putondate',Date))


metadata.create_all(engine)
conn = engine.connect()

def QueryAll(tbl):
    r=obj()
    r.name=tbl.name
    r.field=[f.name for f in tbl.columns]
    r.data=conn.execute(select([tbl])).fetchall()
    addtbl(r)

def dict_base():
    x=""
    return dict(table=x,title=x,name=x,forder=x,ftype=x,twidth=x,tstyle=x,dtype=x,drule=x,remark=x)

def dict_user(depart_id,depart_table,job,skill):
    person=rnditem("_person")
    mail=rndmail(person)
    return dict(account=person.pinyin,pwd=person.pinyin,face=rnditem("_faceimage"),depart_id=depart_id,depart_table=depart_table,job=job,skill=skill,name=person.name,idc=person.id,sex=id2sex(person.id),ethnic=rnditem("_ethnic"),birth=id2birth(person.id),origin=person.origin,idimg=rndaddition("身份证"),phone=str(int(person.phone)),qq=str(int(person.qq)),mail=mail,wechat=rndwechat(person,mail),addr=rnditem("_麦当劳门店").门店地址)

def dict_leafvender(x):
    p1=rnditem("_person")
    p2=rnditem("_station")
    return dict(name=x.name,fname=x.fname,atten=p1.name,tel=str(int(p1.phone)),leader=p2.name,fax=p2.phone,addr=p1.origin)
conn.execute(tbl_leafvender.insert(),[dict_leafvender(x) for x in data("_leaf_vender")])
QueryAll(tbl_leafvender)

def dict_efanvender(x):
    p1=rnditem("_person")
    p2=rnditem("_station")
    return dict(name=x.name,fname=x.fname,atten=p1.name,tel=str(int(p1.phone)),leader=p2.name,fax=p2.phone,addr=p1.origin)
conn.execute(tbl_efanvender.insert(),[dict_efanvender(x) for x in data("_efan_vender")])
QueryAll(tbl_efanvender)

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
conn.execute(tbl_winderarea.insert(),[dict_winderarea(x,y) for y in data("winder") for x in rndarea(prov[getitem("winderprov",id=y.winderprov_id).name][y.name[:-2]],2,5)])
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

conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","叶片超级帐号","")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"winder","风场主管","") for x in data("winder")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"winder","驻场","") for x in data("winder") for y in range(rndnum(2,3))])
conn.execute(tbl_base.insert(),[dict(table="base",title="标识",name="id",forder="",ftype="",twidth="",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="base",title="表名",name="table",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="",),
dict(table="base",title="标题",name="title",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="",),
dict(table="base",title="字段名",name="name",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="",),
dict(table="base",title="表单序号",name="forder",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="",),
dict(table="base",title="表单显示类型",name="ftype",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="div input input_long textarea select",),
dict(table="base",title="表格宽度",name="twidth",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="",),
dict(table="base",title="表格风格",name="tstyle",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="",),
dict(table="base",title="类型",name="dtype",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="",),
dict(table="base",title="生成规则",name="drule",forder="",ftype="",twidth="",tstyle="",dtype="String(64)",drule="x",remark="",),
dict(table="base",title="说明",name="remark",forder="",ftype="bigtext",twidth="",tstyle="",dtype="String(2048)",drule="x",remark="",),
dict(table="user",title="标识",name="id",forder="",ftype="",twidth="0.0",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="user",title="帐号",name="account",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(32)",drule="person.pinyin",remark="",),
dict(table="user",title="密码",name="pwd",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(32)",drule="person.pinyin",remark="",),
dict(table="user",title="头像",name="face",forder="",ftype="image",twidth="0.0",tstyle="",dtype="String(32)",drule="rnditem:_faceimage",remark="",),
dict(table="user",title="所在单位",name="depart_id",forder="",ftype="",twidth="",tstyle="",dtype="Integer",drule="depart_id",remark="",),
dict(table="user",title="单位表名",name="depart_table",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(16)",drule="depart_table",remark="",),
dict(table="user",title="职位",name="job",forder="",ftype="",twidth="",tstyle="",dtype="String(16)",drule="job",remark="专家、队长、技工、驻场、风场主管、调度、调度主管、仓管、仓管主管、设备司机、设备主管、公众",),
dict(table="user",title="领域",name="skill",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(64)",drule="skill",remark="避雷、工艺设计、工艺生产、材料、安全",),
dict(table="user",title="姓名",name="name",forder="",ftype="",twidth="",tstyle="",dtype="String(32)",drule="person.name",remark="",),
dict(table="user",title="身份证号",name="idc",forder="",ftype="",twidth="",tstyle="",dtype="String(32)",drule="person.id",remark="",),
dict(table="user",title="性别",name="sex",forder="",ftype="",twidth="",tstyle="",dtype="String(8)",drule="id2sex(person.id)",remark="身份证住址信息",),
dict(table="user",title="民族",name="ethnic",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(16)",drule="rnditem:_ethnic",remark="",),
dict(table="user",title="出生年月",name="birth",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(16)",drule="id2birth(person.id)",remark="",),
dict(table="user",title="籍贯",name="origin",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(64)",drule="person.origin",remark="",),
dict(table="user",title="身份证扫描件",name="idimg",forder="",ftype="image",twidth="0.0",tstyle="",dtype="String(64)",drule='rndaddition("身份证")',remark="",),
dict(table="user",title="联系电话",name="phone",forder="",ftype="",twidth="",tstyle="",dtype="String(32)",drule="str(int(person.phone))",remark="",),
dict(table="user",title="QQ号码",name="qq",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(32)",drule="str(int(person.qq))",remark="",),
dict(table="user",title="邮箱",name="mail",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(32)",drule="mail",remark="",),
dict(table="user",title="微信号",name="wechat",forder="",ftype="",twidth="0.0",tstyle="",dtype="String(32)",drule="rndwechat(person,mail)",remark="",),
dict(table="user",title="联系地址",name="addr",forder="",ftype="text",twidth="",tstyle="",dtype="String(64)",drule="rnditem:_麦当劳门店:门店地址",remark="当前实际居住地址",),
dict(table="leafvender",title="标识",name="id",forder="-1.0",ftype="div",twidth="15.0",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="leafvender",title="名称",name="name",forder="0.0",ftype="input",twidth="60.0",tstyle="",dtype="String(32)",drule="x.name",remark="",),
dict(table="leafvender",title="完整名称",name="fname",forder="1.0",ftype="input",twidth="120.0",tstyle="",dtype="String(64)",drule="x.fname",remark="",),
dict(table="leafvender",title="联系人",name="atten",forder="3.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="p1.name",remark="",),
dict(table="leafvender",title="电话",name="tel",forder="4.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="str(int(p1.phone))",remark="",),
dict(table="leafvender",title="主要负责人",name="leader",forder="5.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="p2.name",remark="",),
dict(table="leafvender",title="传真",name="fax",forder="6.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="p2.phone",remark="",),
dict(table="leafvender",title="地址",name="addr",forder="2.0",ftype="input_long",twidth="",tstyle="",dtype="String(128)",drule="p1.origin",remark="",),
dict(table="efanvender",title="标识",name="id",forder="-1.0",ftype="div",twidth="15.0",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="efanvender",title="名称",name="name",forder="0.0",ftype="input",twidth="60.0",tstyle="",dtype="String(32)",drule="x.name",remark="",),
dict(table="efanvender",title="完整名称",name="fname",forder="1.0",ftype="input",twidth="120.0",tstyle="",dtype="String(64)",drule="x.fname",remark="",),
dict(table="efanvender",title="联系人",name="atten",forder="3.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="p1.name",remark="",),
dict(table="efanvender",title="电话",name="tel",forder="4.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="str(int(p1.phone))",remark="",),
dict(table="efanvender",title="主要负责人",name="leader",forder="5.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="p2.name",remark="",),
dict(table="efanvender",title="传真",name="fax",forder="6.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="p2.phone",remark="",),
dict(table="efanvender",title="地址",name="addr",forder="2.0",ftype="input_long",twidth="",tstyle="",dtype="String(128)",drule="p1.origin",remark="",),
dict(table="winderco",title="标识",name="id",forder="-1.0",ftype="div",twidth="15.0",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="winderco",title="名称",name="name",forder="0.0",ftype="input",twidth="60.0",tstyle="",dtype="String(64),unique=True",drule="x.name",remark="",),
dict(table="winderco",title="备注",name="remark",forder="1.0",ftype="textarea",twidth="",tstyle="",dtype="String(2048)",drule="rnditem:_songci",remark="",),
dict(table="winderprov",title="标识",name="id",forder="-1.0",ftype="div",twidth="",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="winderprov",title="所属企业",name="winderco_id",forder="0.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('winderco.id')",drule="x.id",remark="",),
dict(table="winderprov",title="名称",name="name",forder="1.0",ftype="input",twidth="",tstyle="",dtype="String(64)",drule="y.name",remark="",),
dict(table="winderprov",title="备注",name="remark",forder="2.0",ftype="textarea",twidth="",tstyle="",dtype="String(2048)",drule="rnditem:_songci",remark="",),
dict(table="winder",title="标识",name="id",forder="-1.0",ftype="div",twidth="",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="winder",title="所属省区",name="winderprov_id",forder="0.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('winderprov.id')",drule="y.id",remark="",),
dict(table="winder",title="所属企业",name="winderco_id",forder="1.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('winderco.id')",drule="y.winderco_id",remark="",),
dict(table="winder",title="名称",name="name",forder="2.0",ftype="input",twidth="",tstyle="",dtype="String(64)",drule='x.name+"风场"',remark="",),
dict(table="winder",title="规模",name="scale",forder="3.0",ftype="input",twidth="",tstyle="",dtype="String(16)",drule="rnditem:_scale",remark="",),
dict(table="winder",title="位置",name="position",forder="4.0",ftype="input",twidth="",tstyle="",dtype="String(64)",drule='str(x.lng)+" "+str(x.lat)',remark="",),
dict(table="winder",title="传真",name="fax",forder="5.0",ftype="input",twidth="",tstyle="",dtype="String(16)",drule="rnditem:_station:phone",remark="",),
dict(table="winder",title="地址",name="addr",forder="6.0",ftype="input_long",twidth="",tstyle="",dtype="String(64)",drule="rnditem:_person:origin",remark="",),
dict(table="winder",title="自然状况",name="natural",forder="7.0",ftype="textarea",twidth="",tstyle="",dtype="String(2048)",drule="rnditem:_songci",remark="例如风力、风沙、冰冻、温湿度、腐蚀、海拔等描述。也可能包括沙漠、山地、草原等地貌信息。",),
dict(table="winder",title="备注",name="remark",forder="8.0",ftype="textarea",twidth="",tstyle="",dtype="String(2048)",drule="rnditem:_songci",remark="",),
dict(table="winderarea",title="标识",name="id",forder="-1.0",ftype="div",twidth="",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="winderarea",title="所属风场",name="winder_id",forder="0.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('winder.id')",drule="y.id",remark="",),
dict(table="winderarea",title="名称",name="name",forder="1.0",ftype="input",twidth="",tstyle="",dtype="String(64)",drule='x.name+"风区"',remark="",),
dict(table="winderarea",title="备注",name="remark",forder="2.0",ftype="textarea",twidth="",tstyle="",dtype="String(2048)",drule="rnditem:_songci",remark="",),
dict(table="winderarea",title="位置",name="position",forder="3.0",ftype="textarea",twidth="",tstyle="",dtype="String(64)",drule="rndgpsarea(y.position,0.3,0.27)",remark="",),
dict(table="efan",title="标识",name="id",forder="-1.0",ftype="div",twidth="",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="efan",title="所属风区",name="winderarea_id",forder="0.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('winderarea.id')",drule="x.id",remark="风场一般分多个区域管理，例如1区、2区、3区等。",),
dict(table="efan",title="所属风场",name="winder_id",forder="1.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('winder.id')",drule="x.winder_id",remark="",),
dict(table="efan",title="编号",name="code",forder="2.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="rndqq()",remark="借用一下QQ号生成函数",),
dict(table="efan",title="型号",name="type",forder="3.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule='rndtype("efan")',remark="",),
dict(table="efan",title="生产厂家",name="efanvender_id",forder="4.0",ftype="select",twidth="",tstyle="",dtype="Integer,ForeignKey('efanvender.id')",drule="rnditem:efanvender:id",remark="",),
dict(table="efan",title="位置",name="position",forder="5.0",ftype="input",twidth="",tstyle="",dtype="String(64)",drule="rndgps(x.position)",remark="",),
dict(table="leaf",title="标识",name="id",forder="-1.0",ftype="div",twidth="",tstyle="",dtype="Integer,primary_key=True",drule="",remark="",),
dict(table="leaf",title="编号",name="code",forder="0.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="x.code+a[y]",remark="",),
dict(table="leaf",title="所属风区",name="winderarea_id",forder="1.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('winderarea.id')",drule="x.winderarea_id",remark="",),
dict(table="leaf",title="所属风场",name="winder_id",forder="2.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('winder.id')",drule="x.winder_id",remark="",),
dict(table="leaf",title="所属风机",name="efan_id",forder="3.0",ftype="div",twidth="",tstyle="",dtype="Integer,ForeignKey('efan.id')",drule="x.id",remark="",),
dict(table="leaf",title="生产厂家",name="leafvender_id",forder="4.0",ftype="select",twidth="",tstyle="",dtype="Integer,ForeignKey('leafvender.id')",drule="rnditem:leafvender:id",remark="",),
dict(table="leaf",title="主要材料",name="mat",forder="5.0",ftype="input",twidth="",tstyle="",dtype="String(32)",drule="rnditem:_mainmat",remark="",),
dict(table="leaf",title="出厂时间",name="producedate",forder="6.0",ftype="date",twidth="",tstyle="",dtype="Date",drule="pdt",remark="",),
dict(table="leaf",title="挂机时间",name="putondate",forder="7.0",ftype="date",twidth="",tstyle="",dtype="Date",drule="rnddatespan(pdt,30,365)",remark="",),
])