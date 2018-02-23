#encoding:utf8
from buildarea import dobj,rndarea
from vdgt import *
from model import *

class obj2():
    def __init__(self,  **kw ):
        for k,v in kw.items():
            setattr( self, k, v)
            
def gettbl( nameorid ):
    r = getitem("_tbl",nameorid)
    if r == None:
        r = getitembyname( "_tbl", nameorid )
    return r

def getjob( name ):
    return getitembyname( "_job", name )

def QueryObj( sql ):
    result = conn.execute(sql).fetchall()
    ret = []
    for row in result:
        r = obj();
        for t in row.items():
            setattr( r, t[0], t[1])
        ret.append(r)
    return ret;

# 生成案件处理数据
#先把各角色代表用户及其单位找出来
roleusers = QueryObj( "select min(id) as id, account, name, job, depart_id, depart_table, face from user group by job")
for u in [x for x in roleusers if x.depart_table != 0]:
    tbl = gettbl(u.depart_table)
    u.depart = QueryObj( "select * from "+tbl.name+" where id="+str(u.depart_id))[0]
    if tbl.name == "winder":
        u.sub = QueryObj( "select id, name from winderarea where winder_id="+str(u.depart_id))
def GetUser( job ):
    jobid = int(getjob(job).id)
    for u in roleusers:
        if u.job == jobid:
            return u
    raise KeyError

#各种需要的数据
winder = QueryObj( "select * from winder where id="+str(GetUser("风场主管").depart_id) )[0]
winder.leader = GetUser("风场主管")
winder.clerks = QueryObj( "select * from user where depart_table="+str(gettbl("winder").id) + " and depart_id="+str(winder.id) )
winder.efans = QueryObj( "select * from efan where winder_id="+str(winder.id) )
winder.leafs = QueryObj( "select * from leaf where winder_id="+str(winder.id) )
guides = QueryObj( "select * from user where job="+str(getjob("调度").id) )
devwh = QueryObj( "select * from devwh where id="+str(GetUser("驻地主管").depart_id) )[0]
devwh.leader = GetUser("驻地主管")
devwh.clerks = QueryObj( "select * from user where depart_table="+str(gettbl("devwh").id) + " and depart_id="+str(devwh.id) )
devwh.devs = QueryObj( "select * from dev where devwh_id="+str(devwh.id ))

#生成30个故障报告，并把它们找出来
conn.execute(tbl_fault.insert(),[dict_fault(random.choice(winder.clerks)) for i in range(30)])
faults = QueryObj( "select * from fault")

def create_devwork(fault):
    devworks=[]
    for c in range(rndnum(2,5)):
        dev = random.choice(devwh.devs)
        devworks.append( dict(status=2,	#状态 0:编辑、1:提交、2受理 -1拒绝
            fault_id=fault.id,	#故障单号
            guide_id=fault.guide_id,	#发单人
            guidedt=rnddatespan(fault.guidetime,0,1),	#发单时间
            clss=int(random.choice(data("_devclss").data)[0]),	#设备分类
            devwh_id=devwh.id,	#所属驻地
            timelen=rndnum(3,5),	#预计工期
            winder_id=winder.id,	#任务风场
            addr=winder.addr,	#任务地址
            remark=rnditem("_songci"),	#备注
            deal_id=devwh.leader.id,	#接单人
            dealdt=rnddatespan(fault.guidetime,1,2),	#接单时间
            dev_id=dev.id,	#调用设备
            driver_id=dev.driver_id,	#司机
        ))
    conn.execute(tbl_devwork.insert(),devworks)

for i, fault in enumerate(faults):
    if i < 5:#前5个作为未提交状态
        continue
    
    cols = {}
    if  i==5 or i==6: 
        cols["status"]=1    #1已提交(调度可看到) 2个
    
    if 7<=i<=13:
        cols["status"]=2  #2已受理(正在评估)
    if i>=7:#受理人
        cols[ "guide_id"]=random.choice(guides).id
        cols["guidetime"]=rnddatespan(fault.reporttime,0,1)
    if i>=8:#专家组
        pass
    if i>=9:#评估报告
        pass
    if i>=10:#维修方案（0人签字）
        pass
    if i>=11:#维修方案（1人签字）
        pass
    if i>=12:#维修方案（2人签字）
        pass
    if i>=13:#维修方案（3人签字）
        pass
    
    if 14<=i<=17:
        cols[ "status"] = 3  #3正在维修（维修方案完成）
        
    if i>=14:#维修队
        pass
    if i>=15:#维修用料单
        pass
    if i>=16:#设备调用单
        create_devwork(fault)
    if i>=17:#维修记录
        pass

    if 18<=i<=19:
        cols[ "status"] = 4  #4即将完成(开始编写维修报告)
    if i>=18:#维修报告（0人签字）
        pass
    if i>=19:#维修报告（1人签字）
        pass

    if i == 20:
        cols[ "status"] = 5  #5已完成(维修报告完成)
    if i>=20:#维修报告（2人签字）
        pass

    if 21<=i<=22:
        cols["status"] = 6  #6提醒付款

    if 23<=i:
        cols["status"] = 7  #7冻结

    sql = "update fault set " + ",".join([k+"='"+str(v)+"'" for k,v in cols.items()])+ " where id="+ str(fault.id)
    conn.execute(sql)

#查询调度人员列表
#随机选取几个风机和叶片，生成报修单 未提交状态3个 已受理1个
#（已评估，在维修状态）、， 计13个
#随机选取2/4报修单，再随机选择调度人员接单（已评估，在维修状态）、已完成10个
#合计27个。

def gen_matin(): #0编辑(正在签收) 1等待审批 2等待入库 3完成 -1退回
    matwh = QueryObj( "select * from matwh where id="+str(GetUser("仓库主管").depart_id) )[0]
    leader = GetUser("仓库主管")
    clerk = GetUser("仓库管理员")
    mats = QueryObj( "select * from mat")

    matins = []
    for i in range(rndnum(3,6)): # 为clerk创建3-6个正在编辑的入库单
        matin = obj2()
        matin.main = obj2(matwh_id=matwh.id, status = 0)
        matin.recs = [obj2(matwh_id=matwh.id,matin_id=-1) for x in range(rndnum(3,6))]
        matin.flows = [obj2(table_id=gettbl("matin").id,record_id=-1,status=0,user_id=clerk.id, remark="创建入库单")]
        matins.append(matin)
    for i in range(rndnum(3,6)): # 为clerk创建3-6个等待审批的入库单
        matin = obj2()
        matin.main = obj2(matwh_id=matwh.id,status = 1)
        matin.recs = [obj2(matwh_id=matwh.id,matin_id=-1) for x in range(rndnum(3,6))]
        matin.flows = [obj2(table_id=gettbl("matin").id,record_id=-1,status=0,user_id=clerk.id,remark="创建入库单"),
                        obj2(table_id=gettbl("matin").id,record_id=-1,status=1,user_id=clerk.id,remark="提交入库单")]
        matins.append(matin)
    for i in range(rndnum(3,6)): # 为clerk创建3-6个等待入库的入库单
        matin = obj2()
        matin.main = obj2(matwh_id=matwh.id,status = 2)
        matin.recs = [obj2(matwh_id=matwh.id,matin_id=-1) for x in range(rndnum(3,6))]
        matin.flows = [obj2(table_id=gettbl("matin").id,record_id=-1,status=0,user_id=clerk.id,remark="创建入库单"),
                        obj2(table_id=gettbl("matin").id,record_id=-1,status=1,user_id=clerk.id,remark="提交入库单"),
                        obj2(table_id=gettbl("matin").id,record_id=-1,status=2,user_id=leader.id,remark="审批通过入库单")]
        matins.append(matin)
    for i in range(rndnum(3,6)): # 为clerk创建3-6个审批退回的入库单
        matin = obj2()
        matin.main = obj2(matwh_id=matwh.id,status = -1)
        matin.recs = [obj2(matwh_id=matwh.id,matin_id=-1) for x in range(rndnum(3,6))]
        matin.flows = [obj2(table_id=gettbl("matin").id,record_id=-1,status=0,user_id=clerk.id,remark="创建入库单"), #编辑
                        obj2(table_id=gettbl("matin").id,record_id=-1,status=1,user_id=clerk.id,remark="提交入库单"), #提交
                        obj2(table_id=gettbl("matin").id,record_id=-1,status=-1,user_id=leader.id,remark="审批退回入库单")]#审批退回
        matins.append(matin)
    for i in range(rndnum(40,60)): # 为clerk创建40-60个完成的入库单
        matin = obj2()
        matin.main = obj2(matwh_id=matwh.id,status = 3)
        matin.recs = [obj2(matwh_id=matwh.id,matin_id=-1) for x in range(rndnum(3,6))]
        matin.flows = [obj2(table_id=gettbl("matin").id,record_id=-1,status=0,user_id=clerk.id,remark="创建入库单"), #编辑
                        obj2(table_id=gettbl("matin").id,record_id=-1,status=1,user_id=clerk.id,remark="提交入库单"), #提交
                        obj2(table_id=gettbl("matin").id,record_id=-1,status=2,user_id=leader.id,remark="审批通过入库单"),#审批
                        obj2(table_id=gettbl("matin").id,record_id=-1,status=3,user_id=clerk.id,remark="入库单完成入库")] #入库
        matins.append(matin)

    for i,x in enumerate(matins):
        for y in x.flows:
            y.record_id=i+1
        for y in x.recs:
            y.matin_id=i+1
    conn.execute(tbl_matin.insert(),[dict_matin(x.main) for x in matins])
    conn.execute(tbl_matinrec.insert(),[dict_matinrec(y.matwh_id,y.matin_id) for x in matins for y in x.recs ])
    conn.execute(tbl_flow.insert(),[dict_flow(y) for x in matins for y in x.flows ])
gen_matin()

def gen_matout(): #0编辑(正在签收) 1等待审批 2等待入库 3完成 -1退回
    matwh = QueryObj( "select * from matwh where id="+str(GetUser("仓库主管").depart_id) )[0]
    leader = GetUser("仓库主管")
    clerk = GetUser("仓库管理员")
    guide = GetUser("调度")

    #找到已完成的入库记录，并将每条随机切分
    mats = QueryObj( "select matinrec.id as id,mat_id,num from matinrec,matin where matinrec.matin_id==matin.id and matin.status==3")
    matos=[obj2(matinrec_id=x.id,mat_id=x.mat_id,num=y) for x in mats for y in rndsplit(x.num, 1,6)]
    index= [x for x in range(len(matos))]

    tbl_id=gettbl("matout").id
    matouts = []    #0编辑(调度创建) 1调度提交等待备货 2库管正在备货或库管创建) 3库管提交等待审批 4主管审批通过等待出库 5入库完成 -1退回
    for i in range(rndnum(3,6)): # 为guide创建3-6个正在备货的出库单
        matout = obj2()
        matout.main = obj2(fault_id=10000, fault_code="10000",matwh_id=matwh.id, status=2,usage="维修用料")
        matout.recs = [obj2(matwh_id=matwh.id,matout_id=len(matouts)+1,mat_id=x.mat_id,num=x.num, matinrec_id=x.matinrec_id) for x in rndpick(matos,index, rndnum(3,6))]
        matout.flows = [obj2(table_id=tbl_id,record_id=len(matouts)+1,status=0,user_id=guide.id,remark="调度创建出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=1,user_id=guide.id,remark="调度提交出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=2,user_id=clerk.id,remark="备货出库单")]
        matouts.append(matout)
    for i in range(rndnum(3,6)): # 为clerk创建3-6个等待备货的出库单
        matout = obj2()
        matout.main = obj2(fault_id=0, fault_code="",matwh_id=matwh.id, status=2,usage="调货")
        matout.recs = [obj2(matwh_id=matwh.id,matout_id=len(matouts)+1,mat_id=x.mat_id,num=x.num, matinrec_id=x.matinrec_id) for x in rndpick(matos,index, rndnum(3,6))]
        matout.flows = [obj2(table_id=tbl_id,record_id=len(matouts)+1,status=0,user_id=clerk.id,remark="库管创建出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=2,user_id=clerk.id,remark="库管开始备货")]
        matouts.append(matout)
    for i in range(rndnum(3,6)): # 为clerk创建3-6个等待审批的出库单
        matout = obj2()
        matout.main = obj2(fault_id=0, fault_code="",matwh_id=matwh.id, status=3,usage="调货")
        matout.recs = [obj2(matwh_id=matwh.id,matout_id=len(matouts)+1,mat_id=x.mat_id,num=x.num, matinrec_id=x.matinrec_id) for x in rndpick(matos,index, rndnum(3,6))]
        matout.flows = [obj2(table_id=tbl_id,record_id=len(matouts)+1,status=0,user_id=clerk.id,remark="库管创建出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=2,user_id=clerk.id,remark="库管开始备货"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=3,user_id=clerk.id,remark="提交审批出库单")]
        matouts.append(matout)
    for i in range(rndnum(3,6)): # 为clerk创建3-6个审批退回的出库单
        matout = obj2()
        matout.main = obj2(fault_id=0, fault_code="",matwh_id=matwh.id, status=-1,usage="调货")
        matout.recs = [obj2(matwh_id=matwh.id,matout_id=len(matouts)+1,mat_id=x.mat_id,num=x.num, matinrec_id=x.matinrec_id) for x in rndpick(matos,index, rndnum(3,6))]
        matout.flows = [obj2(table_id=tbl_id,record_id=len(matouts)+1,status=0,user_id=clerk.id,remark="库管创建出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=2,user_id=clerk.id,remark="库管开始备货"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=3,user_id=clerk.id,remark="提交审批出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=-1,user_id=leader.id,remark="审批退回出库单"),]
        matouts.append(matout)
    for i in range(rndnum(3,6)): # 为clerk创建3-6个审批通过的出库单
        matout = obj2()
        matout.main = obj2(fault_id=0, fault_code="",matwh_id=matwh.id, status=4,usage="调货")
        matout.recs = [obj2(matwh_id=matwh.id,matout_id=len(matouts)+1,mat_id=x.mat_id,num=x.num, matinrec_id=x.matinrec_id) for x in rndpick(matos,index, rndnum(3,6))]
        matout.flows = [obj2(table_id=tbl_id,record_id=len(matouts)+1,status=0,user_id=clerk.id,remark="库管创建出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=2,user_id=clerk.id,remark="库管开始备货"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=3,user_id=clerk.id,remark="提交审批出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=4,user_id=leader.id,remark="审批通过出库单"),]
        matouts.append(matout)
    for i in range(rndnum(3,6)): # 为clerk创建3-6个出库完成的出库单
        matout = obj2()
        matout.main = obj2(fault_id=0, fault_code="",matwh_id=matwh.id, status=5,usage="调货")
        matout.recs = [obj2(matwh_id=matwh.id,matout_id=len(matouts)+1,mat_id=x.mat_id,num=x.num, matinrec_id=x.matinrec_id) for x in rndpick(matos,index, rndnum(3,6))]
        matout.flows = [obj2(table_id=tbl_id,record_id=len(matouts)+1,status=0,user_id=clerk.id,remark="库管创建出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=2,user_id=clerk.id,remark="库管开始备货"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=3,user_id=clerk.id,remark="提交审批出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=4,user_id=leader.id,remark="审批通过出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=5,user_id=clerk.id,remark="发货完毕"),]
        matouts.append(matout)
    for i in range(rndnum(20,30)): # 为clerk创建3-6个已确认收货的出库单
        matout = obj2()
        matout.main = obj2(fault_id=0, fault_code="",matwh_id=matwh.id, status=6,usage="调货")
        matout.recs = [obj2(matwh_id=matwh.id,matout_id=len(matouts)+1,mat_id=x.mat_id,num=x.num, matinrec_id=x.matinrec_id) for x in rndpick(matos,index, rndnum(3,6))]
        matout.flows = [obj2(table_id=tbl_id,record_id=len(matouts)+1,status=0,user_id=clerk.id,remark="库管创建出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=2,user_id=clerk.id,remark="库管开始备货"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=3,user_id=clerk.id,remark="提交审批出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=4,user_id=leader.id,remark="审批通过出库单"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=5,user_id=clerk.id,remark="发货完毕"),
                        obj2(table_id=tbl_id,record_id=len(matouts)+1,status=6,user_id=clerk.id,remark="对方确认收货"),]
        matouts.append(matout)
    conn.execute(tbl_matout.insert(),[dict_matout(x.main) for x in matouts])
    conn.execute(tbl_matoutrec.insert(),[dict_matoutrec(y) for x in matouts for y in x.recs ])
    conn.execute(tbl_flow.insert(),[dict_flow(y) for x in matouts for y in x.flows ])
gen_matout()

#创建库存视图
creat_store_view='''CREATE VIEW store_view AS
    SELECT *
      FROM (
               SELECT matinrec.*
                 FROM matinrec,
                      matin
                WHERE matinrec.matin_id = matin.id AND 
                      matin.status = 3
           )
           AS inrec
           LEFT JOIN
           (
               SELECT matinrec_id,
                      sum(num) AS outnum
                 FROM matoutrec,
                      matout
                WHERE matoutrec.matout_id = matout.id AND 
                      matout.status >= 3
                GROUP BY matinrec_id
           )
           AS outrec ON inrec.id = outrec.matinrec_id;
'''
conn.execute(creat_store_view)

##创建正在出库视图
#createview_matouting='''CREATE VIEW matouting AS
#    SELECT matout.*,
#           creater.user_id AS creater_id,
#           creater.date AS createdate,
#           stocker.user_id AS stocker_id,
#           stocker.date AS stockdate
#      FROM matout
#           LEFT JOIN flow AS creater ON (creater.table_id = 28 AND creater.record_id = matout.id AND creater.status = 0) 
#           LEFT JOIN flow AS stocker ON (stocker.table_id = 28 AND stocker.record_id = matout.id AND stocker.status = 2) 
#     WHERE matout.status IN (2, 3, 4, 5)'''
#conn.execute(createview_matouting)

print("haha!")