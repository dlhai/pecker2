# coding : UTF-8
from xlread import xlread
import random
import datetime
import pickle

class obj():
    pass

def GetIndex(ar, v ):
    for i,x in enumerate(ar):
        if x == v:
            return i
    return -1

def T(s):
    if s.count(":") == 0:
        return s
    ar =s.split(":")
    if len(ar)==2:
        if ar[0] == "rnditem" or ar[0] == "rnditem2":
            return ar[0] + "(\"" + ar[1]+"\")"
        else:
            return ar[0] + "[\"" + ar[1]+"\"]"
    elif len(ar)>2:
        if ar[0] == "rnditem" or ar[0] == "rnditem2":
            return ar[0] + "(\"" + ar[1]+"\")."+ar[2]
        elif ar[0] == "xsample":
            return ar[0] + "(\"" +ar[1] +"\","+ ",".join(ar[2:])+")"
        else:
            return ar[0] + "[\"" + ",".join(ar[1:])+"\"]"
    raise Exception;

def xBuildModel(tbls):
    model = '''#encoding:utf8
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

'''
    for t in [ x for x in tbls if x.type == "table"]:
        iname = GetIndex(t.field, "name")
        irule = GetIndex(t.field,"dtype")
        model += "tbl_"+t.name+"=Table('"+t.name+"', metadata,\n\tColumn('"
        model += "),\n\tColumn('".join(map( lambda f : f[iname]+"',"+f[irule],t.data))
        model += "))\n"
        model += "def dict_"+t.name+t.param+":\n    "
        if t.define !="":
            model += t.define.replace("\n", "\n    ")+"\n    "
        iname = GetIndex(t.field, "name")
        irule = GetIndex(t.field,"drule")
        cols = [c for c in t.data if c[iname] != "id" ];
        model += "return dict("
        model += ",".join(map( lambda c : c[iname] + "=" + T(c[irule]), cols))
        model += ")\n\n"

    model += '''
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
            {"id":"1","account":"su_win","pwd":"su_win","name":"叶片超级帐号","job":"1","face":"img/face/face0.jpg"},
            {"id":"4","account":"su_dev","pwd":"su_dev","name":"设备超级帐号","job":"4","face":"img/face/face1.jpg"},
            {"id":"7","account":"su_mat","pwd":"su_mat","name":"仓库超级帐号","job":"7","face":"img/face/face2.jpg"},
            {"id":"10","account":"su_eng","pwd":"su_eng","name":"调度超级帐号","job":"10","face":"img/face/face3.jpg"},
            {"id":"13","account":"su_exp","pwd":"su_exp","name":"专家超级帐号","job":"13","face":"img/face/face4.jpg"},
            {"id":"15","account":"su_rep","pwd":"su_rep","name":"技工超级帐号","job":"15","face":"img/face/face5.jpg"},
            {"id":"18","account":"su_blg","pwd":"su_blg","name":"博客超级帐号","job":"18","face":"img/face/face6.jpg"},
            {"id":"50","account":"test50","pwd":"test50","name":"测试50","job":"19","face":"img/face/face7.jpg"},
            {"id":"51","account":"test51","pwd":"test51","name":"测试51","job":"19","face":"img/face/face8.jpg"},
            {"id":"52","account":"test52","pwd":"test52","name":"测试52","job":"19","face":"img/face/face9.jpg"},
            {"id":"53","account":"test53","pwd":"test53","name":"测试53","job":"19","face":"img/face/face10.jpg"},
            {"id":"54","account":"test54","pwd":"test54","name":"测试54","job":"19","face":"img/face/face11.jpg"},
            {"id":"55","account":"test55","pwd":"test55","name":"测试55","job":"19","face":"img/face/face12.jpg"},
            {"id":"56","account":"test56","pwd":"test56","name":"测试56","job":"19","face":"img/face/face13.jpg"},
            {"id":"57","account":"test57","pwd":"test57","name":"测试57","job":"19","face":"img/face/face14.jpg"},
            {"id":"58","account":"test58","pwd":"test58","name":"测试58","job":"19","face":"img/face/face15.jpg"},
            {"id":"59","account":"test59","pwd":"test59","name":"测试59","job":"19","face":"img/face/face16.jpg"},
            {"id":"100","account":"angel","pwd":"angel","name":"天使","job":"19","face":"img/face/face17.jpg"}
            ])
'''
    for t in [ x for x in tbls if x.type == "view"]:
        iname = GetIndex(t.field, "name")
        model += 'conn.execute("CREATE VIEW '+t.name+' AS select '
        model += ",".join(map( lambda f : f[iname],t.data))
        model += " from "+ t.fromtables + '")\n\n'

    for t in tbls:
        if t.type == "table":
            if t.cycle != "":
                model +="conn.execute(tbl_"+t.name+".insert(),[dict_"+t.name+t.param+" "+t.cycle+"])\n"
            if t.query == "QueryAll":
                model += "QueryAll(tbl_"+t.name+")\n\n"
            else:
                model += "\n"
        elif t.type == "builddata":
            model += "conn.execute(tbl_"+t.name+".insert(),[dict_"+t.name+t.cycle+"])\n"
        elif t.type == "py":
            model += t.name+"\n"

    model += '''
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
'''

    return model

def gatherfields(tbls):
    ret = []
    for t in [ x for x in tbls if x.type == "table" or x.type=="view"]:
        for r in t.data:
            field = obj()
            field.table = str(t.name)
            field.title = str(r[0])
            field.name = str(r[1])
            if -1 != field.name.find(" as "):
                field.name = field.name.split(" as ")[1]
            if -1 != field.name.find("."):
                field.name = field.name.split(".")[1]
            field.forder = str(r[2])
            field.ftype = str(r[3])
            field.twidth = str(r[4])
            field.tstyle = str(r[5])
            field.dtype = str(r[6])
            field.drule = str(r[7])
            field.remark = str(r[8])
            ret.append(field);
    return ret

def xFileWrite(fname,data):
    f=open(fname,"wb+")
    f.write(data.encode())
    f.close()

if __name__ == '__main__':
    xl = xlread('./db.xlsx')
    tbls = xl.readtbl();
    raw=xl.readraw()
    raw["_fields"]=gatherfields(tbls);
    xFileWrite( "model.py", xBuildModel(tbls) )
    f=open('rawdata.pkl','wb+')
    pickle.dump( raw, f)
    f.close()  




