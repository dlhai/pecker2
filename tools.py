
def rndstr(len):
    return ''.join(random.sample("abcdefghijklmnopqrstuvwxyz0123456789", len))

class obj:
    def __init__(self,  **kw ):
        for k,v in kw.items():
            setattr( self, k, v)

def atoi(s):
    return 0 if s == "" else int(s)

#��python����ת��json
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

#��(a,b,c) ��� in ('a','b','c')
def To(k,v):
    if v[0] == "(":
        return k +" in ("+",".join( ["'"+i+"'" for i in v.strip("()").split(",")]) + ")"
    else:
        return k+"='"+v+"'"

#�����༶Ŀ¼
import os.path
def newdir(path):
    for p in path:
        if not os.path.exists(p):
            os.mkdir(p)

