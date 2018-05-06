#encoding:utf8
from sqlalchemy import *
from random import *
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
def dict_base(x):
    return dict(table=x.table,title=x.title,name=x.name,forder=x.forder,ftype=x.ftype,twidth=x.twidth,tstyle=x.tstyle,dtype=x.dtype,drule=x.drule,remark=x.remark)

tbl_link=Table('link', metadata,
	Column('id',Integer,primary_key=True),
	Column('type',String(16)),
	Column('a_id',Integer),
	Column('b_id',Integer),
	Column('remark',String(32)),
	Column('date',Date))
def dict_link(x):
    return dict(type=x.type,a_id=x.a_id,b_id=x.b_id,remark=x.remark,date=x.date)

tbl_addit=Table('addit', metadata,
	Column('id',Integer,primary_key=True),
	Column('type',String(16)),
	Column('ref_id',Integer),
	Column('name',String(32)),
	Column('remark',String(32)),
	Column('user_id',Integer),
	Column('date',Date))
def dict_addit(x):
    return dict(type=x.type,ref_id=x.ref_id,name=x.name,remark=x.remark,user_id=x.user_id,date=x.date)

tbl_config=Table('config', metadata,
	Column('id',Integer,primary_key=True),
	Column('type',String(32)),
	Column('name',String(32)))
def dict_config(type,name):
    return dict(type=type,name=name)

tbl_admarea=Table('admarea', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(16)),
	Column('name',String(32)),
	Column('parent',String(16)),
	Column('sname',String(16)),
	Column('lng',Float),
	Column('lat',Float),
	Column('grade',Integer))
def dict_admarea(x):
    return dict(code=x.编号,name=x.名称,parent=x.父级,sname=x.简称,lng=x.经度,lat=x.纬度,grade=x.等级)

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
def dict_vender(x,type):
    p1=rnditem("_person")
    p2=rnditem("_station")
    return dict(type=type,name=x.name,fname=x.fname,atten=p1.name,tel=intstr(p1.phone),leader=p1.name,fax=p2.phone,addr=p1.origin)

tbl_flow=Table('flow', metadata,
	Column('id',Integer,primary_key=True),
	Column('table_id',Integer),
	Column('record_id',Integer),
	Column('status',Integer),
	Column('user_id',Integer),
	Column('date',Date),
	Column('remark',String(128)))
def dict_flow(x):
    return dict(table_id=x.table_id,record_id=x.record_id,status=x.status,user_id=x.user_id,date=rnddate(30,60),remark=x.remark)

tbl_msg=Table('msg', metadata,
	Column('id',Integer,primary_key=True),
	Column('type',Integer),
	Column('when',Integer),
	Column('frm',Integer),
	Column('to',Integer),
	Column('table_id',Integer),
	Column('row_id',Integer),
	Column('jsn',String(2048)),
	Column('say',String(2048)),
	Column('readtime',Date),
	Column('result',Integer))
def dict_msg(x):
    return dict(type="",when="",frm="",to="",table_id="",row_id="",jsn="",say="",readtime="",result="")

tbl_user=Table('user', metadata,
	Column('id',Integer,primary_key=True),
	Column('account',String(32),unique=True),
	Column('pwd',String(32)),
	Column('status',Integer,default=8),
	Column('face',String(32)),
	Column('depart_id',Integer),
	Column('depart_table',Integer),
	Column('job',Integer,default=18),
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
	Column('addr',String(64)),
	Column('yellow',Integer),
	Column('purple',Integer),
	Column('blue',Integer),
	Column('green',Integer))
def dict_user(depart_id,depart_table,job,skill):
    person=rnditem("_person")
    mail=rndmail(person)
    return dict(account=person.pinyin,pwd=person.pinyin,status=8.0,face=rnditem("_faceimage"),depart_id=depart_id,depart_table=intstr(getitembyname("_tbl",depart_table).id),job=job,skill=skill,name=person.name,code=person.id,sex=id2sex(person.id),ethnic=rnditem("_ethnic"),birth=id2birth(person.id),origin=person.origin,idimg=rndaddition("身份证"),phone=intstr(person.phone),qq=intstr(person.qq),mail=mail,wechat=rndwechat(person,mail),addr=rnditem("_麦当劳门店").门店地址,yellow=0.0,purple=0.0,blue=0.0,green=0.0)

tbl_certif=Table('certif', metadata,
	Column('id',Integer,primary_key=True),
	Column('user_id',Integer),
	Column('name',String(64)),
	Column('code',String(64)),
	Column('issue',String(64)),
	Column('issuedate',Date),
	Column('image',Integer))
def dict_certif():
    return dict(user_id="",name="",code="",issue="",issuedate="",image="")

tbl_edu=Table('edu', metadata,
	Column('id',Integer,primary_key=True),
	Column('user_id',Integer),
	Column('startdate',Date),
	Column('enddate',Date),
	Column('degree',String(16)),
	Column('issue',String(32)),
	Column('image1',Integer),
	Column('image2',Integer))
def dict_edu():
    return dict(user_id="",startdate="",enddate="",degree="",issue="",image1="",image2="")

tbl_employ=Table('employ', metadata,
	Column('id',Integer,primary_key=True),
	Column('user_id',Integer),
	Column('Organization',String(32)),
	Column('position',String(32)),
	Column('startdate',Date),
	Column('enddate',Date),
	Column('image',Integer))
def dict_employ():
    return dict(user_id="",Organization="",position="",startdate="",enddate="",image="")

tbl_opus=Table('opus', metadata,
	Column('id',Integer,primary_key=True),
	Column('opus_id',Integer),
	Column('board',Integer),
	Column('section',String(32)),
	Column('keyword',String(64)),
	Column('user_id',Integer),
	Column('date',Date),
	Column('title',String(64)),
	Column('body',String(10240)))
def dict_opus(x):
    return dict(opus_id=choice([0,randint(1,x) if x>1 else 0 ]),board=rndnum(1,3),section="",keyword=xsample("_keyword",3,5),user_id=rndnum(50,59),date=rnddate(0,2*365),title=rnditem("_quiz"),body=choice(data("_songci").data)[0])

tbl_follow=Table('follow', metadata,
	Column('id',Integer,primary_key=True),
	Column('fans_id',Integer),
	Column('idol_id',Integer),
	Column('date',Date))
def dict_follow(x,y):
    return dict(fans_id=x+50,idol_id=y+50,date=rnddate(0,2*365))

tbl_winderco=Table('winderco', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(64),unique=True),
	Column('remark',String(2048)))
def dict_winderco(x):
    return dict(name=x.name,remark=rnditem("_songci"))

tbl_winderprov=Table('winderprov', metadata,
	Column('id',Integer,primary_key=True),
	Column('winderco_id',Integer,ForeignKey('winderco.id')),
	Column('name',String(64)),
	Column('remark',String(2048)))
def dict_winderprov(x,y):
    return dict(winderco_id=x.id,name=y.name,remark=rnditem("_songci"))

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
def dict_winder(x,y):
    return dict(winderprov_id=y.id,winderco_id=y.winderco_id,name=x.name+"风场",scale=rnditem("_scale"),position=str(x.lng)+" "+str(x.lat),fax=rnditem("_station").phone,addr=rnditem("_person").origin,natural=rnditem("_songci"),remark=rnditem("_songci"))

tbl_winderarea=Table('winderarea', metadata,
	Column('id',Integer,primary_key=True),
	Column('winder_id',Integer,ForeignKey('winder.id')),
	Column('name',String(64)),
	Column('remark',String(2048)),
	Column('position',String(64)))
def dict_winderarea(x,y):
    return dict(winder_id=y.id,name=x.name+"风区",remark=rnditem("_songci"),position=rndgpsarea(y.position,0.3,0.27))

tbl_efan=Table('efan', metadata,
	Column('id',Integer,primary_key=True),
	Column('winderarea_id',Integer,ForeignKey('winderarea.id')),
	Column('winder_id',Integer,ForeignKey('winder.id')),
	Column('code',String(32)),
	Column('type',String(32)),
	Column('efanvender_id',Integer),
	Column('position',String(64)))
def dict_efan(x,y):
    return dict(winderarea_id=x.id,winder_id=x.winder_id,code=rndqq(),type=rndtype("efan"),efanvender_id=rnditem("efanvender").id,position=rndgps(x.position))

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
def dict_leaf(x,y):
    pdt=rnddate(4*365,5*365)
    a="abc"
    return dict(code=x.code+a[y],winderarea_id=x.winderarea_id,winder_id=x.winder_id,efan_id=x.id,leafvender_id=rnditem("leafvender").id,mat=rnditem("_mainmat"),producedate=pdt,putondate=rnddatespan(pdt,30,365))

tbl_fault=Table('fault', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(32)),
	Column('type',String(32)),
	Column('report_id',Integer),
	Column('reporttime',Date),
	Column('phone',String(16)),
	Column('winder_id',Integer),
	Column('remark',String(2048)),
	Column('status',Integer),
	Column('guide_id',Integer),
	Column('guidetime',Date))
def dict_fault(report):
    return dict(code=rndqq(),type=random.choice( ["风化脱漆","叶片断裂", "电机起火", "电路故障"]),report_id=report.id,reporttime=rnddate(30,60),phone=report.phone,winder_id=report.depart_id,remark=rnditem("_songci"),status="0",guide_id="0",guidetime=rnddate(1,1))

tbl_devwh=Table('devwh', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(32)),
	Column('fname',String(32)),
	Column('position',String(32)),
	Column('addr',String(2048)),
	Column('remark',String(128)))
def dict_devwh(x):
    return dict(name=x.name,fname=x.fname,position=x.position,addr=x.addr,remark=x.remark)

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
def dict_dev(x,y,z):
    dt=rnddate(4*365,5*365)
    person=rnditem("_person")
    return dict(code=rndtype("car"),clss=y.id,type=rnditem("_devtype"),face="img/"+y.name+".png",img=rnditem("_devimg"),devwh_id=x.id,position=rndgps(x.position),status="0",driver_id="0",remark=rnditem("_songci"),vender_id=rnditem("devvender").id,producedate=dt,buydate=rnddatespan(dt,30,365),checkdate=rnddatespan(dt,30,365))

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
def dict_devwork():
    return dict(status="0",fault_id="0",guide_id="0",guidedt="0",clss="0",devwh_id="0",timelen="0",winder_id="0",addr="0",remark="0",deal_id="0",dealdt="0",dev_id="0",driver_id="0")

tbl_matprov=Table('matprov', metadata,
	Column('id',Integer,primary_key=True),
	Column('name',String(64)),
	Column('remark',String(2048)))
def dict_matprov(x):
    return dict(name=x.name,remark=rnditem("_songci"))

tbl_matwh=Table('matwh', metadata,
	Column('id',Integer,primary_key=True),
	Column('matprov_id',Integer,ForeignKey('winderprov.id')),
	Column('name',String(16)),
	Column('scale',Integer),
	Column('base',Integer),
	Column('addr',String(64)),
	Column('position',String(64)),
	Column('remark',String(2048)))
def dict_matwh(x,y):
    return dict(matprov_id=x.id,name=y.name+"仓库",scale=rnditem("_matwhscale").id,base=rndnum(1,10),addr=rnditem("_person").origin,position=str(y.lng)+" "+str(y.lat),remark=rnditem("_songci"))

tbl_mat=Table('mat', metadata,
	Column('id',Integer,primary_key=True),
	Column('code',String(16)),
	Column('name',String(32)),
	Column('type',String(16)),
	Column('unit',String(16)),
	Column('usage',String(32)),
	Column('alarm',Integer),
	Column('essential',Integer),
	Column('matbase',Integer),
	Column('remark',String(2048)))
def dict_mat(x):
    return dict(code=x.code,name=x.name,type=x.type,unit=x.unit,usage=rnditem("_songci"),alarm=x.alarm,essential=rnditem("_essential").id,matbase=x.matbase,remark=x.remark)

tbl_matin=Table('matin', metadata,
	Column('id',Integer,primary_key=True),
	Column('matwh_id',Integer),
	Column('status',Integer),
	Column('code',String(16)),
	Column('source',Integer),
	Column('courier',String(32)),
	Column('courierdate',Date),
	Column('remark',String(2048)),
	Column('img',String(32)))
def dict_matin(x):
    return dict(matwh_id=x.matwh_id,status=x.status,code=rndqq(),source=rnditem2("_matsouce").id,courier=rnditem2("_person").name,courierdate=rnddate(30,60),remark=rnditem2("_songci"),img="")

tbl_matinrec=Table('matinrec', metadata,
	Column('id',Integer,primary_key=True),
	Column('matwh_id',Integer),
	Column('matin_id',Integer),
	Column('mat_id',Integer),
	Column('num',Integer),
	Column('specs',String(16)),
	Column('vender_id',Integer),
	Column('producedt',Date),
	Column('expiredt',Date),
	Column('remark',String(2048)))
def dict_matinrec(matwh_id,matin_id):
    dt=rnddate(30,60)
    return dict(matwh_id=matwh_id,matin_id=matin_id,mat_id=rnditem2("mat").id,num=rndnum(1000,50000),specs=random.choice( ["100kg/包","100kg/袋", "100m/卷", "100个/盒"]),vender_id=rnditem2("matvender").id,producedt=dt,expiredt=rnddatespan(dt,60,90),remark=rnditem2("_songci"))

tbl_matout=Table('matout', metadata,
	Column('id',Integer,primary_key=True),
	Column('fault_id',Integer),
	Column('fault_code',String(16)),
	Column('matwh_id',Integer),
	Column('status',Integer),
	Column('code',String(16)),
	Column('usage',String(32)),
	Column('recver',String(32)),
	Column('recvdate',Date),
	Column('remark',String(2048)),
	Column('img',String(32)))
def dict_matout(x):
    return dict(fault_id=x.fault_id,fault_code=x.fault_code,matwh_id=x.matwh_id,status=x.status,code=rndqq(),usage=x.usage,recver=rnditem2("_person").name,recvdate=rnddate(30,60),remark=rnditem2("_songci"),img="")

tbl_matoutrec=Table('matoutrec', metadata,
	Column('id',Integer,primary_key=True),
	Column('matout_id',Integer),
	Column('matinrec_id',Integer),
	Column('num',Integer),
	Column('remark',String(2048)))
def dict_matoutrec(x):
    dt=rnddate(30,60)
    return dict(matout_id=x.matout_id,matinrec_id=x.matinrec_id,num=x.num,remark=rnditem2("_songci"))

tbl_chat=Table('chat', metadata,
	Column('id',Integer,primary_key=True),
	Column('fault_id',Integer),
	Column('user_id',Integer),
	Column('say',String(1024)),
	Column('date',Date))
def dict_chat(x):
    return dict(fault_id=x.fault_id,user_id=x.user_id,say=x.say,date=x.date)


metadata.create_all(engine)
conn = engine.connect()

def QueryAll(tbl):
    data=conn.execute(select([tbl])).fetchall()
    adddata(tbl.name,data)

def QueryData(name,tbl,field,value):
    q = select([tbl]).where(tbl.c[field]==value)
    data=conn.execute(q).fetchall()
    adddata(name,data)

conn.execute(tbl_user.insert(),[
            {"id":"1","account":"su_win","pwd":"su_win","name":"叶片超级帐号","job":"1","face":"img/face/face10.jpg"},
            {"id":"4","account":"su_dev","pwd":"su_dev","name":"设备超级帐号","job":"4","face":"img/face/face11.jpg"},
            {"id":"7","account":"su_mat","pwd":"su_mat","name":"仓库超级帐号","job":"7","face":"img/face/face12.jpg"},
            {"id":"10","account":"su_eng","pwd":"su_eng","name":"调度超级帐号","job":"10","face":"img/face/face13.jpg"},
            {"id":"13","account":"su_exp","pwd":"su_exp","name":"专家超级帐号","job":"13","face":"img/face/face14.jpg"},
            {"id":"15","account":"su_rep","pwd":"su_rep","name":"技工超级帐号","job":"15","face":"img/face/face15.jpg"},
            {"id":"18","account":"su_blg","pwd":"su_blg","name":"博客超级帐号","job":"18","face":"img/face/face16.jpg"},
            {"id":"50","account":"test50","pwd":"test50","name":"测试50","job":"19","face":"img/face/face0.jpg"},
            {"id":"51","account":"test51","pwd":"test51","name":"测试51","job":"19","face":"img/face/face1.jpg"},
            {"id":"52","account":"test52","pwd":"test52","name":"测试52","job":"19","face":"img/face/face2.jpg"},
            {"id":"53","account":"test53","pwd":"test53","name":"测试53","job":"19","face":"img/face/face3.jpg"},
            {"id":"54","account":"test54","pwd":"test54","name":"测试54","job":"19","face":"img/face/face4.jpg"},
            {"id":"55","account":"test55","pwd":"test55","name":"测试55","job":"19","face":"img/face/face5.jpg"},
            {"id":"56","account":"test56","pwd":"test56","name":"测试56","job":"19","face":"img/face/face6.jpg"},
            {"id":"57","account":"test57","pwd":"test57","name":"测试57","job":"19","face":"img/face/face7.jpg"},
            {"id":"58","account":"test58","pwd":"test58","name":"测试58","job":"19","face":"img/face/face8.jpg"},
            {"id":"59","account":"test59","pwd":"test59","name":"测试59","job":"19","face":"img/face/face9.jpg"},
            {"id":"100","account":"angel","pwd":"angel","name":"天使","job":"19"}])
conn.execute("CREATE VIEW matoutview AS select matout.id,fault_id,fault_code,matwh_id,matout.status,code,usage,matout.remark,img,creater.user_id as creater_id,creater.date as createdate,stocker.user_id as stocker_id,stocker.date as stockdate from matout LEFT JOIN flow AS creater ON (creater.table_id = 28 AND creater.record_id = matout.id AND creater.status = 0) LEFT JOIN flow AS stocker ON (stocker.table_id = 28 AND stocker.record_id = matout.id AND stocker.status = 2)")

conn.execute("CREATE VIEW matoutrecview AS select matoutrec.id,matout.matwh_id,matoutrec.matout_id,matout.code as matout_code,matout.status as matout_status,mat.id as mat_id,mat.code,mat.name,mat.type,matoutrec.num,mat.unit,matinrec.specs,matinrec.matin_id,matin.code as matin_code,matin.status as matin_status,matinrec.id as matinrec_id,matinrec.vender_id,matinrec.producedt,matinrec.expiredt,matinrec.remark as matinrec_remark,matoutrec.remark from matoutrec,matinrec,mat,matin,matout where matoutrec.matinrec_id = matinrec.id and matinrec.mat_id=mat.id and matoutrec.matout_id=matout.id and matinrec.matin_id=matin.id")

conn.execute("CREATE VIEW inrecview AS select matinrec.id,matin.matwh_id,matinrec.matin_id,matin.code as matin_code,matin.status as matin_status,matin.source,matinrec.mat_id,matinrec.num,matinrec.specs,matinrec.vender_id,matinrec.producedt,matinrec.expiredt,matinrec.remark from matinrec,matin where matinrec.matin_id = matin.id")

conn.execute("CREATE VIEW outrecview AS select matoutrec.id,matout.matwh_id,matoutrec.matout_id,matout.code as matout_code,matout.status as matout_status,matout.usage,matinrec.mat_id,matoutrec.num,matinrec.specs,matinrec.matin_id,matinrec.id as matinrec_id,matinrec.vender_id,matinrec.producedt,matinrec.expiredt,matinrec.remark as matinrec_remark,matoutrec.remark from matoutrec,matinrec,matout where matoutrec.matinrec_id = matinrec.id and matoutrec.matout_id=matout.id ")

conn.execute(tbl_base.insert(),[dict_base(x) for x in data("_fields")])




conn.execute(tbl_admarea.insert(),[dict_admarea(x) for x in data("_全国行政区编号")])








conn.execute(tbl_opus.insert(),[dict_opus(x) for x in range(500)])

conn.execute(tbl_follow.insert(),[dict_follow(x,y) for x in range(10) for y in sample([z for z in range(10) if z!=x],randint(0,9))])

conn.execute(tbl_vender.insert(),[dict_vender(x,17) for x in data("_efan_vender")])
conn.execute(tbl_vender.insert(),[dict_vender(x,18) for x in data("_leaf_vender")])
QueryData("efanvender",tbl_vender,"type",17)
QueryData("leafvender",tbl_vender,"type",18)
conn.execute(tbl_winderco.insert(),[dict_winderco(x) for x in data("_winderco")])
QueryAll(tbl_winderco)

conn.execute(tbl_winderprov.insert(),[dict_winderprov(x,y) for x in data("winderco") for y in rndarea(prov,3,6)])
QueryAll(tbl_winderprov)

conn.execute(tbl_winder.insert(),[dict_winder(x,y) for y in data("winderprov") for x in rndarea(prov[y.name],3,6)])
QueryAll(tbl_winder)

conn.execute(tbl_winderarea.insert(),[dict_winderarea(x,y) for y in data("winder") for x in rndarea(prov[getitem("winderprov",y.winderprov_id).name][y.name[:-2]],2,5)])
QueryAll(tbl_winderarea)

conn.execute(tbl_efan.insert(),[dict_efan(x,y) for x in data("winderarea") for y in range(rndnum(30,50))])
QueryAll(tbl_efan)

conn.execute(tbl_leaf.insert(),[dict_leaf(x,y) for x in data("efan") for y in range(3)])
QueryAll(tbl_leaf)


conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","1","")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"winder","2","") for x in data("winder")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"winder","3","") for x in data("winder") for y in range(rndnum(2,3))])
conn.execute(tbl_config.insert(),[dict_config("ethnic",x[0]) for x in data("_ethnic").data])
conn.execute(tbl_vender.insert(),[dict_vender(x,21) for x in data("_dev_vender")])
QueryData("devvender",tbl_vender,"type",21)
conn.execute(tbl_devwh.insert(),[dict_devwh(x) for x in data("_devwh")])
QueryAll(tbl_devwh)

conn.execute(tbl_dev.insert(),[dict_dev(x,y,z) for x in data("devwh") for y in data("_devclss") for z in range(rndnum(1,3))])
QueryAll(tbl_dev)


conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","4","")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"devwh","5","") for x in data("devwh")])
conn.execute(tbl_user.insert(),[dict_user(x.devwh_id,"devwh","6","") for x in data("dev")])
conn.execute(tbl_vender.insert(),[dict_vender(x,25) for x in data("_matvender")])
QueryData("matvender",tbl_vender,"type",25)
conn.execute(tbl_matprov.insert(),[dict_matprov(x) for x in rndarea(prov,3,6)])
QueryAll(tbl_matprov)

conn.execute(tbl_matwh.insert(),[dict_matwh(x,y) for x in data("matprov") for y in rndarea(prov[x.name],3,6)])
QueryAll(tbl_matwh)

conn.execute(tbl_mat.insert(),[dict_mat(x) for x in data("_mat")])
QueryAll(tbl_mat)

conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","7","")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"matwh","8","") for x in data("matwh")])
conn.execute(tbl_user.insert(),[dict_user(x.id,"matwh","9","") for x in data("matwh") for y in range(rndnum(2,5))])
QueryAll(tbl_matin)

QueryAll(tbl_matinrec)

QueryAll(tbl_matout)

QueryAll(tbl_matoutrec)

conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","10","")])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","11","")])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","12","") for x in range(rndnum(5,10))])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","13","")])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","14",rndskill()) for x in range(rndnum(10,20))])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","15","")])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","16","") for x in range(rndnum(10,20))])
conn.execute(tbl_user.insert(),[dict_user(0,"__sys__","17","") for x in range(rndnum(50,100))])


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
