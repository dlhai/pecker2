# coding : UTF-8
import xlrd
import random
import datetime

class obj:
    pass

def xReadBlock(sh, r, c, rc, cc ):
    if rc == -1:
        rc=0
        while(r+rc < sh.nrows and sh.cell(r+rc, c).value!="" ):
            rc=rc+1
    if cc == -1:
        cc=0
        while(c+cc < sh.ncols and sh.cell(r,c+cc).value!="" ):
            cc=cc+1
    rt = []
    for y in range(rc):
        row = []
        for x in range(cc):
            row.append( sh.cell(r+y,c+x))
        rt.append(row)
    return rt

def xReadTable( sh,r,c ):
    tbl = obj()
    if sh.ncols > c+1:
        if sh.cell(r,c+1).value !="":
            tbl.name = sh.cell(r,c+1).value
            if sh.ncols > c+2:
                tbl.title = sh.cell(r,c+2).value
    if not hasattr( tbl,"name"):
        tbl.name = sh.cell(r,c).value
    if sh.ncols > c+1 and sh.cell(r+1,c+1).value !="":
        tbl.field = xReadBlock(sh, r+1,c,1,-1)[0]
        tbl.data = xReadBlock(sh,r+2,c,-1,len(tbl.field))
    else:
        tbl.data = xReadBlock(sh,r+1,c,-1,1)
    return tbl

def xLoadxls(fname):
    xls = xlrd.open_workbook(fname)
    for sh in xls.sheets():
        if sh.name.startswith("tbl"):
            i = 0
            while i < sh.nrows:
                if sh.cell(i,0).value == "table":
                    tbl = xReadTable(sh,i,0)
                    tbls[tbl.name] = tbl
                    i += len(tbl.data)+1
                i += 1
        elif sh.name.startswith("raw"):
            i = 0
            while i < sh.ncols:
                if sh.cell_value(0,i) != "":
                    tbl = xReadTable(sh,0,i)
                    raws[tbl.name] = tbl;
                    if hasattr(tbl,"field"):
                        i += len(tbl.field)-1
                i += 1

raws = {}
tbls = {}
data = {}

def xDateRnd( agemin,agemax ):
    day = random.randint(agemin*365+int(agemin/4),agemax*365+int(agemax/4))
    yearago = datetime.datetime.now() - datetime.timedelta(day)
    return yearago.strftime("%Y-%m-%d")

def GetIndex(ar, v ):
    for i,x in enumerate(ar):
        if x.value == v:
            return i
    return -1

def xBuildModel():
    model = ""
    for t in tbls:
        iname = GetIndex(tbls[t].field, "name" )
        irule = GetIndex(tbls[t].field,"dtype")
        model += "class "+tbls[t].name+"(db.Model):\n\t"
        model += "".join(map( lambda f : f[iname].value + "=" + f[irule].value + "\n\t", tbls[t].data))
        model += "\n"
    return model

if __name__ == '__main__':
    a=['40', '25', '2.5', '-0.5105', '-0.54665', '-0.58815', '-0.5495', '-0.560499', '-0.04279']
    print( sum(map( lambda x: float(x), a )))
    print(sum([float(x) for x in a]))

    xLoadxls('./db/dbdefine-s.xlsx')
    m = xBuildModel()

    for x in range(50):
        print(rnddate(18,40))
    a = 0;
