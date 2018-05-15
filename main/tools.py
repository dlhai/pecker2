#encoding:utf8
def rndstr(len):
    return ''.join(random.sample("abcdefghijklmnopqrstuvwxyz0123456789", len))

class obj:
    def __init__(self,  **kw ):
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
    ls = [1,2,3]
    rs = map(str, ls)
    for k in rs:
        print(k)
    aa=map(lambda x:x.name, [obj(name="a",id=1),obj(name="b",id=2),obj(name="c",id=3)])
    print(type(aa))
    pdb.set_trace()
    b=0
