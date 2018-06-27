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

#先把各角色代表用户及其单位找出来
roleusers = QueryObj( "select min(id) as id, account, name, job, depart_id, depart_table, face from user group by job")
for u in [x for x in roleusers if x.depart_table != 0 and x.depart_table != None ]:
    tbl = gettbl(u.depart_table)
    u.depart = QueryObj( "select * from "+tbl.name+" where id="+str(u.depart_id))[0]
    if tbl.name == "winder":
        u.sub = QueryObj( "select id, name from winderarea where winder_id="+str(u.depart_id))
def GetUser( job ):
    jobid = int(float(getjob(job).id))
    for u in roleusers:
        if u.job == jobid:
            return u
    raise KeyError

def create_team():
    leaders = QueryObj( "select * from user where job="+intstr(getjob( "维修队长" ).id))
    skillers = QueryObj( "select * from user where job="+intstr(getjob( "技工" ).id))
    conn.execute(tbl_link.insert(),[ dict_link(obj2(type="team",a_id=random.choice(leaders).id,b_id=x.id,remark="", date=rnddate(30,60))) for x in skillers])
create_team()

#生成入库单数据
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

matos=[] #后面生成案件数据时要用
index=[]
matoutcount=0
#生成出库单数据
def gen_matout(): #0编辑(正在签收) 1等待审批 2等待入库 3完成 -1退回
    matwh = QueryObj( "select * from matwh where id="+str(GetUser("仓库主管").depart_id) )[0]
    leader = GetUser("仓库主管")
    clerk = GetUser("仓库管理员")
    guide = GetUser("调度")

    #找到已完成的入库记录，并将每条随机切分
    global matos,index,matoutcount;
    mats = QueryObj( "select matinrec.id as id,mat_id,num from matinrec,matin where matinrec.matin_id==matin.id and matin.status==3")
    matos=[obj2(matinrec_id=x.id,mat_id=x.mat_id,num=y) for x in mats for y in rndsplit(x.num, 2,6)]
    index= [x for x in range(len(matos))]

    tbl_id=gettbl("matout").id
    matouts = []    #0编辑(调度创建) 1调度提交等待备货 2库管正在备货或库管创建) 3库管提交等待审批 4主管审批通过等待出库 5出库完成 -1退回
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
    for i in range(rndnum(3,6)): # 为clerk创建3-6个已确认收货的出库单
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
    matoutcount = len(matouts)
    conn.execute(tbl_matout.insert(),[dict_matout(x.main) for x in matouts])
    conn.execute(tbl_matoutrec.insert(),[dict_matoutrec(y) for x in matouts for y in x.recs ])
    conn.execute(tbl_flow.insert(),[dict_flow(y) for x in matouts for y in x.flows ])
gen_matout()

# 生成案件处理数据
#查询调度人员列表
#随机选取几个风机和叶片，生成报修单 未提交状态3个 已受理1个
#（已评估，在维修状态）、， 计13个
#随机选取2/4报修单，再随机选择调度人员接单（已评估，在维修状态）、已完成10个
#合计27个。
class gen_case():
    def __init__(self):
        #各种需要的数据
        self.winder = QueryObj( "select * from winder where id="+intstr(GetUser("风场主管").depart_id) )[0]
        self.winder.leader = GetUser("风场主管")
        self.winder.clerks = QueryObj( "select * from user where depart_table="+intstr(gettbl("winder").id) + " and depart_id="+intstr(self.winder.id) )
        self.winder.winderareas = QueryObj( "select * from winderarea where winder_id="+intstr(self.winder.id) )
        self.winder.efans = QueryObj( "select * from efan where winderarea_id="+intstr(self.winder.winderareas[0].id) )
        self.winder.leafs = QueryObj( "select * from leaf where winderarea_id="+intstr(self.winder.winderareas[0].id) )
        #self.guides = QueryObj( "select * from user where job="+intstr(getjob("调度").id) )
        self.experts = QueryObj( "select * from user where job="+intstr(getjob("专家").id) )
        self.teams = QueryObj( '''select * from user where id in ( select b_id from link where type ='team' and a_id = {0})'''.format(GetUser("维修队长").id) )
        self.devwh = QueryObj( "select * from devwh where id="+intstr(GetUser("驻地主管").depart_id) )[0]
        self.devwh.leader = GetUser("驻地主管")
        self.devwh.clerks = QueryObj( "select * from user where depart_table="+intstr(gettbl("devwh").id) + " and depart_id="+intstr(self.devwh.id))
        self.devwh.devs = QueryObj( "select * from dev where devwh_id="+intstr(self.devwh.id))
        self.matwh = QueryObj( "select * from matwh where id="+intstr(GetUser("仓库主管").depart_id))[0]
        self.matwh.leader = GetUser("仓库主管")
        self.matwh.clerks = QueryObj( "select * from user where depart_table="+intstr(gettbl("matwh").id) + " and depart_id="+intstr(self.matwh.id))

        #生成30个故障报告，并把它们找出来
        conn.execute(tbl_fault.insert(),[dict_fault(random.choice(self.winder.clerks)) for i in range(30)])
        self.faults = QueryObj( "select * from fault")

    def create_matout( self,fault, status ):
        global matoutcount
        matoutcount +=1
        tbl_id=gettbl("matout").id
        stocker_id = random.choice(self.matwh.clerks).id
        flows = [
            obj2(table_id=tbl_id,record_id=matoutcount,status=0,user_id=fault.guide_id,remark="调度创建出库单"),
            obj2(table_id=tbl_id,record_id=matoutcount,status=1,user_id=fault.guide_id,remark="调度提交出库单"),
            obj2(table_id=tbl_id,record_id=matoutcount,status=2,user_id=stocker_id,remark="库管开始备货"),
            obj2(table_id=tbl_id,record_id=matoutcount,status=3,user_id=stocker_id,remark="提交审批出库单"),
            obj2(table_id=tbl_id,record_id=matoutcount,status=4,user_id=self.matwh.leader.id,remark="审批通过出库单"),
            obj2(table_id=tbl_id,record_id=matoutcount,status=5,user_id=stocker_id,remark="发货完毕"),
            obj2(table_id=tbl_id,record_id=matoutcount,status=6,user_id=stocker_id,remark="对方确认收货")]
        rej = obj2(table_id=tbl_id,record_id=matoutcount,status=-1,user_id=self.matwh.leader.id,remark="审批退回出库单")

        matout = obj2()
        matout.main = obj2(fault_id=fault.id, fault_code=fault.code,matwh_id=self.matwh.id, status=0,usage="维修用料")
        matout.recs = [obj2(matwh_id=self.matwh.id,matout_id=matoutcount,mat_id=x.mat_id,num=x.num, matinrec_id=x.matinrec_id) for x in rndpick(matos,index, rndnum(3,6))]
        if status == -1:
            matout.flows = flows[0:4]
            matout.flows.append(rej)
        else:
            matout.flows = flows[0:(status+1)]
        return matout;

    #创建设备调用单
    def create_devwork(self,fault):
        devworks=[]
        for c in range(rndnum(2,5)):
            dev = random.choice(self.devwh.devs)
            devworks.append( dict(status=2,	#状态 0:编辑、1:提交、2受理 -1拒绝
                fault_id=fault.id,	#故障单号
                guide_id=fault.guide_id,	#发单人
                guidedt=rnddatespan(fault.guidetime,0,1),	#发单时间
                clss=int(float(random.choice(data("_devclss").data)[0])),	#设备分类
                devwh_id=self.devwh.id,	#所属驻地
                timelen=rndnum(3,5),	#预计工期
                winder_id=self.winder.id,	#任务风场
                addr=self.winder.addr,	#任务地址
                remark=rnditem("_songci"),	#备注
                deal_id=self.devwh.leader.id,	#接单人
                dealdt=rnddatespan(fault.guidetime,1,2),	#接单时间
                dev_id=dev.id,	#调用设备
                driver_id=dev.driver_id,	#司机
            ))
        conn.execute(tbl_devwork.insert(),devworks)

    def add_data(self,tbl, rec):
        if type(rec) == type([]):
            if tbl == "link":
                conn.execute(tbl_link.insert(),[ dict_link(x) for x in rec])
            elif tbl == "addit":
                conn.execute(tbl_addit.insert(),[ dict_addit(x) for x in rec])
        else:
            if tbl == "link":
                conn.execute(tbl_link.insert(),dict_link(rec))
            elif tbl == "addit":
                conn.execute(tbl_addit.insert(),dict_addit(rec))


    def create_case(self):
        guideleader = GetUser("调度主管")
        guider = GetUser("调度")
        teamleader = GetUser("维修队长")
        damageimg=["img/winder/winder1.jpg", "img/winder/winder2.jpg", "img/winder/winder3.jpg", "img/winder/winder4.jpg", "img/winder/winder5.jpg", "img/winder/winder6.jpg", "img/winder/winder7.jpg", "img/winder/winder8.jpg", "img/winder/winder9.jpg", "img/winder/winder10.jpg", "img/winder/winder11.jpg"]
        for i, fault in enumerate(self.faults):
            experts = random.sample(self.experts, rndnum(4,8))
            teamsize= rndnum(3,5)
            if teamsize > len(self.teams):
                teamsize =len(self.teams)
            repairteam = random.sample(self.teams, teamsize)
            eval1reps = [] #评估报告
            eval2reps = [] #二评报告
            repairprogs = [] #维修方案
            repairreps =[] #维修报告

            #报告哪些设备要维修
            conn.execute(tbl_link.insert(),[ dict_link(obj2(type="f_devices",a_id=fault.id, b_id=random.choice(self.winder.efans).id,remark="",date=rnddate(30,60))) for x in range(3,8)])
            if i < 5:#前5个作为未提交状态
                continue
    
            cols = {}
            if  i==5 or i==6: 
                cols["status"]=1    #1已提交(调度可看到) 2个

            if 7<=i<=13:
                cols["status"]=2  #2已受理(正在评估)
            if i>=7:#受理人
                cols[ "guide_id"]=random.choice([guideleader.id,guider.id])
                cols["guidetime"]=rnddatespan(fault.reporttime,0,1)
                fault.guide_id = cols[ "guide_id"]
                fault.guidetime = cols[ "guidetime"]
            if i>=8:#专家组
                conn.execute(tbl_link.insert(),[ dict_link(obj2(type="f_experts",a_id=fault.id, b_id=x.id,remark="", date=rnddatespan(fault.reporttime,1,2))) for x in experts])
            if i>=9:#评估报告
                for x in range(2,5):
                    expert = random.choice(experts)
                    date = rnddatespan(fault.reporttime,2,4)
                    name = "评估报告_"+expert.name+"_" + date.strftime("%m-%d %H:%M")
                    eval1reps.append( obj2(type="eval1rep",ref_id=fault.id, name=name, remark="", user_id=expert.id, date=date ))
                self.add_data("addit",eval1reps)
                if i%2 == 0:
                    for x in range(2,5):
                        expert = random.choice(experts)
                        date = rnddatespan(fault.reporttime,5,8)
                        name = "二评报告_"+expert.name+"_" + date.strftime("%m-%d %H:%M")
                        eval2reps.append( obj2(type="eval2rep",ref_id=fault.id, name=name, remark="", user_id=expert.id, date=date ))
                    self.add_data("addit",eval2reps)
            if i>=10:#维修方案（0人签字）
                for x in range(2,5):
                    user = random.choice([guideleader,guider])
                    date = rnddatespan(fault.reporttime,8,10)
                    name = "维修方案_"+user.name+"_" + date.strftime("%m-%d %H:%M")
                    repairprogs.append( obj2(type="repairprog",ref_id=fault.id, name=name, remark="", user_id=user.id, date=date ))
                self.add_data("addit",repairprogs)
                repairprogs = QueryObj( "select * from addit where type='repairprog' and ref_id="+intstr(fault.id) )
            if i>=11:#维修方案（调度主管签字）
                conn.execute(tbl_link.insert(),dict_link(obj2(type="conform",a_id=random.choice(repairprogs).id, \
                    b_id=guideleader.id, name="", remark="", date=rnddatespan(fault.reporttime,11,12) )))
            if i>=12:#维修方案（驻场签字）
                conn.execute(tbl_link.insert(),dict_link(obj2(type="conform",a_id=random.choice(repairprogs).id, 
                    b_id=random.choice(self.winder.clerks).id, name="", remark="", date=rnddatespan(fault.reporttime,12,13) )))
            if i>=13:#维修方案（风场主管签字）
                conn.execute(tbl_link.insert(),dict_link(obj2(type="conform",a_id=random.choice(repairprogs).id, 
                    b_id=self.winder.leader.id, name="", remark="", date=rnddatespan(fault.reporttime,13,14) )))
    
            if 14<=i<=17:
                cols[ "status"] = 3  #3正在维修（维修方案完成）
        
            if i>=14:#维修队
                self.add_data("link", [ obj2(type="f_team",a_id=fault.id, b_id=x.id, name="", remark="", date=rnddatespan(fault.reporttime,10,14) ) for x in repairteam])
            if i>=15:#维修用料单（8种状态各一个）
                matouts = [self.create_matout( fault, status) for status in [0,1,2,3,-1,4,5,6]]
                conn.execute(tbl_matout.insert(),[dict_matout(x.main) for x in matouts])
                conn.execute(tbl_matoutrec.insert(),[dict_matoutrec(y) for x in matouts for y in x.recs ])
                conn.execute(tbl_flow.insert(),[dict_flow(y) for x in matouts for y in x.flows ])
            if i>=16:#设备调用单
                self.create_devwork(fault)
            if i>=17:#维修记录(图片部分直至最后再添加)
                repairlogs = []
                for x in range(2,5):
                    mender = random.choice(repairteam)
                    date = rnddatespan(fault.reporttime,15,18)
                    repairlogs.append( obj2(type="repairlog",ref_id=fault.id, name="", remark="", user_id=mender.id, date=date ))
                self.add_data("addit",repairlogs)

            if 18<=i<=19:
                cols[ "status"] = 4  #4即将完成(开始编写维修报告)
            if i>=18:#维修报告
                for x in range(2,5):
                    user = random.choice([guideleader,guider])
                    date = rnddatespan(fault.reporttime,19,20)
                    name = "维修报告_"+user.name+"_" + date.strftime("%m-%d %H:%M")
                    repairreps.append( obj2(type="repairrep",ref_id=fault.id, name=name, remark="", user_id=teamleader.id, date=date ))
                self.add_data("addit",repairreps)
                repairreps = QueryObj( "select * from addit where type='repairrep' and ref_id="+intstr(fault.id) )

                #维修队长签字
                conn.execute(tbl_link.insert(),dict_link(obj2(type="conform",a_id=random.choice(repairreps).id, 
                    b_id=teamleader.id, name="", remark="", date=rnddatespan(fault.reporttime,21,22) )))
            if i>=19:#维修报告（驻场签字）
                conn.execute(tbl_link.insert(),dict_link(obj2(type="conform",a_id=random.choice(repairreps).id, 
                    b_id=random.choice(self.winder.clerks).id, name="", remark="", date=rnddatespan(fault.reporttime,21,22) )))

            if i == 20:
                cols[ "status"] = 5  #5已完成(维修报告完成,提醒付款阶段)
                conn.execute(tbl_flow.insert(),dict_flow(obj2(table_id=gettbl("fault").id,record_id=fault.id,status=5,user_id=fault.guide_id, remark="案件处理结束")))
            if 21<=i<=22:
                cols["status"] = 6  #6已付款，冻结
                conn.execute(tbl_flow.insert(),dict_flow(obj2(table_id=gettbl("fault").id,record_id=fault.id,status=5,user_id=fault.guide_id, remark="付款完成")))

            #为所有的维修记录增加图片
            repairlogs = QueryObj( "select * from addit where type='repairlog' and ref_id="+intstr(fault.id))
            if len(repairlogs)>0:
                self.add_data("addit", [obj2(type="repairrep",ref_id=x.id, name=random.choice(damageimg), remark="", user_id=random.choice(repairteam).id, date=datetime.datetime.strptime(x.date,"%Y-%m-%d") ) for x in repairlogs for y in range(3,5)])
            
            #聊天成员
            chatmans=[guideleader,guider,teamleader]+experts +repairteam+ self.winder.clerks
            self.add_data( "link",[obj2(type="chatman",a_id=fault.id, b_id=x.id, name="", remark="", date=rnddatespan(fault.reporttime,10,14) ) for x in chatmans])
            #聊天记录
            conn.execute(tbl_chat.insert(),[dict_chat(obj2(fault_id=fault.id,user_id=random.choice(chatmans).id, say=rnditem("_songci"),date=rnddatespan(fault.reporttime,3,20))) for i in range(rndnum(30,50))])

            #更新报修单
            self.add_data("addit", [obj2(type="faultspot",ref_id=fault.id, name=random.choice(damageimg), remark="", user_id=random.choice(repairteam).id, date=datetime.datetime.strptime(fault.reporttime,'%Y-%m-%d') ) for x in range(3,5)])
            sql = "update fault set " + ",".join([k+"='"+str(v)+"'" for k,v in cols.items()])+ " where id="+ intstr(fault.id)
            conn.execute(sql)

gc=gen_case()
gc.create_case()


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

#刷数据库
#1.红蓝分不在列表显示
#2.prof不能保存
#3.文章brief显示
#4.用户动态显示
#5.efanvender_id和leafvender_id改为vender_id


#地图：

#树+内容
