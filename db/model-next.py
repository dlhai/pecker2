#encoding:utf8
from buildarea import dobj,rndarea
from vdgt import *
from model import *

db_tbl = [
    { "id": "0", "name": "none", "title": "占位" },
    { "id": "1", "name": "base", "title": "定义" },
    { "id": "2", "name": "link", "title": "一对多引用" },
    { "id": "3", "name": "addit", "title": "附件" },
    { "id": "4", "name": "config", "title": "配置信息" },
    { "id": "5", "name": "admarea", "title": "行政区划" },
    { "id": "6", "name": "user", "title": "供应商" },
    { "id": "7", "name": "certif", "title": "人员" },
    { "id": "8", "name": "edu", "title": "证件信息" },
    { "id": "9", "name": "employ", "title": "受教育经历" },
    { "id": "10", "name": "opus", "title": "就业经历" },
    { "id": "11", "name": "vender", "title": "发表作品" },
    { "id": "12", "name": "wait", "title": "" },
    { "id": "13", "name": "winderco", "title": "风电企业" },
    { "id": "14", "name": "winderprov", "title": "省区" },
    { "id": "15", "name": "winder", "title": "风场" },
    { "id": "16", "name": "winderarea", "title": "风区" },
    { "id": "17", "name": "efan", "title": "风机" },
    { "id": "18", "name": "leaf", "title": "叶片" },
    { "id": "19", "name": "fltrep", "title": "报修" },
    { "id": "20", "name": "devwh", "title": "设备驻地" },
    { "id": "21", "name": "dev", "title": "设备" },
]
def gettbl( nameorid ):
    s = str(nameorid)
    for x in db_tbl:
        if x["name"] == s or x['id'] == s:
            return x
    raise KeyError

db_job = [
    { "id": "1", "type": "winder", "name": "叶片超级帐号" },
    { "id": "2", "type": "", "name": "风场主管" },
    { "id": "3", "type": "", "name": "驻场" },
    { "id": "4", "type": "", "name": "设备超级帐号" },
    { "id": "5", "type": "devwh", "name": "驻地主管" },
    { "id": "6", "type": "devwh", "name": "设备司机" },
    { "id": "7", "type": "su", "name": "仓库超级帐号" },
    { "id": "8", "type": "", "name": "仓库主管" },
    { "id": "9", "type": "", "name": "仓库管理员" },
    { "id": "10", "type": "su", "name": "调度超级帐号" },
    { "id": "11", "type": "", "name": "调度主管" },
    { "id": "12", "type": "", "name": "调度" },
    { "id": "13", "type": "su", "name": "专家超级帐号" },
    { "id": "14", "type": "", "name": "专家" },
    { "id": "15", "type": "su", "name": "技工超级帐号" },
    { "id": "16", "type": "", "name": "维修队长" },
    { "id": "17", "type": "", "name": "技工" },
    { "id": "18", "type": "", "name": "公众" },
]
def getjob( name ):
    for x in db_job:
        if x["name"] == name:
            return x["id"]
    raise KeyError

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
    u.depart = QueryObj( "select * from "+tbl["name"]+" where id="+str(u.depart_id))[0]
    if tbl["name"] == "winder":
        u.sub = QueryObj( "select id, name from winderarea where winder_id="+str(u.depart_id))
def GetUser( job ):
    jobid = int(getjob(job))
    for u in roleusers:
        if u.job == jobid:
            return u
    raise KeyError

#各种需要的数据
winder = QueryObj( "select * from winder where id="+str(GetUser("风场主管").depart_id) )[0]
winder.leader = GetUser("风场主管")
winder.clerks = QueryObj( "select * from user where depart_table="+str(gettbl("winder")["id"]) + " and depart_id="+str(winder.id) )
winder.efans = QueryObj( "select * from efan where winder_id="+str(winder.id) )
winder.leafs = QueryObj( "select * from leaf where winder_id="+str(winder.id) )
guides = QueryObj( "select * from user where job="+str(getjob("调度")) )
devwh = QueryObj( "select * from devwh where id="+str(GetUser("驻地主管").depart_id) )[0]
devwh.leader = GetUser("驻地主管")
devwh.clerks = QueryObj( "select * from user where depart_table="+str(gettbl("devwh")["id"]) + " and depart_id="+str(devwh.id) )
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
            guide= fault.guide,	#发单人
            guidedt=rnddatespan(fault.guidetime,0,1),	#发单时间
            clss=int(random.choice(data("_devclss").data)[0]),	#设备分类
            devwh_id=devwh.id,	#所属驻地
            timelen=rndnum(3,5),	#预计工期
            winder_id=winder.id,	#任务风场
            addr=winder.addr,	#任务地址
            remark=rnditem("_songci"),	#备注
            devwhsu=devwh.leader.id,	#接单人
            devwhsudt=rnddatespan(fault.guidetime,1,2),	#接单时间
            dev_id=dev.id,	#调用设备
            driver=dev.driver,	#司机
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
        cols[ "guide"]=random.choice(guides).id
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


