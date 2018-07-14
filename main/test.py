#encoding:utf-8

a={"aa":"1234","bb":"(1,2,3,4)", "cc":"23445", "dd":"(4,5,6,7)"}
r = " and ".join([ k+"='"+str(v)+"'" for k,v in a.items()])
rr =r.replace("='(", " in (")
rr =rr.replace(")'", ")")
aa=0