# coding : UTF-8
import xlread as xl
import random
import datetime

class obj:
    pass

def xFileWrite(fname,data):
    f=open(fname,"r")
    f.write(data)
    f.close()

def xBuildModel():
    model = ""
    for t in tbls:
        iname = GetIndex(tbls[t].field, "name" )
        irule = GetIndex(tbls[t].field,"dtype")
        model += "class "+tbls[t].name+"(db.Model):\n\t"
        model += "".join(map( lambda f : f[iname].value + "=" + f[irule].value + "\n\t", tbls[t].data))
        model += "\n"
    return model

def GetIndex(ar, v ):
    for i,x in enumerate(ar):
        if x.value == v:
            return i
    return -1

def xBuildData():
    code = ""
    for t in tbls:
        iname = GetIndex(tbls[t].field, "name" )
        irule = GetIndex(tbls[t].field,"drule")
        for r,i in split(tbls[t].trule,";"):
            code += "\t"*i+r+":\n"
        code += "\t"*len(split(tbls[t].trule,";"))+ tbls[t].name+"(" + ",".join(map( lambda f : f[iname].value + "=" + f[irule].value, tbls[t].data)) + ")\n"
    return code

if __name__ == '__main__':
    tbls = xl.xlread('./db/dbdefine-s.xlsx').readtbl()
    xFileWrite( "model.py", xBuildModel(tbls) )
    im = "import model.py\nimport rnd.py\n"
    xFileWrite( "builddata.py", im + xBuildData(raws) )

    for x in range(50):
        print(rnddate(18,40))
    a = 0;
