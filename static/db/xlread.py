# coding : UTF-8

import xlrd

class obj:
    pass

class xlread(object):
    def __init__( self, xls ):
        self.xls = xlrd.open_workbook(xls)

    def readtbl(self):
        tbls = {}
        for sh in [ x for x in self.xls.sheets() if x.name.startswith("tblcoord")]:
            for r in [ x for x in range(sh.nrows) if sh.cell(x,0).value == "table" ]:
                tbl = xlread.xReadTable(sh,r,0)
                tbls[tbl.name] = tbl
        return tbls

    def readraw(self):
        raws = {}
        for sh in [ x for x in self.xls.sheets() if x.name.startswith("raw")]:
            for c in [ x for x in range(sh.ncols) if sh.cell(0,x).value == "table" ]:
                raw = xReadTable(sh,0,c)
                raws[raw.name] = raw
        return raws

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
        if sh.ncols > c+1 and sh.cell(r,c+1).value !="":
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
