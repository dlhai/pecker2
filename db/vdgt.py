#encoding:utf8
#virtual data generate tools(vdgt)

import random
import pickle
import string
import datetime
#from testiter import *

dat_all = {}
userunique = []
def setdata(dat):
    global dat_all,userunique
    dat_all=dat
    userunique = [x for x in range(len(dat_all["_person"].data))]
def data(tbl):
    return dat_all[tbl]
def addtbl(tbl):
    dat_all[tbl.name]=tbl

def loadpkl(filename):
    f=open(filename,'rb+')
    r=pickle.load(f)
    f.close()
    return r
    

class objit(object):
    def __next__(self):
        if self.idx < len(self.obj.data)-1:
            self.idx = self.idx+1
        else:
            raise StopIteration
        return self
    def __getattr__(self,name):
        if name == "编号" or name == "父级":
            return str(int(self.obj.GetValue(self.idx,name)))
        else:
            return self.obj.GetValue(self.idx,name)

class obj(object):
    def __iter__(self):
        r = objit()
        r.obj = self
        r.idx = -1
        return r
    def __getitem__(self, k):
        r = objit()
        r.obj = self
        r.idx = k
        return r
    def GetValue( self, r, c ):
        for i,x in enumerate(self.field):
            if x == c:
                return self.data[r][i]
        else:
            raise KeyError

def T(s):
    if ( s.count(":") == 0):
        return s
    ar =s.split(":")
    if ( len(ar)==2):
        if ( ar[0] == "rnditem" ):
            return ar[0] + "(\"" + ar[1]+"\")"
        else:
            return ar[0] + "[\"" + ar[1]+"\"]"
    else:
        if ( ar[0] == "rnditem" ):
            return ar[0] + "(\"" + ar[1]+"\")."+ar[2]
        else:
            return ar[0] + "[\"" + ",".join(ar[1:])+"\"]"
    return r;

def GetIndex(ar, v ):
    for i,x in enumerate(ar):
        if x == v:
            return i
    return -1

def rnditem(name):
    tbl=dat_all[name]
    if name == "_person":
        idx = random.choice(userunique)
        userunique.remove(idx)
        return tbl.__getitem__(idx)
    idx = random.randint(0,len(tbl.data)-1)
    if hasattr(tbl,"field"):
        return tbl.__getitem__(idx)
    else:
        return tbl.data[idx][0]

def rndaddition(type):
    return random.choice([x.file for x in dat_all["_addition"] if x.type==type])

def getitem( tblname, id ):
    for x in dat_all[tblname]:
        if x.id == id:
            return x

def rndnum(min,max):
    return random.randint(min,max)

def rndtype(type):
    if type=="efan":
        s = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        s = s[0:2]+"-"+s[2:4]+"-"+s[4:6]+"-"+s[6:]
        return s

def id2sex(id):
    return int(id[16])%2

def id2birth(id):
    return id[6:10]+"-"+id[10:12]+"-"+id[12:14]

def rndqq():
    len = random.randint(8,10)
    return ''.join(random.sample(string.digits, len))

def rndmail(person):
    mailaddr = random.choice( ["21cn.com","sina.com","163.com", "163.net", "qq.com"])
    mailname = random.choice( [person.pinyin,str(int(person.qq))])
    return mailname+"@"+mailaddr

def rndwechat(person,mail):
    return random.choice([str(int(person.phone)),mail,person.pinyin,str(int(person.qq))])

def rndgpsarea(pos,xr,yr):
    x = float(pos.split(" ")[0]) - xr/2
    y = float(pos.split(" ")[1])- yr/2
    px = xr/9
    py = yr/9

    xo = random.randint(0,8)
    xs = random.randint(1,3)
    yo = random.randint(0,8)
    ys = random.randint(1,3)

    l = str(x+xo*px)
    t = str(y+yo*py)
    r = str(x+xo*px+xs*px)
    b = str(y+yo*py+ys*py)
    lt = l+" "+t
    rt = r+" "+t
    rb = r+" "+b
    lb = l+" "+b
    return ",".join([lt,rt,rb,lb])

def rndgps( position ):
    lt= position.split(",")[0].split(" ")
    rb= position.split(",")[0].split(" ") 
    l = float(lt[0])
    t = float(lt[1])
    r = float(rb[0])
    b = float(rb[1])
    return str(random.uniform(l,r))+" "+str(random.uniform(t,b))

def rnddate(min,max):
    return (datetime.datetime.now() - datetime.timedelta(days = rndnum(min,max)))

def rnddatespan(dt,min,max):
    return (dt + datetime.timedelta(days = rndnum(min,max)))

def xFileWrite(fname,data):
    f=open(fname,"wb+")
    f.write(data.encode())
    f.close()

def CreateRelationData():
    #1.风场主管、驻场
    #for x in dat["winder"]:
    #    CreateUser( job="风场主管", skill="", x.id, depart_table="winder" )
    #    for y in range(rndnum(2,5)):
    #        CreateUser( job="驻场", skill="", x.id, depart_table="winder" )
    pass

if __name__=="__main__": 
    setdata(loadpkl('rawdata.pkl'))
    #s = '东莞市风场'
    #b=s[:-2]
    #a = dobj()
    #a.a1="A1"
    #a.a2="A2"
    #bb = dobj()
    #bb.a3="A3"
    #bb.a4="A4"
    #cc = dobj()
    #cc.a5="A5"
    #cc.a6="A6"
    #ddd = dobj()
    #ddd.a7="A7"
    #ddd.a8="A8"
    #eee = dobj()
    #eee.a9="A9"
    #eee.a10="A10"
    #fff = dobj()
    #fff.a11="A11"
    #fff.a12="A12"
    #ggg = dobj()
    #ggg.a13="A13"
    #ggg.a14="A14"

    #a["bb"]=bb
    #a["cc"]=cc
    #bb["ddd"]=ddd
    #bb["eee"]=eee
    #cc["fff"]=fff
    #cc["ggg"]=ggg

    #a7=a["bb"]["ddd"].a7

    #s = rndtype("efan")

    #dt = rnddate(4*365,5*365)
    s = rndaddition("身份证")
    x=0