#encoding:utf8
from buildarea import dobj,rndarea
from vdgt import *
from model import *

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


