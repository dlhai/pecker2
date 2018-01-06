# coding : UTF-8

import xlrd
from vdgt import *
class xlread(object):
    def __init__( self, xls ):
        self.xls = xlrd.open_workbook(xls)

    def readtbl(self):
        tbls = []
        for sh in [ x for x in self.xls.sheets() if x.name.startswith("tbl")]:
            for r in [ x for x in range(sh.nrows) if sh.cell(x,0).value == "table" ]:
                tbl = xlread.xReadTable(sh,r,0)
                tbl.type="table"
                tbls.append(tbl)
            for r in [ x for x in range(sh.nrows) if sh.cell(x,0).value == "builddata" ]:
                tbl = xlread.xReadTable(sh,r,0)
                tbl.type="builddata"
                tbls.append(tbl)
        return tbls

    def readraw(self):
        raws = {}
        for sh in [ x for x in self.xls.sheets() if x.name.startswith("raw")]:
            for c in [ x for x in range(sh.ncols) if sh.cell(0,x).value != "" ]:
                x = xlread.xReadTable(sh,0,c)
                raws[ "_"+x.name] =x
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
            #row = []
            #for x in range(cc):
            #    val = sh.cell(r+y,c+x).value
            #    if isinstance(val,type('')):
            #        val = .strip(" \t")
            #    row.append(val)
            #rt.append(row)
            row = [sh.cell(r+y,c+x).value for x in range(cc)]
            row = map(lambda x : x if not isinstance(x,type('')) else x.strip(" \t"), row)
            rt.append(list(row))
        return rt

    def xReadTable( sh,r,c ):
        tbl = obj()
        if sh.ncols > c+1 and sh.cell(r,c+1).value !="":
            tbl.name = sh.cell(r,c+1).value
            if sh.ncols > c+2:
                tbl.title = sh.cell(r,c+2).value
        if not hasattr( tbl,"name"):
            tbl.name = sh.cell(r,c).value
        if sh.cell(r,c).value == "table":
            tbl.type = sh.cell(r,c).value
            tbl.name = sh.cell(r,c+1).value
            tbl.title = sh.cell(r,c+2).value
            #tbl.xxxx = sh.cell(r,c+3).value
            tbl.query = sh.cell(r,c+4).value
            tbl.param = sh.cell(r,c+5).value
            tbl.define = sh.cell(r,c+6).value
            tbl.cycle = sh.cell(r,c+7).value
        elif sh.cell(r,c).value == "builddata":
            tbl.type = sh.cell(r,c).value
            tbl.name = sh.cell(r,c+1).value
            tbl.title = sh.cell(r,c+2).value
            #tbl.xxxx = sh.cell(r,c+3).value
            tbl.cycle = sh.cell(r,c+4).value

        if sh.ncols > c+1 and sh.nrows > r+1 and sh.cell(r+1,c+1).value !="":
            tbl.field = xlread.xReadBlock(sh, r+1,c,1,-1)[0]
            tbl.data = xlread.xReadBlock(sh,r+2,c,-1,len(tbl.field))
        else:
            tbl.data = xlread.xReadBlock(sh,r+1,c,-1,1)
        return tbl

