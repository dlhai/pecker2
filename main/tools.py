#encoding:utf8
def rndstr(len):
    return ''.join(random.sample("abcdefghijklmnopqrstuvwxyz0123456789", len))

class obj:
    def __init__(self, *o, **kw ):
        for x in o:
            for k,v in x.__dict__.items():
                setattr( self, k, v)
        for k,v in kw.items():
            setattr( self, k, v)

def atoi(s):
    return 0 if s == "" else int(s)

#把python对象转换成json字符串
def tojson(o):
    if type(o) == type([]):
        return "["+",".join([tojson(t) for t in o ])+"]\n";
    elif type(o) == type({}):
        return "{"+",".join(['"'+k+'":'+tojson(v) for k,v in o.items() ])+"}\n";
    elif type(o) == type(obj()):
        return tojson(o.__dict__)
    elif o == None:
        return '""'
    else:
        return '"'+str(o)+'"'

def toret(r,**kw):
    for k,v in kw.items():
        setattr( r, k, v)
    return tojson(r)

#把(a,b,c) 变成 in ('a','b','c')
def To(k,v):
    if v[0] == "(":
        return k +" in ("+",".join( ["'"+i+"'" for i in v.strip("()").split(",")]) + ")"
    else:
        return k+"='"+v+"'"


#创建多级目录
import os.path
def newdir(path):
    for p in path:
        if not os.path.exists(p):
            os.mkdir(p)

import pdb
if __name__ == "__main__":
    rec = obj()
    rec.type = "1" #1changejob
    rec.sss="2"
    vals=",".join([ k+"='"+v+"'" for k,v in rec.__dict__.items()])

    for k,v in rec.__dict__.items():
        print(k,v)
    aa=0