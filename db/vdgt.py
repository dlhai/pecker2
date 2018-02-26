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
    length = len(dat_all["_person"].data)
    userunique = [x for x in range(len(dat_all["_person"].data))]
def data(tbl):
    return dat_all[tbl]
def adddata(name,data):
    dat_all[name]=data

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

def name2id(ar, name ):
    for i,x in enumerate(ar):
        if x.name == name:
            return x.id
    return -1

#拆分成rnduser和rnditem2 本接口不再用
def rnditem(name):
    tbl=dat_all[name]
    if name == "_person":
        idx = random.choice(userunique)
        userunique.remove(idx)
        return tbl.__getitem__(idx)
    if type(tbl) == type([]):
        idx = random.randint(0,len(tbl)-1)
        return tbl[idx]
    idx = random.randint(0,len(tbl.data)-1)
    if hasattr(tbl,"field"):
        return tbl.__getitem__(idx)
    elif name == "_songci":
        return tbl.data[idx][0][0:rndnum(8,32)]
    else:
        return tbl.data[idx][0]

def rnduser():
    tbl=dat_all["_person"]
    idx = random.choice(userunique)
    userunique.remove(idx)
    return tbl.__getitem__(idx)

def rnditem2(tblname):
    tbl=dat_all[tblname]
    if type(tbl) == type([]):
        idx = random.randint(0,len(tbl)-1)
        return tbl[idx]
    idx = random.randint(0,len(tbl.data)-1)
    if hasattr(tbl,"field"):
        return tbl.__getitem__(idx)
    elif tblname == "_songci":
        return tbl.data[idx][0][0:rndnum(8,32)]
    else:
        return tbl.data[idx][0]

def rndaddition(type):
    return random.choice([x.file for x in dat_all["_addition"] if x.type==type])

def getitem( tblname, id ):
    for x in dat_all[tblname]:
        if str(int(x.id)) == str(id):
            return x

def getitembyname( tblname, name ):
    for x in dat_all[tblname]:
        if x.name == name:
            return x
    return ""

def rndnum(min,max):
    return random.randint(min,max)

def rndtype(type):
    if type=="efan":
        s = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        s = s[0:2]+"-"+s[2:4]+"-"+s[4:6]+"-"+s[6:]
        return s
    elif type=="car":
        return ''.join(random.sample('京津冀晋蒙辽吉黑沪苏浙皖闽赣鲁豫鄂湘粤桂琼渝川黔滇藏陕甘青宁新台港澳',1)+
        random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1)+['.']+
        random.sample(string.digits, 6))
    return ""

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

#float转str，仅保留小数点后5位
def f2s(f):
    s = str(f)
    i = s.find(".")
    if i == -1:
        return s
    else:
        return s[:i+7]

def rndgpsarea(pos,xr,yr):
    x = float(pos.split(" ")[0]) - xr/2
    y = float(pos.split(" ")[1])- yr/2
    px = xr/9
    py = yr/9

    xo = random.randint(0,8)
    xs = random.randint(1,3)
    yo = random.randint(0,8)
    ys = random.randint(1,3)

    l = f2s(x+xo*px)
    t = f2s(y+yo*py)
    r = f2s(x+xo*px+xs*px)
    b = f2s(y+yo*py+ys*py)
    lt = l+" "+t
    rt = r+" "+t
    rb = r+" "+b
    lb = l+" "+b
    return ",".join([lt,rt,rb,lb])

#如果position是矩形，取其左上角和右下角，在其范围内随机生成一点
#如果position是点，以其为中心点，半长为0.3范围内的正小形区内随机一点
def rndgps( position ):
    ar=position.split(",")
    if (len(ar)==4):
        lt= ar[0].split(" ")
        rb= ar[2].split(" ") 
        l = float(lt[0])
        t = float(lt[1])
        r = float(rb[0])
        b = float(rb[1])
        return f2s(random.uniform(l,r))+" "+f2s(random.uniform(t,b))
    else:
        x= float(ar[0].split(" ")[0])
        y= float(ar[0].split(" ")[1])
        l = float(x-0.3)
        t = float(y-0.3)
        r = float(x+0.3)
        b = float(y+0.3)
        return f2s(random.uniform(l,r))+" "+f2s(random.uniform(t,b))

def rnddate(min,max):
    return (datetime.datetime.now() - datetime.timedelta(days = rndnum(min,max)))

def rnddatespan(dt,min,max):
    if type(dt) == type(""):
        dt =  datetime.datetime.strptime(dt,'%Y-%m-%d')
    return (dt + datetime.timedelta(days = rndnum(min,max)))

#把一个数随机切分成几块
def rndsplit(num, min, max):
    slices=[rndnum(0,num) for y in range(rndnum(min-1,max-1))]
    slices.extend([0,num])
    t=set(slices)
    slices=list(t) #滤掉相同的数
    slices.sort()
    for i in range(len(slices)-1):
        slices[i]=slices[i+1]-slices[i]
    slices.pop()
    return slices

def rndskill():
    return ",".join(list(set([ random.choice(["避雷","工艺设计","工艺生产","材料","安全"]) for x in range(4)])))

def rndpick( ar, aridx, count):
    sel = random.sample(aridx, count) #从数组aridx中随机选count个，作为一个数组返回
    [aridx.remove(x) for x in sel]
    return [ar[x] for x in sel]

if __name__=="__main__": 
    setdata(loadpkl('rawdata.pkl'))
