#encoding:utf8
from xlread import xlread
import random
import pickle

class dobj():
    def __init__(self):
        self.__dict__["__attr__"]={}
        self.sub={}
    def __getitem__(self, name):
        if name not in self.sub.keys():
            x = 0
        return self.sub[name]
    def __setitem__(self, name,value):
        self.sub[name]=value
    def __getattr__(self,name):
        if name.startswith("__") and name.endswith("__"):
            return self.__dict__[name]
        else:
            return self.__dict__["__attr__"][name]
    def __setattr__(self,name,value):
        self.__dict__["__attr__"][name]=value
    def __getstate__(self):
        return self.__dict__["__attr__"]
    def __setstate__(self, state):
        self.__dict__["__attr__"] = state

def _buildarea():
    raw_area = xlread('./areas.xls').readraw()
    prt = {}
    name ={}
    china=dobj()
    for x in raw_area["_全国行政区编号"]:
        area = dobj()
     #   area.编号=x.编号
     #   area.name=x.名称
     #   area.简称=x.简称
        area.lng=x.经度
        area.lat=x.纬度
     #   area.等级=x.等级
     #   area.父级=x.父级

        name[x.编号] =x.名称
        code=x.父级
        if x.等级 == 1:
            china[x.名称]=area
        elif x.等级 == 2:
            china[name[x.父级]][x.名称]=area
        elif x.等级 == 3:
            china[name[code[0:2]+"0000"]][name[x.父级]][x.名称]=area
            prt[x.编号]=x.父级
        elif x.等级 == 4:
            china[name[code[0:2]+"0000"]][name[prt[x.父级]]][name[x.父级]][x.名称]=area
    f=open('areadata.pkl','wb+')  
    pickle.dump( china, f)
    f.close()  

def rndarea(ar,min,max):
    if min == 0 and max == -1:
        return ar
    else:
        size = len(ar.__attr__["sub"])
        min = min if min < size else size
        max = max if max < size else size
        a = random.sample(range(size), random.randint(min,max))
        r = []
        for k in [list(ar.__attr__["sub"].keys())[x] for x in a]:
            t = dobj()
            t.name=k
            t.lng=ar[k].lng
            t.lat=ar[k].lat
            r.append(t)
        return r

def __rndarea_test():
    e=open('areadata.pkl','rb+')  
    cn = pickle.load(e)
    e.close()
    ar = rndarea(cn, 5, 10)
    x = 0

def __dobj():
    a = dobj()
    a.a1="A1"
    a.a2="A2"
    bb = dobj()
    bb.a3="A3"
    bb.a4="A4"
    cc = dobj()
    cc.a5="A5"
    cc.a6="A6"
    ddd = dobj()
    ddd.a7="A7"
    ddd.a8="A8"
    eee = dobj()
    eee.a9="A9"
    eee.a10="A10"
    fff = dobj()
    fff.a11="A11"
    fff.a12="A12"
    ggg = dobj()
    ggg.a13="A13"
    ggg.a14="A14"

    a["bb"]=bb
    a["cc"]=cc
    bb["ddd"]=ddd
    bb["eee"]=eee
    cc["fff"]=fff
    cc["ggg"]=ggg

    a7=a["bb"]["ddd"].a7
    x=0


if __name__=="__main__":   
    __rndarea_test()