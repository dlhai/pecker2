# coding : UTF-8
from xlread import xlread
import random
import datetime
from vdgt import *

def xBuildModel(tbls):
    model = '''#encoding:utf8
from sqlalchemy import *
from vdgt import *
from buildarea import dobj,rndarea
import time

setdata(loadpkl('rawdata.pkl'))
prov=loadpkl('areadata.pkl')

engine = create_engine('sqlite:///./'+str(int(time.time()))+'.db')
engine.echo = True
metadata = MetaData(engine)

'''
    for t in [ x for x in tbls if x.type == "table"]:
        iname = GetIndex(t.field, "name")
        irule = GetIndex(t.field,"dtype")
        model += "tbl_"+t.name+"=Table('"+t.name+"', metadata,\n\tColumn('"
        model += "),\n\tColumn('".join(map( lambda f : f[iname]+"',"+f[irule],t.data))
        model += "))\n\n"

    model += '''
metadata.create_all(engine)
conn = engine.connect()

def QueryAll(tbl):
    r=obj()
    r.name=tbl.name
    r.field=[f.name for f in tbl.columns]
    r.data=conn.execute(select([tbl])).fetchall()
    addtbl(r)

'''
    for t in [ x for x in tbls if x.type == "table"]:
        model += "def dict_"+t.name+t.param+":\n    "
        if t.define !="":
            model += t.define.replace("\n", "\n    ")+"\n    "
        iname = GetIndex(t.field, "name")
        irule = GetIndex(t.field,"drule")
        cols = [c for c in t.data if c[iname] != "id" ];
        model += "return dict("
        model += ",".join(map( lambda c : c[iname] + "=" + T(c[irule]), cols))
        model += ")\n"
        if t.cycle != "":
            model +="conn.execute(tbl_"+t.name+".insert(),[dict_"+t.name+t.param+" "+t.cycle+"])\n"
        if t.query == "QueryAll":
            model += "QueryAll(tbl_"+t.name+")\n\n"
        else:
            model += "\n"

    for t in [ x for x in tbls if x.type == "builddata"]:
        model += "conn.execute(tbl_"+t.name+".insert(),[dict_"+t.name+t.cycle+"])\n"

    model += "conn.execute(tbl_base.insert(),["
    for t in [ x for x in tbls if x.type == "table"]:
        for r in t.data:
            model += 'dict(table="' + t.name+'",'
            for i in range(len(t.field)):
                if '"' in r[i]:
                    model += t.field[i] +"='" + r[i] + "',"
                elif "'" in r[i]: 
                    model += t.field[i] +'="' + r[i] + '",'
                else:
                    model += t.field[i] +'="' + r[i] + '",'
            model += "),\n"
    model += "])"
    return model

if __name__ == '__main__':
    xl = xlread('./db.xlsx')
    f=open('rawdata.pkl','wb+')  
    pickle.dump( xl.readraw(), f)
    f.close()  
    xFileWrite( "model.py", xBuildModel(xl.readtbl()) )




