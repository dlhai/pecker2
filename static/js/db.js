var db_roles = [
    {
        "id": "1", "type": "winder", "name": "叶片超级帐号", modules: [
            { name: "地图", url: "windersumap.html" },
            { name: "风场", url: "windersu.html" },
            { name: "人员", url: "user3.html" },
            { name: "厂家", url: "vender.html" }]
    },
    {
        "id": "2", "type": "winder", "name": "风场主管", modules: [
            { name: "地图", url: "windermap.html" },
            { name: "设备", usesub: true, url: "winder2.html" },
            { name: "案件", usesub: true, url: "coord.html" },
            { name: "记录", usesub: true, url: "repairlog.html" },
            { name: "人员", url: "user3.html" }]
    },
    {
        "id": "3", "type": "winder", "name": "驻场", modules: [
            { name: "地图", url: "windermap.html" },
            { name: "设备", usesub: true, url: "winder2.html" },
            { name: "案件", usesub: true, url: "coord.html" },
            { name: "记录", usesub: true, url: "repairlog.html" }]
    },
    {
        "id": "4", "type": "dev", "name": "设备超级帐号", modules: [
            { name: "地图", url: "devmap.html" },
            { name: "驻地", url: "devsu.html" },
            { name: "人员", url: "user3.html" },
            { name: "厂家", url: "devvender.html" }]
    },
    {
        "id": "5", "type": "dev", "name": "驻地主管", modules: [
            { name: "地图", url: "devmap.html" },
            { name: "驻地", url: "devwh.html" },
            { name: "人员", url: "user3.html" }]
    },
    {
        "id": "6", "type": "dev", "name": "设备司机", modules: [
            { name: "设备", url: "devdriver.html" }]
    },
    {
        "id": "7", "type": "wh", "name": "仓库超级帐号", modules: [
            { name: "仓库", url: "matsu.html" },
            { name: "人员", url: "user3.html" },
            { name: "材料", url: "material.html" }]
    },
    {
        "id": "8", "type": "wh", "name": "仓库主管", modules: [
            { name: "入库", url: "matin.html" },
            { name: "出库", url: "matout.html" },
            { name: "查询", usesub: true, subs: [{ name: "库存", url: "matquery.html" }, { name: "入库", url: "matqueryin.html" }, { name: "出库", url: "matqueryout.html" }]},
            { name: "人员", url: "user3.html" }]
    },
    {
        "id": "9", "type": "wh", "name": "仓库管理员", modules: [
            { name: "入库", url: "matin.html" },
            { name: "出库", url: "matout.html" },
            { name: "查询", usesub: true, subs: [{ name: "库存", url: "matquery.html" }, { name: "入库", url: "matqueryin.html" }, { name: "出库", url: "matqueryout.html" }] }],
    },
    { "id": "10", "type": "coord", "name": "调度超级帐号", modules: [{ name: "调度", url: "user3.html" }] },
    { "id": "11", "type": "coord", "name": "调度主管", modules: [{ name: "案件", url: "coord.html" }, { name: "记录", url: "repairlog.html" }] },
    { "id": "12", "type": "coord", "name": "调度", modules: [{ name: "案件", url: "coord.html" }, { name: "记录", url: "repairlog.html" }] },
    {"id": "13", "type": "expert", "name": "专家超级帐号", modules: [{ name: "专家", url: "user3.html" }]},
    {
        "id": "14", "type": "expert", "name": "专家", modules: [
            { name: "案件", url: "coord.html" },
            { name: "记录", url: "repairlog.html" }]
    },
    { "id": "15", "type": "repair", "name": "技工超级帐号", modules: [{ name: "技工", url: "user3.html" }] },
    {
        "id": "16", "type": "repair", "name": "维修队长", modules: [
            { name: "案件", url: "coord.html" },
            { name: "记录", url: "repairlog.html" },
            { name: "人员", url: "user3.html" }]
    },
    { "id": "17", "type": "repair", "name": "技工", modules: [{ name: "案件", url: "coord.html" }, { name: "记录", url: "repairlog.html" }] },
];

var branch = {
    "root": { "type": "root", "name": "企业列表", "sub": "winderco", "image": "" },
    "winderco": { "type": "winderco", "name": "风电企业", "sub": "winderprov", "image": "img/diy/1_open.png" },
    "winderprov": { "type": "winderprov", "name": "省区", "sub": "winder", "image": "img/folder.gif" },
    "winder": { "type": "winder", "name": "风场", "sub": "winderarea", "image": "img/diy/3.png" },
    "winderarea": { "type": "winderarea", "name": "风区", "sub": "efan", "image": "img/page.gif" },
    "efan": { "type": "efan", "name": "风电机", "sub": "leaf", "image": "" },
    "efanvender": { "type": "efanvender", "name": "整机供应商", "image": "" },
    "leafvender": { "type": "leafvender", "name": "叶片供应商", "image": "" },
    "sub": function (type) {
        return this[this[type].sub]
    }
}

var db_job = [
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

function GetRoleUser(name) {
    ReqdataS("/roleuserall", "", function (res) { db_roleusers = res.data; });
    var user = GetSub(db_roleusers, "job", GetSub(db_job, "name", name).id);
    var tip = "启用" + name + "帐号:{name}({id}) job={job} depart_id={depart_id} 调试"
    alert(tip.format(user));
    return user;
}

function GetsubJob(parentjobid, type) {
    var jobbranch = {
        "1": ["2", "3"], "2": ["2", "3"], "3": ["3"],//风场
        "4": ["5", "6"], "5": ["5", "6"], "6": ["6"],//驻地
        "7": ["8", "9"], "8": ["8", "9"], "9": ["9"],//仓库
        "10": ["11", "12"], "11": ["11", "12"], "11": ["12"], // 调度
        "13": ["14"], "14": ["14"], // 专家
        "15": ["16", "17"], "16": ["16", "17"], "17": ["17"] //技工
    }
    if (type == "array") {
        var r = new Array();
        var visable = jobbranch[parentjobid];
        for (var i in visable)
            r.push(GetArItem(db_job, "id", visable[i]));
        return r;
    }
    else if (type == "string") {
        if (jobbranch[parentjobid].length>1)
            return "(" + (jobbranch[parentjobid]).join(",") + ")";
        else
            return jobbranch[parentjobid];
    }

}

var db_skill = [
    { "id": "1", "name": "避雷" },
    { "id": "2", "name": "工艺设计" },
    { "id": "3", "name": "工艺生产" },
    { "id": "4", "name": "材料" },
    { "id": "5", "name": "安全" },
]

var db_sex = [
    { "id": "0", "name": "女" },
    { "id": "1", "name": "男" },
]

var status_dev = [
    { "id": "0", "name": "空闲" },
    { "id": "1", "name": "任务中" },
    { "id": "-1", "name": "报废" },
]
var status_devwork = [
    { "id": "0", "name": "编辑" },
    { "id": "1", "name": "提交" },
    { "id": "2", "name": "受理" },
    { "id": "-1", "name": "拒绝" },
]

var db_devclss = [
    { "id": "1", "name": "航空母舰" },
    { "id": "2", "name": "战列舰" },
    { "id": "3", "name": "巡洋舰" },
    { "id": "4", "name": "驱逐舰" },
    { "id": "5", "name": "护卫舰" },
    { "id": "6", "name": "鱼雷艇" },
    { "id": "7", "name": "导弹艇" },
    { "id": "8", "name": "猎潜艇" },
    { "id": "9", "name": "布雷舰" },
    ]

var db_matwhscale = [
    { "id": "1", "name": "小型" },
    { "id": "2", "name": "中型" },
    { "id": "3", "name": "大型" },
    { "id": "4", "name": "超大型" },
    { "id": "5", "name": "巨型" },
    { "id": "6", "name": "超巨型" },
]

var db_matsouce = [
    { "id": "1", "name": "厂家直送" },
    { "id": "2", "name": "调货" },
]

var status_matin = [
    { "id": "0", "name": "新建" },
    { "id": "1", "name": "等待审批" },
    { "id": "2", "name": "等待入库" },
    { "id": "3", "name": "完成" },
    { "id": "-1", "name": "退回" },
]
var status_matout = [
    { "id": "0", "name": "新建" },
    { "id": "1", "name": "调度提交" },
    { "id": "2", "name": "库管备货或库管创建" },
    { "id": "3", "name": "等待审批" },
    { "id": "4", "name": "审批通过" },
    { "id": "5", "name": "入库完成" },
    { "id": "-1", "name": "退回" },
]

var db_tbl = [
    { "id": "1", "name": "base", "title": "定义" },
    { "id": "2", "name": "link", "title": "一对多引用" },
    { "id": "3", "name": "addit", "title": "附件" },
    { "id": "4", "name": "config", "title": "配置" },
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
    { "id": "19", "name": "fault", "title": "报修" },
    { "id": "20", "name": "devwh", "title": "驻地" },
    { "id": "21", "name": "dev", "title": "设备" },
    { "id": "22", "name": "devwork", "title": "设备任务" },
    { "id": "23", "name": "matprov", "title": "仓库省区" },
    { "id": "24", "name": "matwh", "title": "仓库" },
    { "id": "25", "name": "mat", "title": "材料" },
    { "id": "26", "name": "matin", "title": "入库单" },
    { "id": "27", "name": "matinrec", "title": "入库记录" },
    { "id": "28", "name": "matout", "title": "出库单" },
    { "id": "29", "name": "matoutrec", "title": "出库记录" },
    { "id": "30", "name": "chat", "title": "聊天记录" },
]
function GetTbl(name) { return GetSub(db_tbl, "name", name); }

cache = new Object()

function Reqdata(url, ctx, fun) {
    if (cache[url]) { // 优先使用缓冲数据
        fun(cache[url], ctx);
        return;
    }

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", url, true);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            jdata = $.parseJSON(xmlhttp.responseText);
            fun(jdata, ctx);
            cache[url] = jdata;
        }
    };
    xmlhttp.send();
}

// 同步方式
function ReqdataS(url, ctx, fun) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", url, false);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            jdata = $.parseJSON(xmlhttp.responseText);
            fun(jdata, ctx);
        }
    };
    xmlhttp.send();
}


// 回调函数格式：render_fun(ar, id)
function ReqRender(url, id, val, render_fun) {
    if (cache[url]) { // 优先使用缓冲数据
        return $("#" + id).html(render_fun(cache[url], val));
    }

    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", url, true);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            jdata = $.parseJSON(xmlhttp.responseText);
            $("#" + id).html(render_fun(jdata, val));
            cache[url] = jdata;
        }
    };
    xmlhttp.send();
    return "";
}

// 自此以下将被废弃

function tmfmt(tm, fmt) {
     var o = { 
        "M+" : tm.getMonth()+1,                 //月份 
        "d+" : tm.getDate(),                    //日 
        "h+" : tm.getHours(),                   //小时 
        "m+" : tm.getMinutes(),                 //分 
        "s+" : tm.getSeconds(),                 //秒 
        "q+" : Math.floor((tm.getMonth()+3)/3), //季度 
        "S"  : tm.getMilliseconds()             //毫秒 
    }; 
    if(/(y+)/.test(fmt)) {
            fmt=fmt.replace(RegExp.$1, (tm.getFullYear()+"").substr(4 - RegExp.$1.length)); 
    }
     for(var k in o) {
        if(new RegExp("("+ k +")").test(fmt)){
             fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
         }
     }
    return fmt; 
}

//生成一个随机字符串
function rndstr(len) {
    var chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    var maxPos = chars.length + 1;
    var pwd = '';
    for (i = 0; i < len; i++)
        pwd += chars.charAt(Math.floor(Math.random() * maxPos));
    return pwd;
}

//生成[min-max)之间的一个数
function rndrange(min, max) { return parseInt(Math.random() * (max - min)) + min; }
//生成长度为len一个数字字符串
function rndnumstr(len) {
    var val = rndrange(0, Math.pow(10, len));
    return (Array(len).join(0) + val).slice(-len);
}

//从数组中随机选1个元素，如果att不为空，则要求被选取的元素att属性值为val
function rnditem(ar, att, val )
{
    if (att) {
        var a = [];
        for (var i = 0; i < ar.length; i++) {
            if (ar[i][att] == val)
                a.push(ar[i]);
        }
        return a[rndrange(0, a.length)];
    }
    else
        return ar[rndrange(0, ar.length)];
}

//从数组中随机选[min-max)个元素，形成一个新的数组, 如果att不为空，则要求被选取的元素att属性值为val
function rndsubarray(ar, min, max, att, val )
{
    if (att){
        var sub = [];
        for (var i = 0; i < ar.length; i++) {
            if (ar[i][att] == val)
                sub.push(ar[i]);
        }
        return rndsubarray(sub, min, max )
    }
    else
    {
        var a = [];
        for (var i = 0; i < ar.length; i++)
            a.push(i);
        var count = rndrange(min, max);
        var sel = [];
        for (var i = 0; i < count && i < ar.length; i++) {
            var x = rndrange(0, a.length);
            sel.push(a[x]);
            a.splice(x, 1);
        }
        sel.sort();

        var r = [];
        for (var i = 0; i < sel.length; i++)
            r.push(ar[sel[i]]);
        return r;
    }
}

//从数组中选出符合条件的元素，形成一个新的数组并返回, 要求被选取的元素att属性值为mval子字符串
function getsubarray(ar, att, mval )
{
    var r = [];
    for (var i = 0; i < ar.length; i++) {
        if ( mval.indexOf(ar[i][att]) >= 0)
            r.push(ar[i]);
    }
    return r;
}


function GetArItem( ar, att, val )
{
    if (att)
    {
        for (var i = 0; i < ar.length; i++) {
            if (ar[i][att] == val)
                return ar[i];
        }
    }
    return "";
}


//初始化关联数据
$(function () {
    $(".x3Doc>.x3Doc-handle").on("click", function () {
        $(this).siblings(".x3Doc-menu").css("display", "block");
        $(this).siblings(".x3Doc-menu").addClass("x3Doc-click");
    });

    window.onclick = x3DocMenuHide;
    function x3DocMenuHide() {
        $(".x3Doc-menu:not(.x3Doc-click)").css("display", "none");
        $(".x3Doc>.x3Doc-click").removeClass("x3Doc-click");
    }
});


var db_leafvender =
[
{ "name": "重庆复合", "fname": "重庆国际复合材料有限公司", "addr": "北京市顺义区新顺南大街8号院1幢F1-51B ", "atten": "顾冰薇", "tel": "0532-86011111", "leader": "常辰淋", "fax": "023-63862607" },
{ "name": "艾尔姆", "fname": "艾尔姆玻璃纤维制品（天津）有限公司", "addr": "南京东路819号百联世贸广场7号门一层", "atten": "钱振海", "tel": "0551-4243311", "leader": "舒代巧", "fax": "0311-87600111" },
{ "name": "上海玻璃", "fname": "上海玻璃钢研究院", "addr": "上海市浦东新区祖冲之路1253号长泰广场E1-06号铺位 ", "atten": "雷亦旋", "tel": "0571-87622362", "leader": "阳昕燕", "fax": "0752-95105688" },
{ "name": "江苏九鼎", "fname": "江苏九鼎新材料股份有限公司", "addr": "常州市新北区通江中路88号万达广场步行街1023号 ", "atten": "陆易绿", "tel": "020-95105105", "leader": "巴以彤", "fax": "0577-88389999" },
{ "name": "南京先进", "fname": "南京先进复合材料制品有限公司", "addr": "成都市锦江区中纱帽街8号太古里F196 铺 ", "atten": "陈嘉木", "tel": "0371-68356666", "leader": "鲍元柳", "fax": "0769-95105106" },
{ "name": "上海越科", "fname": "上海越科复合材料有限公司", "addr": "大连经济技术开发区金马路189号大连安盛购物广场 ", "atten": "周绍元", "tel": "021-8008207890", "leader": "戈刚林", "fax": "0530-3982522" },
{ "name": "中兵五三", "fname": "中国兵器工业集团第五三科技研究院", "addr": "辽宁省大连市甘井子区山东路235号安盛亿合城Y10014/15/16铺位 ", "atten": "杜诗蕾", "tel": "0531-86012520", "leader": "勾觅丹", "fax": "028-86433232" },
{ "name": "威海碳素", "fname": "威海市碳素渔竿厂", "addr": "大庆市萨尔图区东风路18号万达广场室内步行街一层1026、1027、1028号商铺 ", "atten": "罗鸿彩", "tel": "025-95105105", "leader": "苗新华", "fax": "0351-2233611" },
{ "name": "帝斯曼", "fname": "金陵帝斯曼树脂有限公司", "addr": "抚顺市新抚区浑河南路（中段）56号 1021，1022，1023铺位 ", "atten": "石梦凡", "tel": "0535-95105175", "leader": "钱小乐", "fax": "0591-87050222" },
{ "name": "中航惠腾", "fname": "中航（保定）惠腾风电设备有限公司", "addr": "广州市天河区天河路383号以北、天河东路以西地段太古汇商场裙楼地铁上层MU28号商铺 ", "atten": "孙刚毅", "tel": "0512-67513131", "leader": "师子寒", "fax": "0310-3023233" },
{ "name": "浙江联洋", "fname": "浙江联洋复合材料有限公司", "addr": "哈尔滨道里区中央大街69号金安欧罗巴广场一楼 ", "atten": "谢依霜", "tel": "0592-2088888", "leader": "余涛鸣", "fax": "0898-31686222" },
{ "name": "常熟卡柏", "fname": "常熟市卡柏（CoreBoard）复合材料有限公司", "addr": "杭州延安西路546号1楼 ", "atten": "严芷容", "tel": "029-95105688", "leader": "相瑶一", "fax": "0536-2972522" },
{ "name": "恒吉星", "fname": "北京恒吉星工贸有限责任公司", "addr": "杭州银泰城  浙江省杭州市丰登街299号 1F032、1F033、1F035  ", "atten": "余博容", "tel": "021-95105105", "leader": "边星瑶", "fax": "0757-82232940" },
];


var db_attach =
{
    face: ["img/face/face0.jpg", "img/face/face1.jpg", "img/face/face2.jpg", "img/face/face3.jpg", "img/face/face4.jpg", "img/face/face5.jpg", "img/face/face6.jpg", "img/face/face7.jpg", "img/face/face8.jpg", "img/face/face9.jpg", "img/face/face10.jpg", "img/face/face11.jpg", "img/face/face12.jpg", "img/face/face13.jpg", "img/face/face14.jpg", "img/face/face15.jpg", "img/face/face16.jpg", "img/face/face17.jpg", "img/face/face18.jpg", "img/face/face19.jpg", "img/face/face20.jpg"],
    winderimg: ["img/winder/winder1.jpg", "img/winder/winder2.jpg", "img/winder/winder3.jpg", "img/winder/winder4.jpg", "img/winder/winder5.jpg", "img/winder/winder6.jpg", "img/winder/winder7.jpg", "img/winder/winder8.jpg", "img/winder/winder9.jpg", "img/winder/winder10.jpg", "img/winder/winder11.jpg"],
    assess: ["评估报告_顾冰薇_1993-06-03", "评估报告_钱振海_1982-05-25", "评估报告_雷亦旋_1989-03-11", "评估报告_陆易绿_1994-05-10", "评估报告_陈嘉木_1990-12-09", "评估报告_周绍元_1984-12-27", "评估报告_杜诗蕾_1990-07-04", "评估报告_罗鸿彩_1986-03-23", "评估报告_石梦凡_1981-04-15", "评估报告_孙刚毅_1990-02-26", "评估报告_谢依霜_1989-05-11", "评估报告_严芷容_1991-01-06", "评估报告_余博容_1994-11-03", "评估报告_程含芙_1984-01-10", "评估报告_韩德泽_1990-11-30", "评估报告_姜慕蕊_1978-09-22", "评估报告_付高爽_1981-03-02", "评估报告_石又晴_1991-09-07", "评估报告_蓝梦槐_1978-07-28", "评估报告_窦加隆_1981-09-28", "评估报告_盛韩嘉_1975-12-18", "评估报告_常辰淋_1981-09-14", "评估报告_舒代巧_1989-05-29", "评估报告_阳昕燕_1989-02-21", "评估报告_巴以彤_1976-07-22"],
    assess2: ["二评报告_鲍元柳_1970-07-28", "二评报告_戈刚林_1989-03-20", "二评报告_勾觅丹_1973-09-07", "二评报告_苗新华_1993-08-16", "二评报告_钱小乐_1990-08-30", "二评报告_师子寒_1995-12-28", "二评报告_余涛鸣_1976-03-21", "二评报告_相瑶一_1989-08-22", "二评报告_劳思寒_1979-12-22", "二评报告_魏苑_1973-02-17", "二评报告_勾星瑶_1993-02-01", "二评报告_郎佳_1978-02-01", "二评报告_鲍凌春_1992-04-06", "二评报告_伊帅成_1991-01-22", "二评报告_卫尔容_1988-02-17", "二评报告_滕龙_1987-07-08", "二评报告_傅奕冰_1994-03-19", "二评报告_范沛凝_1981-09-30", "二评报告_顾伟祺_1987-11-28", "二评报告_邱雅懿_1994-08-31", "二评报告_覃盼翠_1999-02-10", "二评报告_高文林_1979-07-22"],
    scheme: ["维修方案_莫寄瑶_1991-11-12", "维修方案_付又青_1976-12-26", "维修方案_韦兴庆_1984-02-16", "维修方案_夏安民_1988-02-02", "维修方案_方芷荷_1985-06-24", "维修方案_丁雅昶_1974-06-07", "维修方案_万力强_1974-12-18", "维修方案_肖惜芹_1980-08-26", "维修方案_方天菱_1993-01-11", "维修方案_王丹烟_1993-06-03", "维修方案_杜翠岚_1982-05-25", "维修方案_杨以云_1989-03-11", "维修方案_肖怜雪_1994-05-10", "维修方案_全曼云_1990-12-09", "维修方案_元镇国_1984-12-27", "维修方案_贾灵泉_1990-07-04", "维修方案_巩恒霖_1986-03-23", "维修方案_严少_1981-04-15", "维修方案_云宇峰_1990-02-26", "维修方案_匡贝_1989-05-11", "维修方案_康靖童_1991-01-06", "维修方案_骆慕卉_1994-11-03", "维修方案_俞伟_1984-01-10", "维修方案_余友易_1990-11-30", "维修方案_吴靖_1978-09-22", "维修方案_庾依玉_1981-03-02", "维修方案_万坤_1991-09-07", "维修方案_程新桐_1978-07-28", "维修方案_敖玲沁_1981-09-28", "维修报告_能丰_1975-12-18"],
    report: ["维修报告_计翎妍_1981-09-14", "维修报告_阎乐晨_1989-05-29", "维修报告_吕采南_1989-02-21", "维修报告_堵昕燕_1976-07-22", "维修报告_萧传军_1970-07-28", "维修报告_邓娟_1989-03-20", "维修报告_江智卓_1973-09-07", "维修报告_柏肜瑛_1993-08-16", "维修报告_水成日_1990-08-30", "维修报告_周宏图_1995-12-28", "维修报告_齐痴凝_1976-03-21", "维修报告_郝紫瞳_1989-08-22", "维修报告_云尘_1979-12-22", "维修报告_储艺璇_1973-02-17", "维修报告_荣海龙_1993-02-01", "维修报告_卜伟成_1978-02-01", "维修报告_满玲漪_1976-04-27", "维修报告_马凌春_1985-10-30", "维修报告_傅微_1985-02-17", "维修报告_凌钟吉_1974-10-31", "维修报告_步孜娴_1994-10-07", "维修报告_侯星嘉_1978-09-24", "维修报告_齐任安_1985-04-21", "维修报告_柏鑫_1993-11-18", "维修报告_饶忆丹_1986-11-13", "维修报告_宿柯朱_1984-01-20", "维修报告_孟广斌_1983-03-17", "维修报告_安悦_1979-10-20", "维修报告_鲁白桃_1981-11-01", "维修报告_平勇_1993-11-17"],
    devuse: ["设备调用单_840110737", "设备调用单_901130332", "设备调用单_780922800", "设备调用单_810302577", "设备调用单_910907006", "设备调用单_780728516", "设备调用单_810928109", "设备调用单_751218624", "设备调用单_810914797", "设备调用单_890529869", "设备调用单_890221332", "设备调用单_760722431", "设备调用单_700728549", "设备调用单_890320962", "设备调用单_730907507", "设备调用单_930816162", "设备调用单_900830678", "设备调用单_951228519", "设备调用单_760321367", "设备调用单_890822530", "设备调用单_791222607", "设备调用单_730217983", "设备调用单_930201086", "设备调用单_780201836", "设备调用单_760427128", "设备调用单_851030084", "设备调用单_850217506", "设备调用单_741031506", "设备调用单_941007954", "设备调用单_780924267", "设备调用单_850421166"],
    matout: ["用料单_990210784", "用料单_790722207", "用料单_911112042", "用料单_761226388", "用料单_840216773", "用料单_880202660", "用料单_850624821", "用料单_740607780", "用料单_741218817", "用料单_800826114", "用料单_930111224", "用料单_930603487", "用料单_820525171", "用料单_890311715", "用料单_940510422", "用料单_901209410", "用料单_841227992", "用料单_900704440", "用料单_860323775", "用料单_810415316", "用料单_900226874", "用料单_890511593", "用料单_910106840", "用料单_941103230"],
    matout_status:["等待备货","正在备货","等待审核","等待发货","等待确认"],
    vtime: ["2008-11-30 5:49:21", "2005-03-09 9:39:7", "2007-11-09 2:0:5", "2009-04-16 21:30:41", "2008-12-20 12:54:26", "2007-09-11 16:41:2", "2008-04-21 22:21:48", "2005-10-11 8:20:35", "2004-01-28 6:0:29", "2008-01-31 20:32:35", "2006-01-19 13:53:12", "2003-12-04 14:13:3", "2008-11-06 14:14:19", "2009-01-31 7:7:30", "2005-03-17 11:11:42", "2010-03-15 18:22:11", "2008-12-24 13:50:9", "2008-03-20 2:7:39", "2008-06-15 10:31:10", "2008-05-04 10:44:11", "2010-09-25 14:57:48", "2009-10-15 4:54:22", "2005-05-31 7:20:18", "2008-07-28 19:24:48", "2004-04-24 10:18:1", "2004-08-16 11:27:22", "2010-04-02 17:57:42", "2008-12-18 1:54:24", "2010-06-19 13:18:11", "2006-01-23 5:26:5", "2010-08-05 10:56:17", "2003-08-30 10:59:20", "2006-11-04 18:56:57"],
    sign:[]
    };

var db_devwh_list = {
    fields: [
        { "title": "名称", "name": "name", },
        { "title": "全名", "fname": "name", },
        { "title": "地理位置", "name": "gps", },
        { "title": "地址", "name": "addr", "ftype": "bigtext" },
        { "title": "主管", "name": "leader", },
        { "title": "备注", "name": "remark", "ftype": "bigtext" },
    ],
    data: [
{"name":"长白一驻","fname":"长白山一号驻地","gps":"116.357701,40.596596","addr":"青海省玉树藏族自治州治多县","leader":"顾冰薇","remark":"站在巨人的肩上是为了超过巨人。"},
{"name":"兴安岭驻","fname":"大兴安岭X号驻地","gps":"123.130206,50.629764","addr":"西藏自治区昌都地区类乌齐县","leader":"钱振海","remark":"泉水，奋斗之路越曲折，心灵越纯洁。"},
{"name":"大草原驻","fname":"大草原蓝天白云驻地","gps":"85.231774,46.32769","addr":"辽宁省大连市","leader":"雷亦旋","remark":"如果缺少破土面出并与风雪拚搏的勇气，种子的前途并不比落叶美妙一分。"},
{"name":"风吹草驻","fname":"风吹草低没牛羊驻地","gps":"96.564509,40.766858","addr":"湖北省省直辖行政单位神农架林区","leader":"步孜娴","remark":"竹笋虽然柔嫩，但它不怕重压，敢于奋斗、敢于冒尖。"},
{"name":"天山林驻","fname":"天山森林驻地","gps":"84.127936,38.201158","addr":"重庆市县奉节县","leader":"陈嘉木","remark":"不要让追求之舟停泊在幻想的港湾，而应扬起奋斗的风帆，驶向现实生活的大海。"},
{"name":"塔里木驻","fname":"塔里木驻地","gps":"87.513039,32.664229","addr":"河北省沧州市沧县","leader":"周绍元","remark":"智者的梦再美，也不如愚人实干的脚印。"},
{"name":"准葛尔驻","fname":"准葛尔沙漠驻地","gps":"105.248033,34.267815","addr":"云南省文山壮族苗族自治州文山县","leader":"杜诗蕾","remark":"耕耘者的汗水是哺育种子成长的乳汁。"},
{"name":"柴达木驻","fname":"柴达木盐湖驻地","gps":"120.996119,38.664246","addr":"湖北省宜昌市点军区","leader":"罗鸿彩","remark":"不去耕耘，不去播种，再肥的沃土也长不出庄稼，不去奋斗，不去创造，再美的青春也结不出硕果。"},
{"name":"祁连荒驻","fname":"祁连山荒漠驻地","gps":"109.957741,37.148299","addr":"贵州省遵义市正安县","leader":"石梦凡","remark":"让珊瑚远离惊涛骇浪的侵蚀吗？那无异是将它们的美丽葬送。"},
{"name":"草原蓝驻","fname":"大草原蓝天白云驻地2号","gps":"95.681439,39.808819","addr":"山东省济南市市辖区","leader":"孙刚毅","remark":"再好的种子，不播种下去，也结不出丰硕的果实。"},
{"name":"无人区驻","fname":"无人区卷心菜驻地","gps":"116.286411,33.777599","addr":"西藏自治区山南地区措美县","leader":"谢依霜","remark":"如果可恨的挫折使你尝到苦果，朋友，奋起必将让你尝到人生的欢乐。"},
{"name":"昆仑山驻","fname":"昆仑山雪域驻地","gps":"103.113947,32.227408","addr":"陕西省渭南市富平县","leader":"严芷容","remark":"瀑布---为了奔向江河湖海，即使面临百丈深渊，仍然呼啸前行，决不退缩"},
{"name":"渤海湾驻","fname":"渤海湾无风海浪驻地","gps":"114.446681,19.83017","addr":"甘肃省甘南藏族自治州碌曲县","leader":"余博容","remark":"对于勇士来说，贫病、困窘、责难、诽谤、冷嘲热讽......，一切压迫都是前进的动力。"},
{"name":"太行山驻","fname":"太行山绝壁攀岩上不去驻地","gps":"111.944649,28.136926","addr":"河南省商丘市永城市","leader":"程含芙","remark":"不从泥泞不堪的小道上迈步，就踏不上铺满鲜花的大路。"},
{"name":"天府宝驻","fname":"天府之国无限宝贝驻地","gps":"116.948714,28.006373","addr":"浙江省杭州市建德市","leader":"韩德泽","remark":"幻想在漫长的生活征途中顺水行舟的人，他的终点在下游。只有敢于扬起风帆，顶恶浪的勇士，才能争到上游。"},
]
};

var db_dev_list ={
    fields: [
        { "title": "照片", "name": "image", "ftype": "image", "twidth": "0" },
        { "title": "名称", "name": "name", },
        { "title": "型号", "name": "type", },
        { "title": "编号", "name": "code", },
        { "title": "当前位置", "name": "gps", },
        { "title": "状态", "name": "status", },
        { "title": "司机", "name": "driver", },
        { "title": "联系电话", "name": "phone", },
        { "title": "备注", "name": "remark", "ftype": "bigtext", },
        { "title": "生产厂家", "name": "producer", "ftype": "bigtext", "twidth": "0" },
        { "title": "生产日期", "name": "producedate", "twidth": "0" },
        { "title": "购置日期", "name": "buydate", "twidth": "0" },
        { "title": "年检日期", "name": "checkdate", },
    ],
    data:[
    { "name": "96式主战坦克", "type": "96式", "code": "7030CTA/P2", "status": "空闲", "producer": "嵊州市洒而电器厂", "producedate": "1992-04-06", "buydate": "1984-02-16", "checkdate": "1975-12-18", "remark": "嵊州市洒而电器厂" },
    { "name": "99式主战坦克", "type": "99式", "code": "7330BM ", "status": "出勤", "producer": "沈阳电机厂销售总公司", "producedate": "1991-01-22", "buydate": "1988-02-02", "checkdate": "1981-09-14", "remark": "沈阳电机厂销售总公司" },
    { "name": "63A式水陆坦克", "type": "63A式", "code": "D111508A ", "status": "空闲", "producer": "沈阳士林电机制造有限公司", "producedate": "1988-02-17", "buydate": "1985-06-24", "checkdate": "1989-05-29", "remark": "沈阳士林电机制造有限公司" },
    { "name": "155毫米自行榴弹炮", "type": "155 m", "code": "2528H ", "status": "出勤", "producer": "绍兴市万鹏机电有限公司", "producedate": "1987-07-08", "buydate": "1974-06-07", "checkdate": "1989-02-21", "remark": "绍兴市万鹏机电有限公司" },
    { "name": "PCZ45弹药支援车", "type": "PCZ45", "code": "1207KTN1/P6 ", "status": "空闲", "producer": "上海任重仪表电器有限公司", "producedate": "1994-03-19", "buydate": "1974-12-18", "checkdate": "1976-07-22", "remark": "上海任重仪表电器有限公司" },
    { "name": "ZCY45营指挥车", "type": "ZCY45", "code": "2236HDB ", "status": "出勤", "producer": "深圳市英士达机电技术开发有限公司", "producedate": "1981-09-30", "buydate": "1980-08-26", "checkdate": "1970-07-28", "remark": "深圳市英士达机电技术开发有限公司" },
    { "name": "ZCY45连指挥车", "type": "ZCY45", "code": "BK1712 ", "status": "报废", "producer": "浙江嵊州市大力神机电厂", "producedate": "1987-11-28", "buydate": "1993-01-11", "checkdate": "1989-03-20", "remark": "浙江嵊州市大力神机电厂" },
    { "name": "95式自动步枪", "type": "95式", "code": "4053156W2K ", "status": "其他", "producer": "湖北万邦机电发展有限公司", "producedate": "1994-08-31", "buydate": "1993-06-03", "checkdate": "1973-09-07", "remark": "湖北万邦机电发展有限公司" },
    { "name": "03式自动步枪", "type": "03式", "code": "7303C/P4 ", "status": "空闲", "producer": "沈阳嘉晨电机(产品)制造有限公司", "producedate": "1999-02-10", "buydate": "1982-05-25", "checkdate": "1993-08-16", "remark": "沈阳嘉晨电机(产品)制造有限公司" },
    { "name": "10式阻击步枪", "type": "10式", "code": "E2526EH ", "status": "出勤", "producer": "浙江博佳电机有限公司", "producedate": "1979-07-22", "buydate": "1989-03-11", "checkdate": "1990-08-30", "remark": "浙江博佳电机有限公司" },
    { "name": "WS-2火箭弹", "type": "WS-2", "code": "N413M/P6 ", "status": "空闲", "producer": "东莞市奥比特化工贸易有限公司", "producedate": "1991-11-12", "buydate": "1994-05-10", "checkdate": "1995-12-28", "remark": "东莞市奥比特化工贸易有限公司" },
    { "name": "卫士-2远程火箭炮", "type": "卫士-2", "code": "23120EW33K ", "status": "出勤", "producer": "贵州雨田电机有限公司", "producedate": "1976-12-26", "buydate": "1990-12-09", "checkdate": "1976-03-21", "remark": "贵州雨田电机有限公司" },
    { "name": "WS-2发射车", "type": "WS-2", "code": "SA1-120BSS ", "status": "空闲", "producer": "上海德托精密机电事业部", "producedate": "1984-02-16", "buydate": "1984-12-27", "checkdate": "1989-08-22", "remark": "上海德托精密机电事业部" },
    { "name": "86式步兵战车", "type": "86式", "code": "7034AC ", "status": "出勤", "producer": "鹤壁市伟琴仪器仪表有限公司", "producedate": "1988-02-02", "buydate": "1990-07-04", "checkdate": "1979-12-22", "remark": "鹤壁市伟琴仪器仪表有限公司" },
    { "name": "92式步兵战车", "type": "92式", "code": "32907/P6x ", "status": "报废", "producer": "北京和利时电机技术有限公司", "producedate": "1985-06-24", "buydate": "1986-03-23", "checkdate": "1973-02-17", "remark": "北京和利时电机技术有限公司" },
    { "name": "武直-10武装直升机", "type": "武直-10", "code": "7040X2DF ", "status": "其他", "producer": "常州市丰源微特电机有限公司", "producedate": "1974-06-07", "buydate": "1981-04-15", "checkdate": "1993-02-01", "remark": "常州市丰源微特电机有限公司" },
    { "name": "武直-19武装侦察直升机", "type": "武直-19", "code": "NNQP6960", "status": "空闲", "producer": "东莞市线源电子有限公司", "producedate": "1974-12-18", "buydate": "1990-02-26", "checkdate": "1978-02-01", "remark": "东莞市线源电子有限公司" },

    ]
}

var db_devtasklist = {
    fields: [
        { "title": "发单人", "name": "create" },
        { "title": "发单时间", "name": "createdt" },
        { "title": "接单司机", "name": "receiver" },
        { "title": "接单时间", "name": "receivedt" },
        { "title": "预期时长", "name": "span" },
        { "title": "完成时间", "name": "completedt" },
        { "title": "任务地点", "name": "place" },
        { "title": "状态", "name": "status" },
    ],
    data: [
        { "create": "雷亦旋", "createdt": "1992-04-06", "receiver": "庾依玉", "receivedt": "1984-02-16", "span": "3", "completedt": "1975-12-18", "place": "青海省玉树藏族自治州治多县", "status": "拒绝" },
        { "create": "陆易绿", "createdt": "1991-01-22", "receiver": "万坤", "receivedt": "1988-02-02", "span": "5", "completedt": "1981-09-14", "place": "西藏自治区昌都地区类乌齐县", "status": "完成" },
        { "create": "陈嘉木", "createdt": "1988-02-17", "receiver": "程新桐", "receivedt": "1985-06-24", "span": "7", "completedt": "1989-05-29", "place": "辽宁省大连市", "status": "拒绝" },
        { "create": "周绍元", "createdt": "1987-07-08", "receiver": "敖玲沁", "receivedt": "1974-06-07", "span": "6", "completedt": "1989-02-21", "place": "湖北省省直辖行政单位神农架林区", "status": "完成" },
        { "create": "杜诗蕾", "createdt": "1994-03-19", "receiver": "能丰", "receivedt": "1974-12-18", "span": "10", "completedt": "1976-07-22", "place": "重庆市县奉节县", "status": "完成" },
        { "create": "罗鸿彩", "createdt": "1981-09-30", "receiver": "计翎妍", "receivedt": "1980-08-26", "span": "8", "completedt": "1970-07-28", "place": "河北省沧州市沧县", "status": "完成" },
        { "create": "石梦凡", "createdt": "1987-11-28", "receiver": "阎乐晨", "receivedt": "1993-01-11", "span": "4", "completedt": "1989-03-20", "place": "云南省文山壮族苗族自治州文山县", "status": "拒绝" },
        { "create": "孙刚毅", "createdt": "1994-08-31", "receiver": "吕采南", "receivedt": "1993-06-03", "span": "3", "completedt": "1973-09-07", "place": "湖北省宜昌市点军区", "status": "完成" },
        { "create": "谢依霜", "createdt": "1999-02-10", "receiver": "堵昕燕", "receivedt": "1982-05-25", "span": "5", "completedt": "1993-08-16", "place": "贵州省遵义市正安县", "status": "完成" },
        { "create": "严芷容", "createdt": "1979-07-22", "receiver": "萧传军", "receivedt": "1989-03-11", "span": "1", "completedt": "1990-08-30", "place": "山东省济南市市辖区", "status": "完成" },
        { "create": "余博容", "createdt": "1991-11-12", "receiver": "邓娟", "receivedt": "1994-05-10", "span": "2", "completedt": "1995-12-28", "place": "西藏自治区山南地区措美县", "status": "完成" },
        { "create": "程含芙", "createdt": "1976-12-26", "receiver": "江智卓", "receivedt": "1990-12-09", "span": "7", "completedt": "1976-03-21", "place": "陕西省渭南市富平县", "status": "拒绝" },
        { "create": "韩德泽", "createdt": "1984-02-16", "receiver": "柏肜瑛", "receivedt": "1984-12-27", "span": "6", "completedt": "1989-08-22", "place": "甘肃省甘南藏族自治州碌曲县", "status": "完成" },
        { "create": "姜慕蕊", "createdt": "1988-02-02", "receiver": "水成日", "receivedt": "1990-07-04", "span": "10", "completedt": "1979-12-22", "place": "河南省商丘市永城市", "status": "完成" },
        { "create": "付高爽", "createdt": "1985-06-24", "receiver": "周宏图", "receivedt": "1986-03-23", "span": "8", "completedt": "1973-02-17", "place": "浙江省杭州市建德市", "status": "完成" },
        { "create": "石又晴", "createdt": "1974-06-07", "receiver": "齐痴凝", "receivedt": "1981-04-15", "span": "4", "completedt": "1993-02-01", "place": "安徽省芜湖市", "status": "完成" },
        { "create": "蓝梦槐", "createdt": "1974-12-18", "receiver": "郝紫瞳", "receivedt": "1990-02-26", "span": "3", "completedt": "1978-02-01", "place": "青海省玉树藏族自治州治多县", "status": "拒绝" },
        { "create": "窦加隆", "createdt": "1984-02-16", "receiver": "云尘", "receivedt": "1981-04-15", "span": "5", "completedt": "1989-02-21", "place": "西藏自治区昌都地区类乌齐县", "status": "完成" },
        { "create": "盛韩嘉", "createdt": "1988-02-02", "receiver": "储艺璇", "receivedt": "1990-02-26", "span": "1", "completedt": "1976-07-22", "place": "辽宁省大连市", "status": "完成" },
        { "create": "常辰淋", "createdt": "1985-06-24", "receiver": "荣海龙", "receivedt": "1989-05-11", "span": "2", "completedt": "1970-07-28", "place": "湖北省省直辖行政单位神农架林区", "status": "完成" },
        { "create": "舒代巧", "createdt": "1974-06-07", "receiver": "卜伟成", "receivedt": "1991-01-06", "span": "7", "completedt": "1989-03-20", "place": "重庆市县奉节县", "status": "完成" },
        { "create": "阳昕燕", "createdt": "1974-12-18", "receiver": "满玲漪", "receivedt": "1994-11-03", "span": "6", "completedt": "1979-12-22", "place": "河北省沧州市沧县", "status": "完成" },
        { "create": "巴以彤", "createdt": "1980-08-26", "receiver": "马凌春", "receivedt": "1984-01-10", "span": "7", "completedt": "1973-02-17", "place": "云南省文山壮族苗族自治州文山县", "status": "完成" },
        { "create": "鲍元柳", "createdt": "1993-01-11", "receiver": "傅微", "receivedt": "1990-11-30", "span": "6", "completedt": "1993-02-01", "place": "湖北省宜昌市点军区", "status": "完成" },
        { "create": "戈刚林", "createdt": "1993-06-03", "receiver": "凌钟吉", "receivedt": "1978-09-22", "span": "10", "completedt": "1978-02-01", "place": "贵州省遵义市正安县", "status": "拒绝" },
        { "create": "勾觅丹", "createdt": "1982-05-25", "receiver": "步孜娴", "receivedt": "1981-03-02", "span": "8", "completedt": "1976-04-27", "place": "山东省济南市市辖区", "status": "拒绝" },
        { "create": "苗新华", "createdt": "1989-03-11", "receiver": "侯星嘉", "receivedt": "1991-09-07", "span": "1", "completedt": "1985-10-30", "place": "西藏自治区山南地区措美县", "status": "完成" },
        { "create": "钱小乐", "createdt": "1994-05-10", "receiver": "齐任安", "receivedt": "1978-07-28", "span": "2", "completedt": "1985-02-17", "place": "陕西省渭南市富平县", "status": "完成" },
        { "create": "师子寒", "createdt": "1990-12-09", "receiver": "柏鑫", "receivedt": "1981-09-28", "span": "7", "completedt": "1974-10-31", "place": "甘肃省甘南藏族自治州碌曲县", "status": "完成" },
        { "create": "余涛鸣", "createdt": "1984-12-27", "receiver": "饶忆丹", "receivedt": "1975-12-18", "span": "6", "completedt": "1994-10-07", "place": "河南省商丘市永城市", "status": "完成" },
        { "create": "相瑶一", "createdt": "1990-07-04", "receiver": "宿柯朱", "receivedt": "1981-09-14", "span": "10", "completedt": "1978-09-24", "place": "浙江省杭州市建德市", "status": "完成" },
        { "create": "劳思寒", "createdt": "1986-03-23", "receiver": "孟广斌", "receivedt": "1989-05-29", "span": "8", "completedt": "1985-04-21", "place": "新疆维吾尔自治区巴音郭楞蒙古自治州库尔勒市", "status": "拒绝" },
        { "create": "魏苑", "createdt": "1978-07-28", "receiver": "安悦", "receivedt": "1990-08-30", "span": "4", "completedt": "1974-10-31", "place": "湖南省邵阳市武冈市", "status": "完成" },
        { "create": "勾星瑶", "createdt": "1981-09-28", "receiver": "鲁白桃", "receivedt": "1995-12-28", "span": "3", "completedt": "1994-10-07", "place": "安徽省黄山市徽州区", "status": "完成" },
        { "create": "郎佳", "createdt": "1975-12-18", "receiver": "平勇", "receivedt": "1976-03-21", "span": "5", "completedt": "1978-09-24", "place": "黑龙江省大庆市", "status": "完成" },
        { "create": "鲍凌春", "createdt": "1981-09-14", "receiver": "肖怜雪", "receivedt": "1989-08-22", "span": "4", "completedt": "1985-04-21", "place": "四川省南充市嘉陵区", "status": "完成" },
        { "create": "伊帅成", "createdt": "1989-05-29", "receiver": "全曼云", "receivedt": "1979-12-22", "span": "3", "completedt": "1993-11-18", "place": "辽宁省沈阳市新民市", "status": "完成" },
        { "create": "卫尔容", "createdt": "1989-02-21", "receiver": "元镇国", "receivedt": "1973-02-17", "span": "5", "completedt": "1986-11-13", "place": "黑龙江省伊春市汤旺河区", "status": "拒绝" },
        { "create": "滕龙", "createdt": "1976-07-22", "receiver": "贾灵泉", "receivedt": "1993-02-01", "span": "1", "completedt": "1984-01-20", "place": "新疆维吾尔自治区和田地区和田县", "status": "完成" },
        { "create": "傅奕冰", "createdt": "1970-07-28", "receiver": "巩恒霖", "receivedt": "1978-02-01", "span": "2", "completedt": "1983-03-17", "place": "湖北省孝感市汉川市", "status": "完成" },
        { "create": "范沛凝", "createdt": "1989-03-20", "receiver": "严少", "receivedt": "1976-04-27", "span": "7", "completedt": "1979-10-20", "place": "广东省河源市紫金县", "status": "完成" },
        { "create": "顾伟祺", "createdt": "1973-09-07", "receiver": "云宇峰", "receivedt": "1985-10-30", "span": "6", "completedt": "1981-11-01", "place": "安徽省淮南市田家庵区", "status": "完成" },
        { "create": "邱雅懿", "createdt": "1993-08-16", "receiver": "匡贝", "receivedt": "1985-02-17", "span": "10", "completedt": "1993-11-17", "place": "西藏自治区日喀则地区吉隆县", "status": "完成" },
    ]
};

var db_userlist = {
    head: "帐号,密码,姓名,性别,民族,出生年月,住址,身份证号,身份证扫描件,联系电话,邮箱,QQ号码,微信号,居住地址,类别,领域",
    col: "account,pwd,name,sex,ethnic,birth,origo,id,idimg,phone,mail,qq,wechat,addr,prof,skill",
    fields: [
        { "title": "帐号", "name": "account", },
        { "title": "密码", "name": "pwd", },
        { "title": "头像", "name": "face", "type": "image" },
        { "title": "姓名", "name": "name", },
        { "title": "性别", "name": "sex", },
        { "title": "民族", "name": "ethnic", },
        { "title": "出生年月", "name": "birth", },
        { "title": "住址", "name": "origo", },
        { "title": "身份证号", "name": "id", },
        { "title": "身份证扫描件", "name": "idimg", "type": "image" },
        { "title": "联系电话", "name": "phone", },
        { "title": "邮箱", "name": "mail", },
        { "title": "QQ号码", "name": "qq", },
        { "title": "微信号", "name": "wechat", },
        { "title": "居住地址", "name": "addr", "type": "text" },
        { "title": "角色", "name": "prof", },
        { "title": "领域", "name": "skill", },
        { "title": "所在单位", "name": "depart", },
    ],
    data: [
        { "account": "gubingwei", "pwd": "gubingwei", "face": "14", "name": "顾冰薇", "sex": "女", "ethnic": "汉族", "birth": "1992-04-06", "origo": "广西壮族自治区贵港市港北区", "id": "450802199204068703", "idimg": "img/person/sfz1.jpg", "phone": "17788109922", "mail": "gubingwei@163.com", "qq": "4112408840", "wechat": "4112408840", "addr": "罗湖区东晓路", "prof": "专家", "skill": "避雷" },
        { "account": "qianzhenhai", "pwd": "qianzhenhai", "face": "3", "name": "钱振海", "sex": "男", "ethnic": "壮族", "birth": "1991-01-22", "origo": "河南省南阳市", "id": "411300199101223559", "idimg": "img/person/sfz2.jpg", "phone": "13333715119", "mail": "qianzhenhai@21cn.com", "qq": "3071619289", "wechat": "3071619289", "addr": "罗湖区蛟湖路12号大院", "prof": "队长", "skill": "工艺设计 材料" },
        { "account": "leiyixuan", "pwd": "leiyixuan", "face": "5", "name": "雷亦旋", "sex": "女", "ethnic": "汉族", "birth": "1988-02-17", "origo": "陕西省宝鸡市", "id": "610300198802174085", "idimg": "img/person/sfz3.jpg", "phone": "13333850299", "mail": "leiyixuan@sina.com", "qq": "4232830671", "wechat": "4232830671", "addr": "福田区景田东路景田市场二楼", "prof": "技工", "skill": "工艺生产" },
        { "account": "luyilv", "pwd": "luyilv", "face": "16", "name": "陆易绿", "sex": "女", "ethnic": "回族", "birth": "1987-07-08", "origo": "安徽省滁州市全椒县", "id": "341124198707088408", "idimg": "img/person/sfz4.jpg", "phone": "13333822799", "mail": "luyilv@qq.com", "qq": "4212628996", "wechat": "4212628996", "addr": "福田区园岭44栋105号", "prof": "驻场", "skill": "材料" },
        { "account": "chenjiamu", "pwd": "chenjiamu", "face": "8", "name": "陈嘉木", "sex": "男", "ethnic": "汉族", "birth": "1994-03-19", "origo": "黑龙江省伊春市上甘岭区", "id": "230716199403192899", "idimg": "img/person/sfz5.jpg", "phone": "17734800004", "mail": "chenjiamu@126.com", "qq": "53232374", "wechat": "53232374", "addr": "南山区南头常兴路11号", "prof": "风场", "skill": "安全 避雷" },
        { "account": "zhoushaoyuan", "pwd": "zhoushaoyuan", "face": "10", "name": "周绍元", "sex": "男", "ethnic": "满族", "birth": "1981-09-30", "origo": "山西省忻州地区石楼县", "id": "142328198109306719", "idimg": "img/person/sfz6.jpg", "phone": "17752555009", "mail": "zhoushaoyuan@189.cn", "qq": "4078194", "wechat": "4078194", "addr": "南山区西丽留仙大道", "prof": "调度", "skill": "避雷" },
        { "account": "dushilei", "pwd": "dushilei", "face": "4", "name": "杜诗蕾", "sex": "女", "ethnic": "汉族", "birth": "1987-11-28", "origo": "西藏自治区昌都地区察雅县", "id": "542126198711289967", "idimg": "img/person/sfz7.jpg", "phone": "17737777344", "mail": "dushilei@yeah.net", "qq": "6040078", "wechat": "6040078", "addr": "罗湖区罗沙公路经二路1号（罗湖体育局对面）", "prof": "总调", "skill": "工艺设计" },
        { "account": "luohongcai", "pwd": "luohongcai", "face": "19", "name": "罗鸿彩", "sex": "男", "ethnic": "维吾尔", "birth": "1994-08-31", "origo": "陕西省咸阳市永寿县", "id": "610426199408311938", "idimg": "img/person/sfz8.jpg", "phone": "17703717005", "mail": "luohongcai@eyou.com", "qq": "6252318817", "wechat": "6252318817", "addr": "罗湖区莲塘国威路松源大厦一楼", "prof": "仓管", "skill": "工艺生产" },
        { "account": "shimengfan", "pwd": "shimengfan", "face": "4", "name": "石梦凡", "sex": "女", "ethnic": "汉族", "birth": "1999-02-10", "origo": "四川省达川地区达川市", "id": "513001199902107844", "idimg": "img/person/sfz9.jpg", "phone": "17320111171", "mail": "shimengfan@hotmail.com", "qq": "5222926114", "wechat": "5222926114", "addr": "福田区南园街道松岭路22号", "prof": "仓主", "skill": "材料 工艺设计 工艺生产" },
        { "account": "sungangyi", "pwd": "sungangyi", "face": "2", "name": "孙刚毅", "sex": "男", "ethnic": "苗族", "birth": "1979-07-22", "origo": "贵州省六盘水市六枝特区", "id": "520203197907222079", "idimg": "img/person/sfz10.jpg", "phone": "18103711136", "mail": "sungangyi@163.com", "qq": "4060411224", "wechat": "4060411224", "addr": "龙岗区葵涌街道葵兴东路12号", "prof": "司机", "skill": "安全" },
        { "account": "xieyishuang", "pwd": "xieyishuang", "face": "20", "name": "谢依霜", "sex": "女", "ethnic": "汉族", "birth": "1991-11-12", "origo": "四川省攀枝花市盐边县", "id": "510422199111120429", "idimg": "img/person/sfz11.jpg", "phone": "13333829001", "mail": "xieyishuang@21cn.com", "qq": "1010103487", "wechat": "1010103487", "addr": "深圳市罗湖区翠竹路2028号翠竹大厦", "prof": "公众", "skill": "避雷" },
        { "account": "yanzhirong", "pwd": "yanzhirong", "face": "3", "name": "严芷容", "sex": "女", "ethnic": "彝族", "birth": "1976-12-26", "origo": "广东省韶关市仁化县", "id": "440224197612263887", "idimg": "img/person/sfz12.jpg", "phone": "13303711138", "mail": "yanzhirong@sina.com", "qq": "1010125171", "wechat": "1010125171", "addr": "罗湖区宝岗路笋岗大厦5楼", "prof": "专家", "skill": "工艺设计" },
        { "account": "yuborong", "pwd": "yuborong", "face": "9", "name": "余博容", "sex": "男", "ethnic": "汉族", "birth": "1984-02-16", "origo": "新疆维吾尔族自治区昌吉回族自治州呼图壁县", "id": "652323198402167736", "idimg": "img/person/sfz13.jpg", "phone": "18137888009", "mail": "yuborong@qq.com", "qq": "4020811715", "wechat": "4020811715", "addr": "深圳市罗湖区翠山路国防大厦", "prof": "队长", "skill": "工艺生产" },
        { "account": "chenghanfu", "pwd": "chenghanfu", "face": "17", "name": "程含芙", "sex": "女", "ethnic": "土家", "birth": "1988-02-02", "origo": "辽宁省抚顺市望花区", "id": "210404198802026601", "idimg": "img/person/sfz14.jpg", "phone": "18037773369", "mail": "chenghanfu@126.com", "qq": "3272410422", "wechat": "3272410422", "addr": "深圳市罗湖区泥岗西路1046号鸿颖大厦首层", "prof": "技工", "skill": "材料" },
        { "account": "handeze", "pwd": "handeze", "face": "15", "name": "韩德泽", "sex": "男", "ethnic": "汉族", "birth": "1985-06-24", "origo": "重庆市渝北区", "id": "500112198506248210", "idimg": "img/person/sfz15.jpg", "phone": "18100333939", "mail": "handeze@189.cn", "qq": "4212409410", "wechat": "4212409410", "addr": "福田区香蜜湖社区文化中心二楼", "prof": "驻场", "skill": "安全" },
        { "account": "jiangmurui", "pwd": "jiangmurui", "face": "8", "name": "姜慕蕊", "sex": "女", "ethnic": "藏族", "birth": "1974-06-07", "origo": "陕西省西安市市辖区", "id": "610101197406077807", "idimg": "img/person/sfz1.jpg", "phone": "13333831009", "mail": "jiangmurui@yeah.net", "qq": "1020027992", "wechat": "1020027992", "addr": "盐田区梅沙街道成坑71号", "prof": "风场", "skill": "避雷" },
        { "account": "fugaoshuang", "pwd": "fugaoshuang", "face": "1", "name": "付高爽", "sex": "男", "ethnic": "汉族", "birth": "1974-12-18", "origo": "江西省抚州地区黎川县", "id": "362523197412188175", "idimg": "img/person/sfz2.jpg", "phone": "13343849666", "mail": "fugaoshuang@eyou.com", "qq": "2902104440", "wechat": "2902104440", "addr": "南山区白石洲下白石居委会综合楼101", "prof": "调度", "skill": "工艺设计" },
        { "account": "shiyouqing", "pwd": "shiyouqing", "face": "16", "name": "石又晴", "sex": "女", "ethnic": "蒙古", "birth": "1980-08-26", "origo": "福建省宁德地区寿宁县", "id": "352229198008261144", "idimg": "img/person/sfz3.jpg", "phone": "13333818366", "mail": "shiyouqing@hotmail.com", "qq": "23623775", "wechat": "23623775", "addr": "盐田区盐田四村永安综合服务楼", "prof": "总调", "skill": "工艺生产" },
        { "account": "lanmenghuai", "pwd": "lanmenghuai", "face": "12", "name": "蓝梦槐", "sex": "女", "ethnic": "汉族", "birth": "1993-01-11", "origo": "广东省佛山市", "id": "440604199301112243", "idimg": "img/person/sfz4.jpg", "phone": "13333835119", "mail": "lanmenghuai@qq.com", "qq": "44011383", "wechat": "44011383", "addr": "罗湖区南极路南华大厦附楼（广深宾馆后）", "prof": "仓管", "skill": "材料" },
        { "account": "doujialong", "pwd": "doujialong", "face": "9", "name": "窦加隆", "sex": "男", "ethnic": "侗族", "birth": "1993-06-03", "origo": "河南省郑州市市辖区", "id": "410101199306034879", "idimg": "img/person/sfz5.jpg", "phone": "18137166646", "mail": "doujialong@126.com", "qq": "13072580", "wechat": "13072580", "addr": "盐田区沙头角园林路25号", "prof": "仓主", "skill": "安全" },
        { "account": "shenghanjia", "pwd": "shenghanjia", "face": "2", "name": "盛韩嘉", "sex": "男", "ethnic": "汉族", "birth": "1982-05-25", "origo": "辽宁省沈阳市市辖区", "id": "210101198205251717", "idimg": "img/person/sfz6.jpg", "phone": "18037155369", "mail": "shenghanjia@189.cn", "qq": "65900380", "wechat": "65900380", "addr": "宝安区九区创业一路", "prof": "司机", "skill": "避雷" },
        { "account": "changchenlin", "pwd": "changchenlin", "face": "0", "name": "常辰淋", "sex": "男", "ethnic": "布依", "birth": "1989-03-11", "origo": "安徽省芜湖市", "id": "340208198903117151", "idimg": "img/person/sfz7.jpg", "phone": "17752565757", "mail": "changchenlin@yeah.net", "qq": "1042631193", "wechat": "1042631193", "addr": "西乡宝民二路108号西乡街道办事综合楼1楼", "prof": "公众", "skill": "工艺设计 工艺生产" },
        { "account": "shudaiqiao", "pwd": "shudaiqiao", "face": "12", "name": "舒代巧", "sex": "女", "ethnic": "汉族", "birth": "1994-05-10", "origo": "青海省玉树藏族自治州治多县", "id": "63272419940510422X", "idimg": "img/person/sfz8.jpg", "phone": "18103710621", "mail": "shudaiqiao@eyou.com", "qq": "1300110784", "wechat": "1300110784", "addr": "福永街道德丰路77号（福永医院旁边）", "prof": "专家", "skill": "工艺生产" },
        { "account": "yangxinyan", "pwd": "yangxinyan", "face": "3", "name": "阳昕燕", "sex": "女", "ethnic": "瑶族", "birth": "1990-12-09", "origo": "西藏自治区昌都地区类乌齐县", "id": "54212419901209410X", "idimg": "img/person/sfz9.jpg", "phone": "17320111191", "mail": "yangxinyan@hotmail.com", "qq": "2020322207", "wechat": "17320111191", "addr": "宝安区新沙路488号107号房", "prof": "队长", "skill": "材料" },
        { "account": "bayitong", "pwd": "bayitong", "face": "8", "name": "巴以彤", "sex": "女", "ethnic": "汉族", "birth": "1984-12-27", "origo": "辽宁省大连市", "id": "210200198412279922", "idimg": "img/person/sfz10.jpg", "phone": "18103711190", "mail": "bayitong@163.com", "qq": "1042212042", "wechat": "18103711190", "addr": "宝安区松岗街道办事处3楼302室", "prof": "技工", "skill": "避雷" },
        { "account": "baoyuanliu", "pwd": "baoyuanliu", "face": "14", "name": "鲍元柳", "sex": "女", "ethnic": "白族", "birth": "1990-07-04", "origo": "湖北省省直辖行政单位神农架林区", "id": "429021199007044401", "idimg": "img/person/sfz11.jpg", "phone": "13333822009", "mail": "baoyuanliu@21cn.com", "qq": "4022426388", "wechat": "13333822009", "addr": "宝安区石岩街道前心大道国税3楼308室", "prof": "驻场", "skill": "工艺设计 材料" },
        { "account": "geganglin", "pwd": "geganglin", "face": "6", "name": "戈刚林", "sex": "男", "ethnic": "汉族", "birth": "1986-03-23", "origo": "重庆市县奉节县", "id": "500236198603237755", "idimg": "img/person/sfz12.jpg", "phone": "18939511369", "mail": "geganglin@sina.com", "qq": "5232316773", "wechat": "18939511369", "addr": "罗湖区东晓路", "prof": "风场", "skill": "工艺生产" },
        { "account": "goumidan", "pwd": "goumidan", "face": "4", "name": "勾觅丹", "sex": "女", "ethnic": "朝鲜", "birth": "1981-04-15", "origo": "河北省沧州市沧县", "id": "130921198104153164", "idimg": "img/person/sfz13.jpg", "phone": "18137888005", "mail": "goumidan@qq.com", "qq": "1040402660", "wechat": "18137888005", "addr": "罗湖区蛟湖路12号大院", "prof": "调度", "skill": "材料" },
        { "account": "miaoxinhua", "pwd": "miaoxinhua", "face": "2", "name": "苗新华", "sex": "女", "ethnic": "汉族", "birth": "1990-02-26", "origo": "云南省文山壮族苗族自治州文山县", "id": "53262119900226874X", "idimg": "img/person/sfz14.jpg", "phone": "17703866664", "mail": "miaoxinhua@126.com", "qq": "11224821", "wechat": "17703866664", "addr": "福田区景田东路景田市场二楼", "prof": "总调", "skill": "安全 避雷" },
        { "account": "qianxiaole", "pwd": "qianxiaole", "face": "3", "name": "钱小乐", "sex": "男", "ethnic": "哈尼", "birth": "1989-05-11", "origo": "湖北省宜昌市点军区", "id": "420504198905115935", "idimg": "img/person/sfz15.jpg", "phone": "13333711179", "mail": "qianxiaole@163.com", "qq": "1010107780", "wechat": "13333711179", "addr": "福田区园岭44栋105号", "prof": "仓管", "skill": "避雷" },
        { "account": "shizihan", "pwd": "shizihan", "face": "13", "name": "师子寒", "sex": "女", "ethnic": "汉族", "birth": "1991-01-06", "origo": "贵州省遵义市正安县", "id": "520324199101068400", "idimg": "img/person/sfz1.jpg", "phone": "18039578577", "mail": "shizihan@21cn.com", "qq": "5052507507", "wechat": "18039578577", "addr": "南山区南头常兴路11号", "prof": "仓主", "skill": "工艺设计" },
        { "account": "yutaoming", "pwd": "yutaoming", "face": "9", "name": "余涛鸣", "sex": "女", "ethnic": "黎族", "birth": "1994-11-03", "origo": "山东省济南市市辖区", "id": "370101199411032303", "idimg": "img/person/sfz2.jpg", "phone": "18135679789", "mail": "yutaoming@sina.com", "qq": "5423271993", "wechat": "18135679789", "addr": "南山区西丽留仙大道", "prof": "司机", "skill": "工艺生产" },
        { "account": "xiangyaoyi", "pwd": "xiangyaoyi", "face": "5", "name": "相瑶一", "sex": "男", "ethnic": "汉族", "birth": "1984-01-10", "origo": "西藏自治区山南地区措美县", "id": "542227198401107373", "idimg": "img/person/sfz3.jpg", "phone": "13323861688", "mail": "xiangyaoyi@qq.com", "qq": "1424001990", "wechat": "13323861688", "addr": "罗湖区罗沙公路经二路1号（罗湖体育局对面）", "prof": "公众", "skill": "材料 工艺设计 工艺生产" },
        { "account": "laosihan", "pwd": "laosihan", "face": "1", "name": "劳思寒", "sex": "女", "ethnic": "哈萨克", "birth": "1990-11-30", "origo": "陕西省渭南市富平县", "id": "610528199011303321", "idimg": "img/person/sfz4.jpg", "phone": "18037277737", "mail": "laosihan@126.com", "qq": "4211011995", "wechat": "18037277737", "addr": "罗湖区莲塘国威路松源大厦一楼", "prof": "专家", "skill": "安全" },
        { "account": "weiyuan", "pwd": "weiyuan", "face": "5", "name": "魏苑", "sex": "女", "ethnic": "汉族", "birth": "1978-09-22", "origo": "甘肃省甘南藏族自治州碌曲县", "id": "623026197809228004", "idimg": "img/person/sfz5.jpg", "phone": "17752555369", "mail": "weiyuan@189.cn", "qq": "4404211976", "wechat": "17752555369", "addr": "福田区南园街道松岭路22号", "prof": "队长", "skill": "避雷" },
        { "account": "gouxingyao", "pwd": "gouxingyao", "face": "2", "name": "勾星瑶", "sex": "男", "ethnic": "傣族", "birth": "1981-03-02", "origo": "河南省商丘市永城市", "id": "411481198103025774", "idimg": "img/person/sfz6.jpg", "phone": "17737700060", "mail": "gouxingyao@yeah.net", "qq": "4109001989", "wechat": "17737700060", "addr": "龙岗区葵涌街道葵兴东路12号", "prof": "技工", "skill": "工艺设计" },
        { "account": "langjia", "pwd": "langjia", "face": "6", "name": "郎佳", "sex": "女", "ethnic": "汉族", "birth": "1991-09-07", "origo": "浙江省杭州市建德市", "id": "33018219910907006X", "idimg": "img/person/sfz7.jpg", "phone": "18037311688", "mail": "langjia@eyou.com", "qq": "41272679", "wechat": "18037311688", "addr": "深圳市罗湖区翠竹路2028号翠竹大厦", "prof": "驻场", "skill": "工艺生产" },
        { "account": "baolingchun", "pwd": "baolingchun", "face": "11", "name": "鲍凌春", "sex": "女", "ethnic": "畲族", "birth": "1978-07-28", "origo": "新疆维吾尔自治区巴音郭楞蒙古自治州库尔勒市", "id": "652801197807285161", "idimg": "img/person/sfz8.jpg", "phone": "17320111161", "mail": "baolingchun@hotmail.com", "qq": "43112273", "wechat": "17320111161", "addr": "罗湖区宝岗路笋岗大厦5楼", "prof": "风场", "skill": "材料" },
        { "account": "yishuaicheng", "pwd": "yishuaicheng", "face": "1", "name": "伊帅成", "sex": "男", "ethnic": "汉族", "birth": "1981-09-28", "origo": "湖南省邵阳市武冈市", "id": "430581198109281099", "idimg": "img/person/sfz9.jpg", "phone": "17320111181", "mail": "yishuaicheng@163.com", "qq": "44162193", "wechat": "17320111181", "addr": "深圳市罗湖区翠山路国防大厦", "prof": "调度", "skill": "安全" },
        { "account": "weierrong", "pwd": "weierrong", "face": "17", "name": "卫尔容", "sex": "女", "ethnic": "傈僳", "birth": "1975-12-18", "origo": "安徽省黄山市徽州区", "id": "341004197512186248", "idimg": "img/person/sfz10.jpg", "phone": "18103711196", "mail": "weierrong@21cn.com", "qq": "41272278", "wechat": "18103711196", "addr": "深圳市罗湖区泥岗西路1046号鸿颖大厦首层", "prof": "总调", "skill": "避雷" },
        { "account": "tenglong", "pwd": "tenglong", "face": "14", "name": "滕龙", "sex": "男", "ethnic": "汉族", "birth": "1981-09-14", "origo": "黑龙江省大庆市", "id": "230600198109147973", "idimg": "img/person/sfz11.jpg", "phone": "18037888521", "mail": "tenglong@sina.com", "qq": "37050076", "wechat": "18037888521", "addr": "福田区香蜜湖社区文化中心二楼", "prof": "仓管", "skill": "工艺设计" },
        { "account": "fuyibing", "pwd": "fuyibing", "face": "5", "name": "傅奕冰", "sex": "男", "ethnic": "东乡族", "birth": "1989-05-29", "origo": "四川省南充市嘉陵区", "id": "51130419890529869X", "idimg": "img/person/sfz12.jpg", "phone": "18137888007", "mail": "fuyibing@qq.com", "qq": "23010885", "wechat": "18137888007", "addr": "盐田区梅沙街道成坑71号", "prof": "仓主", "skill": "工艺生产" },
        { "account": "fanpeining", "pwd": "fanpeining", "face": "12", "name": "范沛凝", "sex": "女", "ethnic": "汉族", "birth": "1989-02-21", "origo": "辽宁省沈阳市新民市", "id": "210181198902213320", "idimg": "img/person/sfz13.jpg", "phone": "18037888009", "mail": "fanpeining@126.com", "qq": "37070485", "wechat": "18037888009", "addr": "南山区白石洲下白石居委会综合楼101", "prof": "司机", "skill": "材料" },
        { "account": "guweiqi", "pwd": "guweiqi", "face": "4", "name": "顾伟祺", "sex": "男", "ethnic": "仡佬族", "birth": "1976-07-22", "origo": "黑龙江省伊春市汤旺河区", "id": "230712197607224317", "idimg": "img/person/sfz14.jpg", "phone": "17703717774", "mail": "guweiqi@189.cn", "qq": "13063189", "wechat": "17703717774", "addr": "盐田区盐田四村永安综合服务楼", "prof": "公众", "skill": "安全" },
        { "account": "qiuyayi", "pwd": "qiuyayi", "face": "19", "name": "邱雅懿", "sex": "男", "ethnic": "汉族", "birth": "1970-07-28", "origo": "河南省鹤壁市山城区", "id": "410603197007285492", "idimg": "img/person/sfz15.jpg", "phone": "18903844448", "mail": "qiuyayi@yeah.net", "qq": "54233879", "wechat": "18903844448", "addr": "罗湖区南极路南华大厦附楼（广深宾馆后）", "prof": "专家", "skill": "避雷" },
        { "account": "qinpancui", "pwd": "qinpancui", "face": "15", "name": "覃盼翠", "sex": "女", "ethnic": "拉祜族", "birth": "1989-03-20", "origo": "云南省德宏傣族景颇族自治州梁河县", "id": "53312219890320962X", "idimg": "img/person/sfz1.jpg", "phone": "13333812199", "mail": "qinpancui@eyou.com", "qq": "5222251986", "wechat": "13333812199", "addr": "盐田区沙头角园林路25号", "prof": "队长", "skill": "工艺设计 工艺生产" },
        { "account": "gaowenlin", "pwd": "gaowenlin", "face": "2", "name": "高文林", "sex": "男", "ethnic": "汉族", "birth": "1973-09-07", "origo": "福建省泉州市永春县", "id": "350525197309075075", "idimg": "img/person/sfz2.jpg", "phone": "13333859788", "mail": "gaowenlin@hotmail.com", "qq": "4306231991", "wechat": "13333859788", "addr": "宝安区九区创业一路", "prof": "技工", "skill": "工艺生产" },
        { "account": "mojiyao", "pwd": "mojiyao", "face": "15", "name": "莫寄瑶", "sex": "女", "ethnic": "佤族", "birth": "1993-08-16", "origo": "西藏自治区日喀则地区昂仁县", "id": "542327199308161623", "idimg": "img/person/sfz3.jpg", "phone": "18039111151", "mail": "mojiyao@qq.com", "qq": "150500179", "wechat": "18039111151", "addr": "西乡宝民二路108号西乡街道办事综合楼1楼", "prof": "驻场", "skill": "材料" },
        { "account": "fuyouqing", "pwd": "fuyouqing", "face": "20", "name": "付又青", "sex": "女", "ethnic": "汉族", "birth": "1990-08-30", "origo": "山西省晋中地区", "id": "142400199008306780", "idimg": "img/person/sfz4.jpg", "phone": "18103710062", "mail": "fuyouqing@126.com", "qq": "130534188", "wechat": "18103710062", "addr": "福永街道德丰路77号（福永医院旁边）", "prof": "风场", "skill": "避雷" },
        { "account": "weixingqing", "pwd": "weixingqing", "face": "18", "name": "韦兴庆", "sex": "男", "ethnic": "水族", "birth": "1995-12-28", "origo": "湖北省黄冈市市辖区", "id": "421101199512285196", "idimg": "img/person/sfz5.jpg", "phone": "18103710130", "mail": "weixingqing@189.cn", "qq": "623026194", "wechat": "18103710130", "addr": "宝安区新沙路488号107号房", "prof": "调度", "skill": "工艺设计 材料" },
        { "account": "xiaanmin", "pwd": "xiaanmin", "face": "0", "name": "夏安民", "sex": "男", "ethnic": "汉族", "birth": "1976-03-21", "origo": "广东省珠海市斗门县", "id": "440421197603213679", "idimg": "img/person/sfz6.jpg", "phone": "17760766636", "mail": "xiaanmin@yeah.net", "qq": "522700175", "wechat": "17760766636", "addr": "宝安区松岗街道办事处3楼302室", "prof": "总调", "skill": "工艺生产" },
        { "account": "fangzhihe", "pwd": "fangzhihe", "face": "10", "name": "方芷荷", "sex": "女", "ethnic": "纳西", "birth": "1989-08-22", "origo": "河南省濮阳市", "id": "410900198908225309", "idimg": "img/person/sfz7.jpg", "phone": "17703717009", "mail": "fangzhihe@eyou.com", "qq": "341125194", "wechat": "17703717009", "addr": "宝安区石岩街道前心大道国税3楼308室", "prof": "仓管", "skill": "材料" },
        { "account": "dingyachang", "pwd": "dingyachang", "face": "1", "name": "丁雅昶", "sex": "男", "ethnic": "汉族", "birth": "1979-12-22", "origo": "河南省周口地区郸城县", "id": "412726197912226072", "idimg": "img/person/sfz8.jpg", "phone": "17335577774", "mail": "dingyachang@hotmail.com", "qq": "430100181", "wechat": "17335577774", "addr": "罗湖区东晓路", "prof": "仓主", "skill": "安全 避雷" },
        { "account": "wanliqiang", "pwd": "wanliqiang", "face": "12", "name": "万力强", "sex": "男", "ethnic": "羌族", "birth": "1973-02-17", "origo": "湖南省永州市东安县", "id": "431122197302179832", "idimg": "img/person/sfz9.jpg", "phone": "17303858866", "mail": "wanliqiang@163.com", "qq": "510727179", "wechat": "17303858866", "addr": "罗湖区蛟湖路12号大院", "prof": "司机", "skill": "避雷" },
        { "account": "xiaoxiqin", "pwd": "xiaoxiqin", "face": "19", "name": "肖惜芹", "sex": "女", "ethnic": "汉族", "birth": "1993-02-01", "origo": "广东省河源市紫金县", "id": "441621199302010860", "idimg": "img/person/sfz10.jpg", "phone": "17788109896", "mail": "xiaoxiqin@21cn.com", "qq": "632722186", "wechat": "17788109896", "addr": "福田区景田东路景田市场二楼", "prof": "公众", "skill": "工艺设计" },
        { "account": "fangtianling", "pwd": "fangtianling", "face": "6", "name": "方天菱", "sex": "女", "ethnic": "土族", "birth": "1978-02-01", "origo": "河南省周口地区西华县", "id": "412722197802018365", "idimg": "img/person/sfz11.jpg", "phone": "17703715061", "mail": "fangtianling@sina.com", "qq": "320500190", "wechat": "17703715061", "addr": "福田区园岭44栋105号", "prof": "专家", "skill": "工艺生产" },
        { "account": "wangdanyan", "pwd": "wangdanyan", "face": "4", "name": "王丹烟", "sex": "女", "ethnic": "汉族", "birth": "1976-04-27", "origo": "山东省东营市", "id": "370500197604271286", "idimg": "img/person/sfz12.jpg", "phone": "17703716709", "mail": "wangdanyan@qq.com", "qq": "441826188", "wechat": "wangdanyan@qq.com", "addr": "南山区南头常兴路11号", "prof": "队长", "skill": "材料 工艺设计 工艺生产" },
        { "account": "ducuilan", "pwd": "ducuilan", "face": "18", "name": "杜翠岚", "sex": "女", "ethnic": "仫佬", "birth": "1985-10-30", "origo": "黑龙江省哈尔滨市平房区", "id": "230108198510300843", "idimg": "img/person/sfz13.jpg", "phone": "18903718932", "mail": "ducuilan@126.com", "qq": "360622183", "wechat": "ducuilan@126.com", "addr": "南山区西丽留仙大道", "prof": "技工", "skill": "安全" },
        { "account": "yangyiyun", "pwd": "yangyiyun", "face": "13", "name": "杨以云", "sex": "女", "ethnic": "汉族", "birth": "1985-02-17", "origo": "山东省潍坊市坊子区", "id": "370704198502175067", "idimg": "img/person/sfz14.jpg", "phone": "18903717720", "mail": "yangyiyun@yeah.net", "qq": "320412175", "wechat": "yangyiyun@yeah.net", "addr": "罗湖区罗沙公路经二路1号（罗湖体育局对面）", "prof": "驻场", "skill": "避雷" },
        { "account": "xiaolianxue", "pwd": "xiaolianxue", "face": "3", "name": "肖怜雪", "sex": "女", "ethnic": "锡伯", "birth": "1974-10-31", "origo": "云南省楚雄彝族自治州牟定县", "id": "532323197410315063", "idimg": "img/person/sfz15.jpg", "phone": "18137772520", "mail": "xiaolianxue@eyou.com", "qq": "1309271977", "wechat": "xiaolianxue@eyou.com", "addr": "罗湖区莲塘国威路松源大厦一楼", "prof": "风场", "skill": "工艺设计" },
        { "account": "quanmanyun", "pwd": "quanmanyun", "face": "19", "name": "全曼云", "sex": "女", "ethnic": "汉族", "birth": "1994-10-07", "origo": "湖南省常德市津市市", "id": "430781199410079549", "idimg": "img/person/sfz1.jpg", "phone": "13333850599", "mail": "quanmanyun@hotmail.com", "qq": "4512021979", "wechat": "quanmanyun@hotmail.com", "addr": "福田区南园街道松岭路22号", "prof": "调度", "skill": "工艺生产" },
        { "account": "yuanzhenguo", "pwd": "yuanzhenguo", "face": "3", "name": "元镇国", "sex": "男", "ethnic": "柯尔克", "birth": "1978-09-24", "origo": "宁夏回族自治区", "id": "640400197809242673", "idimg": "img/person/sfz2.jpg", "phone": "17729799989", "mail": "yuanzhenguo@qq.com", "qq": "5108021994", "wechat": "yuanzhenguo@qq.com", "addr": "龙岗区葵涌街道葵兴东路12号", "prof": "总调", "skill": "材料" },
        { "account": "jialingquan", "pwd": "jialingquan", "face": "13", "name": "贾灵泉", "sex": "女", "ethnic": "汉族", "birth": "1985-04-21", "origo": "天津市市辖区红桥区", "id": "12010619850421166X", "idimg": "img/person/sfz3.jpg", "phone": "17729799994", "mail": "jialingquan@126.com", "qq": "6527221986", "wechat": "jialingquan@126.com", "addr": "深圳市罗湖区翠竹路2028号翠竹大厦", "prof": "仓管", "skill": "安全" },
        { "account": "gonghenglin", "pwd": "gonghenglin", "face": "14", "name": "巩恒霖", "sex": "男", "ethnic": "景颇", "birth": "1993-11-18", "origo": "吉林省长春市榆树市", "id": "220182199311188015", "idimg": "img/person/sfz4.jpg", "phone": "18103710105", "mail": "gonghenglin@189.cn", "qq": "3206011992", "wechat": "gonghenglin@189.cn", "addr": "罗湖区宝岗路笋岗大厦5楼", "prof": "仓主", "skill": "避雷" },
        { "account": "yanshao", "pwd": "yanshao", "face": "0", "name": "严少", "sex": "男", "ethnic": "汉族", "birth": "1986-11-13", "origo": "广东省深圳市龙岗区", "id": "440307198611133136", "idimg": "img/person/sfz5.jpg", "phone": "18103719250", "mail": "yanshao@yeah.net", "qq": "3092115316", "wechat": "yanshao@yeah.net", "addr": "深圳市罗湖区翠山路国防大厦", "prof": "司机", "skill": "工艺设计" },
        { "account": "yunyufeng", "pwd": "yunyufeng", "face": "5", "name": "云宇峰", "sex": "男", "ethnic": "达斡尔", "birth": "1984-01-20", "origo": "河北省沧州市青县", "id": "130922198401205211", "idimg": "img/person/sfz6.jpg", "phone": "17719811988", "mail": "yunyufeng@eyou.com", "qq": "3262126874", "wechat": "yunyufeng@eyou.com", "addr": "深圳市罗湖区泥岗西路1046号鸿颖大厦首层", "prof": "公众", "skill": "工艺生产" },
        { "account": "kuangbei", "pwd": "kuangbei", "face": "13", "name": "匡贝", "sex": "女", "ethnic": "汉族", "birth": "1983-03-17", "origo": "青海省西宁市", "id": "630123198303172146", "idimg": "img/person/sfz7.jpg", "phone": "17752566606", "mail": "kuangbei@hotmail.com", "qq": "2050411593", "wechat": "kuangbei@hotmail.com", "addr": "福田区香蜜湖社区文化中心二楼", "prof": "专家", "skill": "材料" },
        { "account": "kangjingtong", "pwd": "kangjingtong", "face": "11", "name": "康靖童", "sex": "男", "ethnic": "撒拉", "birth": "1979-10-20", "origo": "山东省德州市平原县", "id": "37142619791020569X", "idimg": "img/person/sfz8.jpg", "phone": "17335577767", "mail": "kangjingtong@163.com", "qq": "2032406840", "wechat": "kangjingtong@163.com", "addr": "盐田区梅沙街道成坑71号", "prof": "队长", "skill": "安全" },
        { "account": "luomuhui", "pwd": "luomuhui", "face": "4", "name": "骆慕卉", "sex": "女", "ethnic": "汉族", "birth": "1981-11-01", "origo": "四川省甘孜藏族自治州丹巴县", "id": "513323198111014123", "idimg": "img/person/sfz9.jpg", "phone": "18137796677", "mail": "luomuhui@21cn.com", "qq": "7010103230", "wechat": "luomuhui@21cn.com", "addr": "南山区白石洲下白石居委会综合楼101", "prof": "技工", "skill": "避雷" },
        { "account": "yuwei", "pwd": "yuwei", "face": "12", "name": "俞伟", "sex": "男", "ethnic": "布朗", "birth": "1993-11-17", "origo": "湖北省黄冈市黄州区", "id": "421102199311177152", "idimg": "img/person/sfz10.jpg", "phone": "17788109926", "mail": "yuwei@sina.com", "qq": "4222710737", "wechat": "yuwei@sina.com", "addr": "盐田区盐田四村永安综合服务楼", "prof": "驻场", "skill": "工艺设计 工艺生产" },
        { "account": "yuyouyi", "pwd": "yuyouyi", "face": "11", "name": "余友易", "sex": "女", "ethnic": "汉族", "birth": "1984-03-13", "origo": "广东省河源市紫金县", "id": "441621198403134606", "idimg": "img/person/sfz11.jpg", "phone": "17703715062", "mail": "yuyouyi@qq.com", "qq": "1052830332", "wechat": "yuyouyi@qq.com", "addr": "罗湖区南极路南华大厦附楼（广深宾馆后）", "prof": "风场", "skill": "工艺生产" },
        { "account": "wujing", "pwd": "wujing", "face": "16", "name": "吴靖", "sex": "男", "ethnic": "毛南", "birth": "1980-12-18", "origo": "安徽省芜湖市马塘区", "id": "340203198012180219", "idimg": "img/person/sfz12.jpg", "phone": "18103832966", "mail": "wujing@126.com", "qq": "2302622800", "wechat": "wujing@126.com", "addr": "盐田区沙头角园林路25号", "prof": "调度", "skill": "材料" },
        { "account": "yuyiyu", "pwd": "yuyiyu", "face": "12", "name": "庾依玉", "sex": "女", "ethnic": "汉族", "birth": "1978-03-20", "origo": "河北省保定市涿州市", "id": "130681197803207788", "idimg": "img/person/sfz13.jpg", "phone": "18135777725", "mail": "yuyiyu@163.com", "qq": "1148102577", "wechat": "yuyiyu@163.com", "addr": "宝安区九区创业一路", "prof": "总调", "skill": "避雷" },
        { "account": "wankun", "pwd": "wankun", "face": "8", "name": "万坤", "sex": "男", "ethnic": "塔吉克", "birth": "1994-01-22", "origo": "福建省福州市平潭县", "id": "350128199401220171", "idimg": "img/person/sfz14.jpg", "phone": "17761666624", "mail": "wankun@21cn.com", "qq": "3018207006", "wechat": "wankun@21cn.com", "addr": "西乡宝民二路108号西乡街道办事综合楼1楼", "prof": "仓管", "skill": "工艺设计 材料" },
        { "account": "chengxintong", "pwd": "chengxintong", "face": "19", "name": "程新桐", "sex": "女", "ethnic": "汉族", "birth": "1983-04-13", "origo": "广东省广州市", "id": "440113198304138080", "idimg": "img/person/sfz15.jpg", "phone": "17703715554", "mail": "chengxintong@sina.com", "qq": "5280128516", "wechat": "chengxintong@sina.com", "addr": "福永街道德丰路77号（福永医院旁边）", "prof": "仓主", "skill": "工艺生产" },
        { "account": "aolingqin", "pwd": "aolingqin", "face": "8", "name": "敖玲沁", "sex": "女", "ethnic": "普米", "birth": "1980-02-02", "origo": "河北省张家口市尚义县", "id": "13072519800202346X", "idimg": "img/person/sfz1.jpg", "phone": "13333825099", "mail": "aolingqin@qq.com", "qq": "3058128109", "wechat": "aolingqin@qq.com", "addr": "宝安区新沙路488号107号房", "prof": "司机", "skill": "材料" },
        { "account": "nengfeng", "pwd": "nengfeng", "face": "14", "name": "能丰", "sex": "女", "ethnic": "汉族", "birth": "1980-04-06", "origo": "新疆维吾尔自治区省直辖行政单位", "id": "659003198004060508", "idimg": "img/person/sfz2.jpg", "phone": "13333828199", "mail": "nengfeng@126.com", "qq": "4100418624", "wechat": "nengfeng@126.com", "addr": "宝安区松岗街道办事处3楼302室", "prof": "公众", "skill": "安全 避雷" },
        { "account": "jilingyan", "pwd": "jilingyan", "face": "13", "name": "计翎妍", "sex": "女", "ethnic": "阿昌", "birth": "1989-10-09", "origo": "河北省保定市望都县", "id": "130631198910092446", "idimg": "img/person/sfz3.jpg", "phone": "18039111171", "mail": "jilingyan@189.cn", "qq": "3060014797", "wechat": "jilingyan@189.cn", "addr": "宝安区石岩街道前心大道国税3楼308室", "prof": "专家", "skill": "避雷" },
        { "account": "yanlechen", "pwd": "yanlechen", "face": "15", "name": "阎乐晨", "sex": "男", "ethnic": "汉族", "birth": "1979-08-02", "origo": "西藏自治区日喀则地区岗巴县", "id": "542338197908020410", "idimg": "img/person/sfz4.jpg", "phone": "18003719110", "mail": "yanlechen@yeah.net", "qq": "1130429869", "wechat": "yanlechen@yeah.net", "addr": "罗湖区东晓路", "prof": "队长", "skill": "工艺设计" },
        { "account": "lvcainan", "pwd": "lvcainan", "face": "11", "name": "吕采南", "sex": "女", "ethnic": "怒族", "birth": "1986-05-16", "origo": "贵州省铜仁地区思南县", "id": "522225198605161682", "idimg": "img/person/sfz5.jpg", "phone": "18103710926", "mail": "lvcainan@eyou.com", "qq": "1018121332", "wechat": "lvcainan@eyou.com", "addr": "罗湖区蛟湖路12号大院", "prof": "技工", "skill": "工艺生产" },
        { "account": "duxinyan", "pwd": "duxinyan", "face": "12", "name": "堵昕燕", "sex": "女", "ethnic": "汉族", "birth": "1991-08-02", "origo": "湖南省岳阳市华容县", "id": "430623199108021902", "idimg": "img/person/sfz6.jpg", "phone": "18137666629", "mail": "duxinyan@hotmail.com", "qq": "3071222431", "wechat": "duxinyan@hotmail.com", "addr": "福田区景田东路景田市场二楼", "prof": "驻场", "skill": "材料 工艺设计 工艺生产" },
        { "account": "xiaochuanjun", "pwd": "xiaochuanjun", "face": "1", "name": "萧传军", "sex": "男", "ethnic": "鄂温克", "birth": "1979-03-18", "origo": "内蒙古自治区", "id": "150500197903182637", "idimg": "img/person/sfz7.jpg", "phone": "17788177588", "mail": "xiaochuanjun@163.com", "qq": "1060328549", "wechat": "xiaochuanjun@163.com", "addr": "福田区园岭44栋105号", "prof": "风场", "skill": "安全" },
        { "account": "dengjuan", "pwd": "dengjuan", "face": "0", "name": "邓娟", "sex": "女", "ethnic": "汉族", "birth": "1988-01-30", "origo": "河北省邢台市清河县", "id": "130534198801302524", "idimg": "img/person/sfz8.jpg", "phone": "17703810086", "mail": "dengjuan@21cn.com", "qq": "3312220962", "wechat": "dengjuan@21cn.com", "addr": "南山区南头常兴路11号", "prof": "调度", "skill": "避雷" },
        { "account": "jiangzhizhuo", "pwd": "jiangzhizhuo", "face": "3", "name": "江智卓", "sex": "女", "ethnic": "京族", "birth": "1994-01-10", "origo": "甘肃省甘南藏族自治州碌曲县", "id": "623026199401105464", "idimg": "img/person/sfz9.jpg", "phone": "17335752222", "mail": "jiangzhizhuo@sina.com", "qq": "1010685", "wechat": "jiangzhizhuo@sina.com", "addr": "南山区西丽留仙大道", "prof": "总调", "skill": "工艺设计" },
        { "account": "bairongying", "pwd": "bairongying", "face": "9", "name": "柏肜瑛", "sex": "男", "ethnic": "汉族", "birth": "1975-01-23", "origo": "贵州省黔南布依族苗族自治州", "id": "522700197501237297", "idimg": "img/person/sfz10.jpg", "phone": "18037336699", "mail": "bairongying@qq.com", "qq": "2018293", "wechat": "bairongying@qq.com", "addr": "罗湖区罗沙公路经二路1号（罗湖体育局对面）", "prof": "仓管", "skill": "工艺生产" },
        { "account": "shuichengri", "pwd": "shuichengri", "face": "11", "name": "水成日", "sex": "男", "ethnic": "基诺", "birth": "1994-05-16", "origo": "安徽省滁州市定远县", "id": "341125199405169633", "idimg": "img/person/sfz11.jpg", "phone": "17788109930", "mail": "shuichengri@126.com", "qq": "4030786", "wechat": "shuichengri@126.com", "addr": "罗湖区莲塘国威路松源大厦一楼", "prof": "仓主", "skill": "材料" },
        { "account": "zhouhongtu", "pwd": "zhouhongtu", "face": "18", "name": "周宏图", "sex": "男", "ethnic": "汉族", "birth": "1981-01-01", "origo": "湖南省长沙市", "id": "43010019810101923X", "idimg": "img/person/sfz12.jpg", "phone": "17703716705", "mail": "zhouhongtu@126.com", "qq": "1092284", "wechat": "zhouhongtu@126.com", "addr": "福田区南园街道松岭路22号", "prof": "总备", "skill": "安全" },
        { "account": "qichining", "pwd": "qichining", "face": "2", "name": "齐痴凝", "sex": "女", "ethnic": "德昂", "birth": "1979-07-12", "origo": "四川省绵阳市平武县", "id": "510727197907128767", "idimg": "img/person/sfz13.jpg", "phone": "18037334789", "mail": "qichining@189.cn", "qq": "6012383", "wechat": "qichining@189.cn", "addr": "龙岗区葵涌街道葵兴东路12号", "prof": "公众", "skill": "避雷" },
        { "account": "haozitong", "pwd": "haozitong", "face": "0", "name": "郝紫瞳", "sex": "女", "ethnic": "汉族", "birth": "1986-04-23", "origo": "青海省玉树藏族自治州杂多县", "id": "632722198604237220", "idimg": "img/person/sfz14.jpg", "phone": "18037373746", "mail": "haozitong@yeah.net", "qq": "5080206870", "wechat": "haozitong@yeah.net", "addr": "深圳市罗湖区翠竹路2028号翠竹大厦", "prof": "专家", "skill": "工艺设计" },
        { "account": "yunchen", "pwd": "yunchen", "face": "5", "name": "云尘", "sex": "男", "ethnic": "保安", "birth": "1990-02-15", "origo": "江苏省苏州市", "id": "320500199002151551", "idimg": "img/person/sfz15.jpg", "phone": "13383855554", "mail": "yunchen@eyou.com", "qq": "1130022355", "wechat": "13383855554", "addr": "罗湖区宝岗路笋岗大厦5楼", "prof": "队长", "skill": "工艺生产" },
        { "account": "chuyixuan", "pwd": "chuyixuan", "face": "1", "name": "储艺璇", "sex": "女", "ethnic": "汉族", "birth": "1988-09-04", "origo": "广东省清远市连南瑶族自治县", "id": "441826198809046203", "idimg": "img/person/sfz1.jpg", "phone": "13082525268", "mail": "chuyixuan@hotmail.com", "qq": "1030017408", "wechat": "13082525268", "addr": "深圳市罗湖区翠山路国防大厦", "prof": "技工", "skill": "材料" },
        { "account": "ronghailong", "pwd": "ronghailong", "face": "4", "name": "荣海龙", "sex": "女", "ethnic": "俄罗斯", "birth": "1983-04-02", "origo": "江西省鹰潭市余江县", "id": "360622198304021564", "idimg": "img/person/sfz2.jpg", "phone": "15220202026", "mail": "ronghailong@163.com", "qq": "3142679", "wechat": "15220202026", "addr": "深圳市罗湖区泥岗西路1046号鸿颖大厦首层", "prof": "驻场", "skill": "安全" },
        { "account": "buweicheng", "pwd": "buweicheng", "face": "13", "name": "卜伟成", "sex": "男", "ethnic": "汉族", "birth": "1975-03-21", "origo": "江苏省常州市", "id": "320412197503218639", "idimg": "img/person/sfz3.jpg", "phone": "13001097739", "mail": "buweicheng@21cn.com", "qq": "5332381", "wechat": "13001097739", "addr": "福田区香蜜湖社区文化中心二楼", "prof": "风场", "skill": "避雷" },
        { "account": "manlingyi", "pwd": "manlingyi", "face": "7", "name": "满玲漪", "sex": "女", "ethnic": "裕固", "birth": "1977-08-09", "origo": "河北省沧州市南皮县", "id": "130927197708097283", "idimg": "img/person/sfz4.jpg", "phone": "15640852345", "mail": "manlingyi@sina.com", "qq": "4110293", "wechat": "15640852345", "addr": "盐田区梅沙街道成坑71号", "prof": "调度", "skill": "工艺设计 工艺生产" },
        { "account": "malingchun", "pwd": "malingchun", "face": "3", "name": "马凌春", "sex": "女", "ethnic": "汉族", "birth": "1979-04-09", "origo": "广西壮族自治区", "id": "451202197904090927", "idimg": "img/person/sfz5.jpg", "phone": "17746599939", "mail": "malingchun@qq.com", "qq": "4162184", "wechat": "17746599939", "addr": "南山区白石洲下白石居委会综合楼101", "prof": "总调", "skill": "工艺生产" },
        { "account": "fuwei", "pwd": "fuwei", "face": "11", "name": "傅微", "sex": "女", "ethnic": "乌孜别", "birth": "1994-08-20", "origo": "四川省广元市市中区", "id": "510802199408201381", "idimg": "img/person/sfz6.jpg", "phone": "13686860858", "mail": "fuwei@126.com", "qq": "3020380", "wechat": "13686860858", "addr": "盐田区盐田四村永安综合服务楼", "prof": "仓管", "skill": "材料" },
        { "account": "lingzhongji", "pwd": "lingzhongji", "face": "19", "name": "凌钟吉", "sex": "男", "ethnic": "汉族", "birth": "1986-01-14", "origo": "新疆维吾尔自治区博尔塔拉蒙古自治州精河县", "id": "652722198601141710", "idimg": "img/person/sfz7.jpg", "phone": "18636751234", "mail": "lingzhongji@yeah.net", "qq": "1068178", "wechat": "18636751234", "addr": "罗湖区南极路南华大厦附楼（广深宾馆后）", "prof": "仓主", "skill": "避雷" },
        { "account": "buzixian", "pwd": "buzixian", "face": "14", "name": "步孜娴", "sex": "男", "ethnic": "门巴", "birth": "1992-01-01", "origo": "江苏省南通市市辖区", "id": "320601199201011350", "idimg": "img/person/sfz8.jpg", "phone": "15208167567", "mail": "buzixian@eyou.com", "qq": "35012894", "wechat": "15208167567", "addr": "盐田区沙头角园林路25号", "prof": "总备", "skill": "工艺设计 材料" },
        { "account": "houxingjia", "pwd": "houxingjia", "face": "17", "name": "侯星嘉", "sex": "男", "ethnic": "汉族", "birth": "1984-08-26", "origo": "四川省成都市市辖区", "id": "510101198408267672", "idimg": "img/person/sfz9.jpg", "phone": "15699999927", "mail": "houxingjia@hotmail.com", "qq": "5101011984", "wechat": "15699999927", "addr": "宝安区九区创业一路", "prof": "公众", "skill": "工艺生产" },
        { "account": "qirenan", "pwd": "qirenan", "face": "13", "name": "齐任安", "sex": "男", "ethnic": "鄂伦春", "birth": "1991-03-08", "origo": "新疆维吾尔自治区和田地区和田县", "id": "653221199103089894", "idimg": "img/person/sfz10.jpg", "phone": "15699996944", "mail": "qirenan@qq.com", "qq": "6532211991", "wechat": "15699996944", "addr": "西乡宝民二路108号西乡街道办事综合楼1楼", "prof": "专家", "skill": "材料" },
        { "account": "baixin", "pwd": "baixin", "face": "2", "name": "柏鑫", "sex": "男", "ethnic": "汉族", "birth": "1988-10-25", "origo": "湖北省孝感市汉川市", "id": "42098419881025483X", "idimg": "img/person/sfz11.jpg", "phone": "18810000908", "mail": "baixin@126.com", "qq": "4209841988", "wechat": "18810000908", "addr": "福永街道德丰路77号（福永医院旁边）", "prof": "队长", "skill": "安全 避雷" },
        { "account": "raoyidan", "pwd": "raoyidan", "face": "19", "name": "饶忆丹", "sex": "女", "ethnic": "独龙", "birth": "1975-01-07", "origo": "广东省河源市紫金县", "id": "441621197501079386", "idimg": "img/person/sfz12.jpg", "phone": "13821825399", "mail": "raoyidan@189.cn", "qq": "4416211975", "wechat": "13821825399", "addr": "宝安区新沙路488号107号房", "prof": "技工", "skill": "避雷" },
        { "account": "sukezhu", "pwd": "sukezhu", "face": "9", "name": "宿柯朱", "sex": "男", "ethnic": "汉族", "birth": "1980-11-20", "origo": "安徽省淮南市田家庵区", "id": "340403198011200733", "idimg": "img/person/sfz13.jpg", "phone": "18088676767", "mail": "sukezhu@yeah.net", "qq": "3404031980", "wechat": "18088676767", "addr": "宝安区松岗街道办事处3楼302室", "prof": "驻场", "skill": "工艺设计" },
        { "account": "mengguangbin", "pwd": "mengguangbin", "face": "7", "name": "孟广斌", "sex": "男", "ethnic": "赫哲", "birth": "1990-09-05", "origo": "西藏自治区日喀则地区吉隆县", "id": "542335199009057797", "idimg": "img/person/sfz14.jpg", "phone": "13821138505", "mail": "mengguangbin@eyou.com", "qq": "5423351990", "wechat": "13821138505", "addr": "宝安区石岩街道前心大道国税3楼308室", "prof": "风场", "skill": "工艺生产" },
        { "account": "anyue", "pwd": "anyue", "face": "0", "name": "安悦", "sex": "男", "ethnic": "汉族", "birth": "1989-10-21", "origo": "重庆市县荣昌县", "id": "500226198910215190", "idimg": "img/person/sfz15.jpg", "phone": "18600000346", "mail": "anyue@hotmail.com", "qq": "5002261989", "wechat": "18600000346", "addr": "罗湖区东晓路", "prof": "调度", "skill": "材料 工艺设计 工艺生产" },
        { "account": "lubaitao", "pwd": "lubaitao", "face": "3", "name": "鲁白桃", "sex": "女", "ethnic": "高山", "birth": "1977-08-16", "origo": "江苏省连云港市连云区", "id": "320703197708165665", "idimg": "img/person/sfz1.jpg", "phone": "15699999974", "mail": "lubaitao@163.com", "qq": "3207031977", "wechat": "15699999974", "addr": "罗湖区蛟湖路12号大院", "prof": "总调", "skill": "安全" },
        { "account": "pingyong", "pwd": "pingyong", "face": "17", "name": "平勇", "sex": "男", "ethnic": "汉族", "birth": "1980-01-15", "origo": "四川省凉山彝族自治州木里藏族自治县", "id": "513422198001159451", "idimg": "img/person/sfz2.jpg", "phone": "15122391000", "mail": "pingyong@21cn.com", "qq": "5134221980", "wechat": "15122391000", "addr": "福田区景田东路景田市场二楼", "prof": "仓管", "skill": "避雷" },
    ]
};

var db_addition = [
    {
        certif: [{ img: "img/person/jkz1.jpg", name: "健康证", office: "福建省宁德地区疾病控制中心", issuedate: "2008.06.16" },
        { img: "img/person/gkzy1.jpg", name: "高空作业证", office: "福建省宁德安监局", issuedate: "2008.06.16" },
        { img: "img/person/dgzy1.jpg", name: "电工证", office: "福建省宁德安监局", issuedate: "2008.06.16" },
        { img: "img/person/jjz1.jpg", name: "急救证", office: "福建省红十字会", issuedate: "2008.06.16" },
        { img: "img/person/bxpz1.jpg", name: "保险凭证", office: "人保财险福建省宁德地区支公司", issuedate: "2008.06.16" }],
        edu: [{ img1: "img/person/byz1.jpg", img2: "img/person/xwz1.jpg", tmstart: "2008.06.16", qualif: "博士", tmend: "2009.07.16", edu: "清华大学" },
        { img1: "img/person/byz2.jpg", img2: "img/person/xwz2.jpg", tmstart: "2007.06.16", qualif: "硕士", tmend: "2008.06.16", edu: "北京航空航天大学" },
        { img1: "img/person/byz3.jpg", img2: "img/person/xwz3.jpg", tmstart: "2006.06.16", qualif: "学士", tmend: "2007.06.16", edu: "河南科技大学" }],
        employ: [{ img: "img/person/lzzm1.jpg", tmstart: "2008.06.16", tmend: "2009.07.16", workin: "广州联创通信技术有限公司", pos: "前台" },
        { img: "img/person/lzzm2.jpg", tmstart: "2007.06.16", tmend: "2008.06.16", workin: "惠州华特斯智能科技有限公司", pos: "检验员" },
        { img: "img/person/lzzm3.jpg", tmstart: "2006.06.16", tmend: "2007.06.16", workin: "西安晟威通信技术有限公司", pos: "研发工程师" }],
        opus: [{ img: "img/person/zp1.jpg", title: "金风科技为“中国智造”注入新动能", journal: "中国风电新闻网", date: "2015.12.31", link: "http://www.chinawindnews.com/" },
        { img: "img/person/zp2.jpg", title: "中国风电塔筒高度新纪录诞生", journal: "北极星电力新闻网", date: "2010.10.30", link: "http://www.chinawindnews.com/" },
        { img: "img/person/zp3.jpg", title: "金风科技天津首个兆瓦级分布式风电项目获批", journal: "新能源网", date: "2016.02.03", link: "http://www.chinawindnews.com/" }]
    },
    {
        certif: [{ img: "img/person/jkz2.jpg", name: "健康证", office: "江西省抚州地区疾病控制中心", issuedate: "2008.06.16" },
        { img: "img/person/gkzy2.jpg", name: "高空作业证", office: "江西省抚州地区安监局", issuedate: "2008.06.16" },
        { img: "img/person/dgzy2.jpg", name: "电工证", office: "江西省抚州地区安监局", issuedate: "2008.06.16" },
        { img: "img/person/jjz2.jpg", name: "急救证", office: "江西省抚州地区红十字会", issuedate: "2008.06.16" },
        { img: "img/person/bxpz2.jpg", name: "保险凭证", office: "江西省抚州地区人保财险", issuedate: "2008.06.16" }],
        edu: [{ img1: "img/person/byz1.jpg", img2: "img/person/xwz1.jpg", tmstart: "2008.06.16", tmend: "2009.07.16", qualif: "博士", edu: "上海交通大学" },
        { img1: "img/person/byz2.jpg", img2: "img/person/xwz2.jpg", tmstart: "2007.06.16", tmend: "2008.06.16", qualif: "硕士", edu: "南开大学" },
        { img1: "img/person/byz3.jpg", img2: "img/person/xwz3.jpg", tmstart: "2006.06.16", tmend: "2007.06.16", qualif: "学士", edu: "中国人民大学" }],
        employ: [{ img: "img/person/lzzm4.jpg", tmstart: "2008.06.16", tmend: "2009.07.16", workin: "广州联创通信技术有限公司", pos: "前台" },
        { img: "img/person/lzzm5.jpg", tmstart: "2007.06.16", tmend: "2008.06.16", workin: "惠州华特斯智能科技有限公司", pos: "检验员" },
        { img: "img/person/lzzm6.jpg", tmstart: "2006.06.16", tmend: "2007.06.16", workin: "西安晟威通信技术有限公司", pos: "研发工程师" }],
        opus: [{ img: "img/person/zp1.jpg", title: "金风科技为“中国智造”注入新动能", journal: "中国风电新闻网", date: "2015.12.31", link: "http://www.chinawindnews.com/" },
        { img: "img/person/zp2.jpg", title: "中国风电塔筒高度新纪录诞生", journal: "北极星电力新闻网", date: "2010.10.30", link: "http://www.chinawindnews.com/" },
        { img: "img/person/zp3.jpg", title: "金风科技天津首个兆瓦级分布式风电项目获批", journal: "新能源网", date: "2016.02.03", link: "http://www.chinawindnews.com/" }]
    },
    {
        certif: [{ img: "img/person/jkz3.jpg", name: "健康证", office: "陕西省西安市病控制中心", issuedate: "2008.06.16" },
        { img: "img/person/gkzy3.jpg", name: "高空作业证", office: "陕西省西安市安监局", issuedate: "2008.06.16" },
        { img: "img/person/dgzy3.jpg", name: "电工证", office: "陕西省西安市安监局", issuedate: "2008.06.16" },
        { img: "img/person/jjz3.jpg", name: "急救证", office: "陕西省西安市红十字会", issuedate: "2008.06.16" },
        { img: "img/person/bxpz3.jpg", name: "保险凭证", office: "人保财险陕西省西安市支公司", issuedate: "2008.06.16" }],
        edu: [{ img1: "img/person/byz1.jpg", img2: "img/person/xwz1.jpg", tmstart: "2008.06.16", tmend: "2009.07.16", qualif: "博士", edu: "西安交通大学" },
        { img1: "img/person/byz2.jpg", img2: "img/person/xwz2.jpg", tmstart: "2007.06.16", tmend: "2008.06.16", qualif: "硕士", edu: "武汉大学" },
        { img1: "img/person/byz3.jpg", img2: "img/person/xwz3.jpg", tmstart: "2006.06.16", tmend: "2007.06.16", qualif: "学士", edu: "厦门大学" }],
        employ: [{ img: "img/person/lzzm1.jpg", tmstart: "2008.06.16", tmend: "2009.07.16", workin: "曲阜利特莱通信器材有限公司", pos: "前台" },
        { img: "img/person/lzzm2.jpg", tmstart: "2007.06.16", tmend: "2008.06.16", workin: "山东百谷信息技术有限公司", pos: "检验员" },
        { img: "img/person/lzzm3.jpg", tmstart: "2006.06.16", tmend: "2007.06.16", workin: "昆山亿溪电子材料有限公司", pos: "研发工程师" }],
        opus: [{ img: "img/person/zp1.jpg", title: "金风科技为“中国智造”注入新动能", journal: "中国风电新闻网", date: "2015.12.31", link: "http://www.chinawindnews.com/" },
        { img: "img/person/zp2.jpg", title: "中国风电塔筒高度新纪录诞生", journal: "北极星电力新闻网", date: "2010.10.30", link: "http://www.chinawindnews.com/" },
        { img: "img/person/zp3.jpg", title: "金风科技天津首个兆瓦级分布式风电项目获批", journal: "新能源网", date: "2016.02.03", link: "http://www.chinawindnews.com/" }]
    },
    {
        certif: [{ img: "img/person/jkz4.jpg", name: "健康证", office: "辽宁省抚顺市疾病控制中心", issuedate: "2008.06.16" },
        { img: "img/person/gkzy4.jpg", name: "高空作业证", office: "辽宁省抚顺市安监局", issuedate: "2008.06.16" },
        { img: "img/person/dgzy4.jpg", name: "电工证", office: "辽宁省抚顺市安监局", issuedate: "2008.06.16" },
        { img: "img/person/jjz4.jpg", name: "急救证", office: "辽宁省抚顺市红十字会", issuedate: "2008.06.16" },
        { img: "img/person/bxpz4.jpg", name: "保险凭证", office: "人保财险辽宁省抚顺市支公司", issuedate: "2008.06.16" }],
        edu: [{ img1: "img/person/byz1.jpg", img2: "img/person/xwz1.jpg", tmstart: "2008.06.16", tmend: "2009.07.16", qualif: "博士", edu: "中南财经政法大学" },
        { img1: "img/person/byz2.jpg", img2: "img/person/xwz2.jpg", tmstart: "2007.06.16", tmend: "2008.06.16", qualif: "硕士", edu: "内蒙古大学" },
        { img1: "img/person/byz3.jpg", img2: "img/person/xwz3.jpg", tmstart: "2006.06.16", tmend: "2007.06.16", qualif: "学士", edu: "北京工商大学" }],
        employ: [{ img: "img/person/lzzm4.jpg", tmstart: "2008.06.16", tmend: "2009.07.16", workin: "天津盈禾利物流有限公司", pos: "前台" },
        { img: "img/person/lzzm5.jpg", tmstart: "2007.06.16", tmend: "2008.06.16", workin: "上海华夏物流有限公司", pos: "检验员" },
        { img: "img/person/lzzm6.jpg", tmstart: "2006.06.16", tmend: "2007.06.16", workin: "深圳戎马广告有限公司", pos: "研发工程师" }],
        opus: [{ img: "img/person/zp1.jpg", title: "金风科技为“中国智造”注入新动能", journal: "中国风电新闻网", date: "2015.12.31", link: "http://www.chinawindnews.com/" },
        { img: "img/person/zp2.jpg", title: "中国风电塔筒高度新纪录诞生", journal: "北极星电力新闻网", date: "2010.10.30", link: "http://www.chinawindnews.com/" },
        { img: "img/person/zp3.jpg", title: "金风科技天津首个兆瓦级分布式风电项目获批", journal: "新能源网", date: "2016.02.03", link: "http://www.chinawindnews.com/" }]
    }
];

var db_speech =["事常与人违，事总在人为。",
"骏马是跑出来的，强兵是打出来的。",
"驾驭命运的舵是奋斗。不抱有一丝幻想，不放弃一点机会，不停止一日努力。",
"如果惧怕前面跌宕的山岩，生命就永远只能是死水一潭。",
"懦弱的人只会裹足不前，莽撞的人只能引为烧身，只有真正勇敢的人才能所向披靡。",
"我们这个世界，从不会给一个伤心的落伍者颁发奖牌。",
"梯子的梯阶从来不是用来搁脚的，它只是让人们的脚放上一段时间，以便让别一只脚能够再往上登。",
"平时没有跑发卫千米，占时就难以进行一百米的冲刺。",
"没有激流就称不上勇进，没有山峰则谈不上攀登。",
"山路曲折盘旋，但毕竟朝着顶峰延伸。",
"只有登上山顶，才能看到那边的风光。",
"即使道路坎坷不平，车轮也要前进；即使江河波涛汹涌，船只也航行。",
"只有创造，才是真正的享受，只有拚搏，才是充实的生活。",
"敢于向黑暗宣战的人，心里必须充满光明。",
"崇高的理想就象生长在高山上的鲜花。如果要搞下它，勤奋才能是攀登的绳索。",
"种子牢记着雨滴献身的叮嘱，增强了冒尖的勇气。",
"自然界没有风风雨雨，大地就不会春华秋实。",
"只会幻想而不行动的人，永远也体会不到收获果实时的喜悦。",
"勤奋是你生命的密码，能译出你一部壮丽的史诗。",
"对于攀登者来说，失掉往昔的足迹并不可惜，迷失了继续前时的方向却很危险。",
"奋斗者在汗水汇集的江河里，将事业之舟驶到了理想的彼岸。",
"忙于采集的蜜蜂，无暇在人前高谈阔论。",
"勇士搏出惊涛骇流而不沉沦，懦夫在风平浪静也会溺水。",
"志在峰巅的攀登者，不会陶醉在沿途的某个脚印之中。",
"海浪为劈风斩浪的航船饯行，为随波逐流的轻舟送葬。",
"山路不象坦途那样匍匐在人们足下。",
"激流勇进者方能领略江河源头的奇观胜景。",
"如果圆规的两只脚都动，永远也画不出一个圆。",
"如果你想攀登高峰，切莫把彩虹当作梯子。",
"脚步怎样才能不断前时？把脚印留在身后。",
"不管多么险峻的高山，总是为不畏艰难的人留下一条攀登的路。",
"让生活的句号圈住的人，是无法前时半步的。",
"只要能收获甜蜜，荆棘丛中也会有蜜蜂忙碌的身影。",
"进取乾用汗水谱烈军属着奋斗和希望之歌。",
"生活呆以是甜的，也可以是苦的，但不能是没味的。你可以胜利，也可以失败，但你不能屈服。",
"向你的美好的希冀和追求撒开网吧，九百九十九次落空了，还有一千次呢......",
"机会只对进取有为的人开放,庸人永远无法光顾.",
"只会在水泥地上走路的人,永远不会留下深深的脚印.",
"生命力的意义在于拚搏,因为世界本身就是一个竞技场.",
"海浪的品格,就是无数次被礁石击碎又无数闪地扑向礁石.",
"榕树因为扎根于深厚的土壤,生命的绿荫才会越长越茂盛.稗子享受着禾苗一样的待遇,结出的却不是谷穗.",
"骄傲,是断了引线的风筝,稍纵即逝;自卑,是剪了双翼的飞鸟,难上青天.这两者都是成才的大忌.",
"树苗如果因为怕痛而拒绝修剪,那就永远不会成材.",
"经过大海的一番磨砺,卵石才变得更加美丽光滑.",
"生活的激流已经涌现到万丈峭壁,只要再前进一步,就会变成壮丽的瀑布.",
"向前吧,荡起生命之舟,不必依恋和信泊,破浪的船自会一路开放常新的花朵.",
"盆景秀木正因为被人溺爱,才破灭了成为栋梁之材的梦.",
"如果把才华比作剑,那么勤奋就是磨刀石.",
"经受了火的洗礼泥巴也会有坚强的体魄.",
"山涧的泉水经过一路曲折,才唱出一支美妙的歌.",
"瀑布跨过险峻陡壁时，才显得格外雄伟壮观。",
"通过云端的道路，只亲吻攀登者的足迹。",
"彩云飘在空中，自然得意洋洋，但最多只能换取几声赞美；唯有化作甜雨并扎根于沃壤之中，才能给世界创造芳菲。",
"教育是人才的娘家，社会是人才的婆家。",
"桂冠上的飘带，不是用天才纤维捻制而成的，而是用痛苦，磨难的丝缕纺织出来的。",
"没有一颗珍珠的闪光，是靠别人涂抹上去的。",
"沙漠里的脚印很快就消逝了。一支支奋进歌却在跋涉者的心中长久激荡。",
"你既然认准一条道路，何必去打听要走多久。",
"如果为了安全而不和大海在一起，船就失去了存在的意义。",
"蝴蝶如要在百花园里得到飞舞的欢乐，那首先得忍受与蛹决裂的痛苦。",
"萤火虫的光点虽然微弱，但亮着便是向黑暗挑战。",
"拒绝严峻的冶炼，矿石并不比被发掘前更有价值。",
"要想成为强乾，决不能绕过挡道的荆棘也不能回避风雨的冲刷。",
"行路人，用足音代替叹息吧！",
"假如你从来未曾害怕、受窘、受伤害，好就是你从来没有冒过险。",
"耕耘者最信和过自己的汗水，每一滴都孕育着一颗希望的种子。",
"只有脚踏实地的人，才能够说：路，就在我的脚下。",
"美丽的蓝图，落在懒汉手里，也不过是一页废纸。",
"一时的挫折往往可以通过不屈的搏击，变成学问及见识。",
"努力向上的开拓，才使弯曲的竹鞭化作了笔直的毛竹。",
"竹根---即使被埋在地下无人得见，也决然不会停止探索而力争冒出新笋。",
"希望，只有和勤奋作伴，才能如虎添翼。",
"沉湎于希望的人和守株待兔的樵夫没有什么两样。",
"没有风浪，便没有勇敢的弄潮儿；没有荆棘，也没有不屈的开拓者。",
"世上所有美好的感情加在一起，也抵不上一桩高尚的行动。",
"奋斗的双脚在踏碎自己的温床时，却开拓了一条创造之路。",
"站在巨人的肩上是为了超过巨人。",
"泉水，奋斗之路越曲折，心灵越纯洁。",
"如果缺少破土面出并与风雪拚搏的勇气，种子的前途并不比落叶美妙一分。",
"竹笋虽然柔嫩，但它不怕重压，敢于奋斗、敢于冒尖。",
"不要让追求之舟停泊在幻想的港湾，而应扬起奋斗的风帆，驶向现实生活的大海。",
"智者的梦再美，也不如愚人实干的脚印。",
"耕耘者的汗水是哺育种子成长的乳汁。",
"不去耕耘，不去播种，再肥的沃土也长不出庄稼，不去奋斗，不去创造，再美的青春也结不出硕果。",
"让珊瑚远离惊涛骇浪的侵蚀吗？那无异是将它们的美丽葬送。",
"再好的种子，不播种下去，也结不出丰硕的果实。",
"如果可恨的挫折使你尝到苦果，朋友，奋起必将让你尝到人生的欢乐。",
"瀑布---为了奔向江河湖海，即使面临百丈深渊，仍然呼啸前行，决不退缩",
"对于勇士来说，贫病、困窘、责难、诽谤、冷嘲热讽......，一切压迫都是前进的动力。",
"不从泥泞不堪的小道上迈步，就踏不上铺满鲜花的大路。",
"幻想在漫长的生活征途中顺水行舟的人，他的终点在下游。只有敢于扬起风帆，顶恶浪的勇士，才能争到上游。",
"望远镜---可以望见远的目标，却不能代替你走半步。",
"不要嘲笑铁树。为了开一次花，它付出了比别的树种更长久的努力。",
"生命力顽强的种子，从不对瘠土唱诅咒的歌。",
"只要不放弃努力和追求，小草也有点缀春天的价值。",
"松软的沙滩上最容易留下脚印。钽也最容易被潮水抹去。",
"惊叹号是勇士滴在攀登路上的血，也是懦夫失望时流淌的泪。",
"一帆风顺，并不等于行驶的是一条平坦的航线。",
"在茫茫沙漠，唯有前时进的脚步才是希望的象征。",
"攀登山顶的脚力，生于欲穷千里目的壮心和不到长城非好汉的意志。",
"忍辛负重的耕牛，留下的脚印最清晰。",
"帆的自豪，是能在风浪中挺起胸膛。",
"愚蠢的人总是为昨天悔恨，为明天祈祷，可惜的是少了今天的努力。",
"跑昨越快，遇到风的阻力越大。阻力与成就相伴随。",
"天赋是埋藏在矿里的黄金，才能是挖掘矿藏的矿工。",
"翘首盼来的春天属于大自然，用手织出的春天才属于自己。",
"战士的意志要象礁石一样坚定，战士的性格要象和风一样温柔。",
"谁把安逸当成幸福的花朵，那么等到结果时节，他只能望着空枝叹息。",
"太阳虽有黑点，却在奋力燃烧中树立了光辉的形象。",
"努力就是光，成功就是影。没有光哪儿来影？",
"岸边的奇花异草，是拘留不住奔腾向前的江水的。",
"没有斗狼的胆量，就不要牧羊。",
"路灯经过一夜的努力，才无愧地领受第一缕晨光的抚慰。",
"不安于现状，不甘于平庸，就可能在勇于进取的奋斗中奏响人生壮美的乐间。",
"涓涓细流一旦停止了喧哗，浩浩大海也就终止了呼吸。",
"只要是辛勤的蜜蜂，在生活的广阔原野里，到处都可以找到蜜源。",
"勤奋的含义是今天的热血，而不是明天的决心，后天的保证。",
"鞋底磨穿了，不等于路走到了头。",
"事业的大厦如缺乏毅力的支柱，只能是空中楼阁。",
"只有收获，才能检验耕耘的意义；只有贡献，方可衡量人生的价值。",
"幻想者头脑里只有空中楼阁，实干家胸中才有摩天大厦。",
"长蔓植物依附着支物向上爬，当它爬到比支撑它的支物不高时，它又窥伺着另一株支物。",
"望洋兴叹的人，永远达不到成功的彼岸。",
"沿着别人走出的道路前进时，应该踩着路边的荆棘，因为这样走多了，就能使道路增宽。",
"新路开始常是狭窄的，但它却是自己延伸拓宽的序曲。",
"闲适和宁静，对于浪花，意味着死亡。",
"如果脆弱的心灵创伤太多，朋友，追求才是愈合你伤口最好的良药。",
"马行软地易失蹄，人贪安逸易失志。",
"松驰的琴弦，永远奏不出时代的强音。",
"撒进奋斗的沃土，一滴汗珠就是一颗孕育希望的良种。",
"根儿向纵深处延伸一寸，小树被狂风推倒的危险就减弱了一分。",
"在懒汉的眼里，汗是苦的，脏的，在勤者的心上，汗是甜的，在勤者的心上，汗是甜的，美的。",
"压力---在事业成功的道路上，你是无知者颓丧的前奏，更是有志者奋进的序曲。",
"在避风的港湾里，找不到昂扬的帆。",
"空谈家用空谈来装饰自己，实干家用实干去创造业绩。",
"英雄的事业必定包含着艰险，如果没有艰险也就不成为英雄了。",
"如果刀刃怕伤了自己而不与磨刀石接触，就永远不会锋利。",
"有建树的人，并非具备了比一般人更优越的条件，相反，他们要经过更多的磨练，走更艰辛的路。",
"实干家在沙漠里也能开垦出绿洲，懒惰者在沃野上也不会获得丰收。",
"不举步，越不守栅栏，不迈腿，登不上高山。",
"消沉就角一支单调的画笔，只能给未来涂上一层灰色。",
"假如樵夫害怕荆棘，船只避忌风浪，铁匠畏惧火星，那么，世界就会变成另一副模样。",
"收获是事业的雨量计；聚集着奋斗者洒落的每滴汗珠。",
"无穷的伟大，也是从一开始的。",
"花的生命虽然短暂，但它毕竟拥抱过春天。",
"天才之舟，在汗水的河流里启程。",
"在林荫路上散步不值得称赞，攀登险峰才有真正的乐趣。",
"懒惰包含着永久的失望。",
"希望是美好的，她令人神往、追求、但是希望伴随着风浪。贪图安逸的人，他的希望不过是一带道路、一种幻境，只有敢于和狂风巨浪拚搏的人，希望才会开出鲜花，结出硕果。",
"小溪---在生命的长河里，你前进的步伐每时每刻都拨动着大海心中的琴弦。",
"如果把成才比作登天，自学便是成才的天梯。",
"只有脚踏实地的人，大地才乐意留下他的脚印。",
"钢钎与顽石的碰撞声，是一首力的歌曲。",
"贪图省力的船夫，目标永远下游。",
"浪花永不凋萎的秘诀：永远追求不安闲的生活。",
"要是你的心本来就在燃烧，那么一旦需要，掏出来就可以当火把。",
"纤夫在河边留下一串脚印，那是跋涉者生活的省略号。",
"眼睛里没有追求的时候，一定是心如死灰的时候。",
"蚌下苦轼的时候是不作声的，献出来的终于是明珠。",
"与其是无数遍地重温那个虚幻的玫瑰式的梦，还不如去一个静静的湖畔采一朵金黄色的野菊花。",
"踏着过去的脚印，不会增加新的脚印。",
"痛苦的记忆是泪水洗不净的，只有汗水才能把它冲掉。",
"只要你想种下美好记忆的种子，便能找到你心灵中的处女地。开垦吧，现在就开始。",
"攀登者智慧和汗水，构思着一首信念和意志的长诗。",
"执着的攀登者不必去与别人比较自己的形象是否高大，重要的是要多多思考自己前进的脚步是否扎实。",
"埋首俯身，全为了奋力向上，并不是对头上的太阳缺乏感情。",
"腰板挺得笔直的人，终究不会走在攀登者队伍的前列。",
"浪花，从不伴随躲在避风港的小表演，而始终追赶着拚搏向前的巨轮。",
"克服困难，勇敢者自有千方百计，怯懦者只感到万般无奈。",
"燕子嘴上的春泥，别看它点点滴滴，筑不成大厦，却能垒起幸福之巢。",
"砖---经受过炉火的考验，才有资格成为大厦的一员。",
"正是礁石的阻挡，才使浪花显得美丽。",
"在逆境中要看到生活的美，在希望中别忘记不断奋斗。",
"为了成材，松树从不向四季如春的温室外献殷勤。",
"松树在悬崖峭壁上巍然挺立，雄风不衰，是因为它具有勇于傲霜斗雪的内在气质。",
"盲人眼前虽然一片漆黑，但脚下同样可以开拓出一条光明的路.",
"荆棘、坎坷是磨砺开拓者意志的摇复；困难艰险，是开拓者前进路上的垫脚石。",
"勤奋可以弥补聪明的不足，但聪明无法弥补懒惰的缺陷。",
"停止奋斗的脚步，江河就会沦为一潭死水。",
"在为事业奋斗的征途上，拄着双拐的人虽然步履艰难，但只要有一颗奋发不息的心则可以登上成功的峰巅的。",
"浪花总是着扬帆者的路开放的。",
"离开奋斗的沃壤，天赋的种子便寻不到春华秋实的前程。",
"同样的旋车，车轮不知前进了多少，陀螺却仍在原处。",
"小鸟眷恋春天，因为它懂得飞翔才是生命的价值。",
"为了走上成材的道路，钢铁决不惋惜璀璨的钢花被遗弃。",
"开拓者走的是弯弯曲曲的路，而他留下的却是又直又宽的足迹。",
"海浪宁可在挡路的礁山上撞得粉碎，也不肯后退一步。",
"即使脚步下是一片岩石，它也会迸发出火花，只要你拿起铁锤钢钎。",
"上游，是勇士劈风破浪的终点，下游，是懦夫一帆风顺的归宿。",
"躺在被窝里的人，并不感到太阳的温暖。",
"人最可悲的是自己不能战胜自己。",
"奋斗者的幸福是从痛苦起步的，享乐者的痛苦是从幸福开始的。",
"沟潭之水，凝滞沉闷，飞瀑之流，奋迅高亢——同是为水，性却异，前者满足安逸，后者进取不已。", ]

var db_troublelist = {
    head: "编号,报修人,报修时间,故障类别,所属风场,图片或视频,故障说明,状态",
    col: "code,create,createdt,type,winder,img,remark,status",
    fields: [{"title":"编号","name":"code",},
            {"title":"报修人","name":"create",},
            {"title":"报修时间","name":"createdt","class":"datetime"},
            {"title":"故障类别","name":"type",},
            {"title":"所属风场","name":"winder",},
            {"title":"图片或视频","name":"img","class":"relate"},
            {"title":"故障说明","name":"remark",},
            {"title":"状态","name":"status",},
            ],
    data: [
{"code":"920406870","create":"顾冰薇","createdt":"1992-04-06","type":"叶片断裂","winder":"十里画屏风场","remark":"经受了火的洗礼泥巴也会有坚强的体魄.","status":"编辑","phone":"17788109922"},
{"code":"910122355","create":"钱振海","createdt":"1991-01-22","type":"叶片裂纹","winder":"官厅水库风场","remark":"山涧的泉水经过一路曲折,才唱出一支美妙的歌.","status":"编辑","phone":"13333715119"},
{"code":"880217408","create":"雷亦旋","createdt":"1988-02-17","type":"风化脱漆","winder":"十度风场","remark":"瀑布跨过险峻陡壁时，才显得格外雄伟壮观。","status":"编辑","phone":"13333850299"},
{"code":"870708840","create":"陆易绿","createdt":"1987-07-08","type":"过热起火","winder":"康西草原风场","remark":"通过云端的道路，只亲吻攀登者的足迹。","status":"编辑","phone":"13333822799"},
{"code":"940319289","create":"陈嘉木","createdt":"1994-03-19","type":"风沙侵蚀","winder":"八达岭风场","remark":"彩云飘在空中，自然得意洋洋，但最多只能换取几声赞美；唯有化作甜雨并扎根于沃壤之中，才能给世界创造芳菲。","status":"等待受理","phone":"17734800004"},
{"code":"810930671","create":"周绍元","createdt":"1981-09-30","type":"叶片断裂","winder":"新王府井风场","remark":"教育是人才的娘家，社会是人才的婆家。","status":"等待受理","phone":"17752555009"},
{"code":"871128996","create":"杜诗蕾","createdt":"1987-11-28","type":"叶片裂纹","winder":"东大桥风场","remark":"桂冠上的飘带，不是用天才纤维捻制而成的，而是用痛苦，磨难的丝缕纺织出来的。","status":"等待受理","phone":"17737777344"},
{"code":"940831193","create":"罗鸿彩","createdt":"1994-08-31","type":"风化脱漆","winder":"华威风场","remark":"没有一颗珍珠的闪光，是靠别人涂抹上去的。","status":"等待受理","phone":"17703717005"},
{"code":"990210784","create":"石梦凡","createdt":"1999-02-10","type":"过热起火","winder":"京宝风场","remark":"沙漠里的脚印很快就消逝了。一支支奋进歌却在跋涉者的心中长久激荡。","status":"撤回","phone":"17320111171"},
{"code":"790722207","create":"孙刚毅","createdt":"1979-07-22","type":"风沙侵蚀","winder":"劲松风场","remark":"你既然认准一条道路，何必去打听要走多久。","status":"撤回","phone":"18103711136"},
{"code":"911112042","create":"谢依霜","createdt":"1991-11-12","type":"叶片断裂","winder":"海淀风场","remark":"如果为了安全而不和大海在一起，船就失去了存在的意义。","status":"撤回","phone":"13333829001"},
{"code":"761226388","create":"严芷容","createdt":"1976-12-26","type":"叶片裂纹","winder":"白广路风场","remark":"蝴蝶如要在百花园里得到飞舞的欢乐，那首先得忍受与蛹决裂的痛苦。","status":"撤回","phone":"13303711138"},
{"code":"840216773","create":"余博容","createdt":"1984-02-16","type":"风化脱漆","winder":"万通风场","remark":"萤火虫的光点虽然微弱，但亮着便是向黑暗挑战。","status":"退回","phone":"18137888009"},
{"code":"880202660","create":"程含芙","createdt":"1988-02-02","type":"过热起火","winder":"古城风场","remark":"拒绝严峻的冶炼，矿石并不比被发掘前更有价值。","status":"编辑","phone":"18037773369"},
{"code":"850624821","create":"韩德泽","createdt":"1985-06-24","type":"风沙侵蚀","winder":"亚运村风场","remark":"要想成为强乾，决不能绕过挡道的荆棘也不能回避风雨的冲刷。","status":"编辑","phone":"18100333939"},
{"code":"740607780","create":"姜慕蕊","createdt":"1974-06-07","type":"叶片断裂","winder":"小庄风场","remark":"行路人，用足音代替叹息吧！","status":"编辑","phone":"13333831009"},
{"code":"741218817","create":"付高爽","createdt":"1974-12-18","type":"叶片裂纹","winder":"左家庄风场","remark":"假如你从来未曾害怕、受窘、受伤害，好就是你从来没有冒过险。","status":"编辑","phone":"13343849666"},
{"code":"800826114","create":"石又晴","createdt":"1980-08-26","type":"风化脱漆","winder":"航天桥风场","remark":"耕耘者最信和过自己的汗水，每一滴都孕育着一颗希望的种子。","status":"等待受理","phone":"13333818366"},
{"code":"930111224","create":"蓝梦槐","createdt":"1993-01-11","type":"过热起火","winder":"军博风场","remark":"只有脚踏实地的人，才能够说：路，就在我的脚下。","status":"等待受理","phone":"13333835119"},
{"code":"930603487","create":"窦加隆","createdt":"1993-06-03","type":"风沙侵蚀","winder":"三里河风场","remark":"美丽的蓝图，落在懒汉手里，也不过是一页废纸。","status":"等待受理","phone":"18137166646"},
{"code":"820525171","create":"盛韩嘉","createdt":"1982-05-25","type":"叶片断裂","winder":"黄庄风场","remark":"一时的挫折往往可以通过不屈的搏击，变成学问及见识。","status":"等待受理","phone":"18037155369"},
{"code":"890311715","create":"常辰淋","createdt":"1989-03-11","type":"叶片裂纹","winder":"贵友风场","remark":"努力向上的开拓，才使弯曲的竹鞭化作了笔直的毛竹。","status":"撤回","phone":"17752565757"},
{"code":"940510422","create":"舒代巧","createdt":"1994-05-10","type":"风化脱漆","winder":"洋桥风场","remark":"竹根---即使被埋在地下无人得见，也决然不会停止探索而力争冒出新笋。","status":"撤回","phone":"18103710621"},
{"code":"901209410","create":"阳昕燕","createdt":"1990-12-09","type":"过热起火","winder":"国华风场","remark":"希望，只有和勤奋作伴，才能如虎添翼。","status":"撤回","phone":"17320111191"},
{"code":"841227992","create":"巴以彤","createdt":"1984-12-27","type":"风沙侵蚀","winder":"建国门风场","remark":"沉湎于希望的人和守株待兔的樵夫没有什么两样。","status":"撤回","phone":"18103711190"},
{"code":"900704440","create":"鲍元柳","createdt":"1990-07-04","type":"叶片断裂","winder":"成府路风场","remark":"没有风浪，便没有勇敢的弄潮儿；没有荆棘，也没有不屈的开拓者。","status":"退回","phone":"13333822009"},
{"code":"860323775","create":"戈刚林","createdt":"1986-03-23","type":"叶片裂纹","winder":"新安风场","remark":"世上所有美好的感情加在一起，也抵不上一桩高尚的行动。","status":"评估","phone":"18939511369"},
{"code":"810415316","create":"勾觅丹","createdt":"1981-04-15","type":"风化脱漆","winder":"丰台桥南风场","remark":"奋斗的双脚在踏碎自己的温床时，却开拓了一条创造之路。","status":"评估","phone":"18137888005"},
{"code":"900226874","create":"苗新华","createdt":"1990-02-26","type":"过热起火","winder":"牡丹园风场","remark":"站在巨人的肩上是为了超过巨人。","status":"评估","phone":"17703866664"},
{"code":"890511593","create":"钱小乐","createdt":"1989-05-11","type":"风沙侵蚀","winder":"芳城园风场","remark":"泉水，奋斗之路越曲折，心灵越纯洁。","status":"评估","phone":"13333711179"},
{"code":"910106840","create":"师子寒","createdt":"1991-01-06","type":"叶片断裂","winder":"甜水园风场","remark":"如果缺少破土面出并与风雪拚搏的勇气，种子的前途并不比落叶美妙一分。","status":"评估","phone":"18039578577"},
{"code":"941103230","create":"余涛鸣","createdt":"1994-11-03","type":"叶片裂纹","winder":"中粮广场风场","remark":"竹笋虽然柔嫩，但它不怕重压，敢于奋斗、敢于冒尖。","status":"评估","phone":"18135679789"},
{"code":"840110737","create":"相瑶一","createdt":"1984-01-10","type":"风化脱漆","winder":"新东安风场","remark":"不要让追求之舟停泊在幻想的港湾，而应扬起奋斗的风帆，驶向现实生活的大海。","status":"评估","phone":"13323861688"},
{"code":"901130332","create":"劳思寒","createdt":"1990-11-30","type":"过热起火","winder":"苏州桥风场","remark":"智者的梦再美，也不如愚人实干的脚印。","status":"评估","phone":"18037277737"},
{"code":"780922800","create":"魏苑","createdt":"1978-09-22","type":"风沙侵蚀","winder":"翠微路风场","remark":"耕耘者的汗水是哺育种子成长的乳汁。","status":"评估","phone":"17752555369"},
{"code":"810302577","create":"勾星瑶","createdt":"1981-03-02","type":"叶片断裂","winder":"交道口风场","remark":"不去耕耘，不去播种，再肥的沃土也长不出庄稼，不去奋斗，不去创造，再美的青春也结不出硕果。","status":"评估","phone":"17737700060"},
{"code":"910907006","create":"郎佳","createdt":"1991-09-07","type":"叶片裂纹","winder":"团结湖风场","remark":"让珊瑚远离惊涛骇浪的侵蚀吗？那无异是将它们的美丽葬送。","status":"评估","phone":"18037311688"},
{"code":"780728516","create":"鲍凌春","createdt":"1978-07-28","type":"风化脱漆","winder":"双榆树风场","remark":"再好的种子，不播种下去，也结不出丰硕的果实。","status":"评估","phone":"17320111161"},
{"code":"810928109","create":"伊帅成","createdt":"1981-09-28","type":"过热起火","winder":"怀柔风场","remark":"如果可恨的挫折使你尝到苦果，朋友，奋起必将让你尝到人生的欢乐。","status":"维修","phone":"17320111181"},
{"code":"751218624","create":"卫尔容","createdt":"1975-12-18","type":"风沙侵蚀","winder":"昌平风场","remark":"瀑布---为了奔向江河湖海，即使面临百丈深渊，仍然呼啸前行，决不退缩","status":"维修","phone":"18103711196"},
{"code":"810914797","create":"滕龙","createdt":"1981-09-14","type":"叶片断裂","winder":"潘家园风场","remark":"对于勇士来说，贫病、困窘、责难、诽谤、冷嘲热讽......，一切压迫都是前进的动力。","status":"维修","phone":"18037888521"},
{"code":"890529869","create":"傅奕冰","createdt":"1989-05-29","type":"叶片裂纹","winder":"复兴门风场","remark":"不从泥泞不堪的小道上迈步，就踏不上铺满鲜花的大路。","status":"维修","phone":"18137888007"},
{"code":"890221332","create":"范沛凝","createdt":"1989-02-21","type":"风化脱漆","winder":"玉泉路风场","remark":"幻想在漫长的生活征途中顺水行舟的人，他的终点在下游。只有敢于扬起风帆，顶恶浪的勇士，才能争到上游。","status":"维修","phone":"18037888009"},
{"code":"760722431","create":"顾伟祺","createdt":"1976-07-22","type":"过热起火","winder":"右安门外风场","remark":"望远镜---可以望见远的目标，却不能代替你走半步。","status":"维修","phone":"17703717774"},
{"code":"700728549","create":"邱雅懿","createdt":"1970-07-28","type":"风沙侵蚀","winder":"和平街北口风场","remark":"不要嘲笑铁树。为了开一次花，它付出了比别的树种更长久的努力。","status":"维修","phone":"18903844448"},
{"code":"890320962","create":"覃盼翠","createdt":"1989-03-20","type":"叶片断裂","winder":"清河风场","remark":"生命力顽强的种子，从不对瘠土唱诅咒的歌。","status":"维修","phone":"13333812199"},
{"code":"730907507","create":"高文林","createdt":"1973-09-07","type":"叶片裂纹","winder":"三元风场","remark":"只要不放弃努力和追求，小草也有点缀春天的价值。","status":"维修","phone":"13333859788"},
{"code":"930816162","create":"莫寄瑶","createdt":"1993-08-16","type":"风化脱漆","winder":"新世界风场","remark":"松软的沙滩上最容易留下脚印。钽也最容易被潮水抹去。","status":"维修","phone":"18039111151"},
{"code":"900830678","create":"付又青","createdt":"1990-08-30","type":"过热起火","winder":"十里画屏风场","remark":"惊叹号是勇士滴在攀登路上的血，也是懦夫失望时流淌的泪。","status":"维修","phone":"18103710062"},
{"code":"951228519","create":"韦兴庆","createdt":"1995-12-28","type":"风沙侵蚀","winder":"官厅水库风场","remark":"一帆风顺，并不等于行驶的是一条平坦的航线。","status":"维修","phone":"18103710130"},
{"code":"760321367","create":"夏安民","createdt":"1976-03-21","type":"叶片断裂","winder":"十度风场","remark":"在茫茫沙漠，唯有前时进的脚步才是希望的象征。","status":"完成","phone":"17760766636"},
{"code":"890822530","create":"方芷荷","createdt":"1989-08-22","type":"叶片裂纹","winder":"康西草原风场","remark":"攀登山顶的脚力，生于“欲穷千里目”的壮心和“不到长城非好汉”的意志。","status":"完成","phone":"17703717009"},
{"code":"791222607","create":"丁雅昶","createdt":"1979-12-22","type":"风化脱漆","winder":"八达岭风场","remark":"忍辛负重的耕牛，留下的脚印最清晰。","status":"完成","phone":"17335577774"},
{"code":"730217983","create":"万力强","createdt":"1973-02-17","type":"过热起火","winder":"新王府井风场","remark":"帆的自豪，是能在风浪中挺起胸膛。","status":"完成","phone":"17303858866"},
{"code":"930201086","create":"肖惜芹","createdt":"1993-02-01","type":"风沙侵蚀","winder":"东大桥风场","remark":"愚蠢的人总是为昨天悔恨，为明天祈祷，可惜的是少了今天的努力。","status":"完成","phone":"17788109896"},
{"code":"780201836","create":"方天菱","createdt":"1978-02-01","type":"叶片断裂","winder":"华威风场","remark":"跑昨越快，遇到风的阻力越大。阻力与成就相伴随。","status":"完成","phone":"17703715061"},
{"code":"760427128","create":"王丹烟","createdt":"1976-04-27","type":"叶片裂纹","winder":"京宝风场","remark":"天赋是埋藏在矿里的黄金，才能是挖掘矿藏的矿工。","status":"完成","phone":"17703716709"},
{"code":"851030084","create":"杜翠岚","createdt":"1985-10-30","type":"风化脱漆","winder":"劲松风场","remark":"翘首盼来的春天属于大自然，用手织出的春天才属于自己。","status":"完成","phone":"18903718932"},
{"code":"850217506","create":"杨以云","createdt":"1985-02-17","type":"过热起火","winder":"海淀风场","remark":"战士的意志要象礁石一样坚定，战士的性格要象和风一样温柔。","status":"完成","phone":"18903717720"},
{"code":"741031506","create":"肖怜雪","createdt":"1974-10-31","type":"风沙侵蚀","winder":"白广路风场","remark":"谁把安逸当成幸福的花朵，那么等到结果时节，他只能望着空枝叹息。","status":"完成","phone":"18137772520"},
{"code":"941007954","create":"全曼云","createdt":"1994-10-07","type":"叶片断裂","winder":"万通风场","remark":"太阳虽有黑点，却在奋力燃烧中树立了光辉的形象。","status":"完成","phone":"13333850599"},
{"code":"780924267","create":"元镇国","createdt":"1978-09-24","type":"叶片裂纹","winder":"古城风场","remark":"努力就是光，成功就是影。没有光哪儿来影？","status":"评估","phone":"17729799989"},
{"code":"850421166","create":"贾灵泉","createdt":"1985-04-21","type":"风化脱漆","winder":"亚运村风场","remark":"岸边的奇花异草，是拘留不住奔腾向前的江水的。","status":"评估","phone":"17729799994"},
{"code":"931118801","create":"巩恒霖","createdt":"1993-11-18","type":"过热起火","winder":"小庄风场","remark":"没有斗狼的胆量，就不要牧羊。","status":"评估","phone":"18103710105"},
{"code":"861113313","create":"严少","createdt":"1986-11-13","type":"风沙侵蚀","winder":"左家庄风场","remark":"路灯经过一夜的努力，才无愧地领受第一缕晨光的抚慰。","status":"评估","phone":"18103719250"},
{"code":"840120521","create":"云宇峰","createdt":"1984-01-20","type":"叶片断裂","winder":"航天桥风场","remark":"不安于现状，不甘于平庸，就可能在勇于进取的奋斗中奏响人生壮美的乐间。","status":"评估","phone":"17719811988"},
{"code":"830317214","create":"匡贝","createdt":"1983-03-17","type":"叶片裂纹","winder":"军博风场","remark":"涓涓细流一旦停止了喧哗，浩浩大海也就终止了呼吸。","status":"评估","phone":"17752566606"},
{"code":"791020569","create":"康靖童","createdt":"1979-10-20","type":"风化脱漆","winder":"三里河风场","remark":"只要是辛勤的蜜蜂，在生活的广阔原野里，到处都可以找到蜜源。","status":"评估","phone":"17335577767"},
{"code":"811101412","create":"骆慕卉","createdt":"1981-11-01","type":"过热起火","winder":"黄庄风场","remark":"勤奋的含义是今天的热血，而不是明天的决心，后天的保证。","status":"评估","phone":"18137796677"},
{"code":"931117715","create":"俞伟","createdt":"1993-11-17","type":"风沙侵蚀","winder":"贵友风场","remark":"鞋底磨穿了，不等于路走到了头。","status":"评估","phone":"17788109926"},
{"code":"840313460","create":"余友易","createdt":"1984-03-13","type":"叶片断裂","winder":"洋桥风场","remark":"事业的大厦如缺乏毅力的支柱，只能是空中楼阁。","status":"评估","phone":"17703715062"},
{"code":"801218021","create":"吴靖","createdt":"1980-12-18","type":"叶片裂纹","winder":"国华风场","remark":"只有收获，才能检验耕耘的意义；只有贡献，方可衡量人生的价值。","status":"评估","phone":"18103832966"},
{"code":"780320778","create":"庾依玉","createdt":"1978-03-20","type":"风化脱漆","winder":"建国门风场","remark":"幻想者头脑里只有空中楼阁，实干家胸中才有摩天大厦。","status":"评估","phone":"18135777725"},
{"code":"940122017","create":"万坤","createdt":"1994-01-22","type":"过热起火","winder":"成府路风场","remark":"长蔓植物依附着支物向上爬，当它爬到比支撑它的支物不高时，它又窥伺着另一株支物。","status":"维修","phone":"17761666624"},
{"code":"830413808","create":"程新桐","createdt":"1983-04-13","type":"风沙侵蚀","winder":"新安风场","remark":"望洋兴叹的人，永远达不到成功的彼岸。","status":"维修","phone":"17703715554"},
{"code":"800202346","create":"敖玲沁","createdt":"1980-02-02","type":"叶片断裂","winder":"丰台桥南风场","remark":"沿着别人走出的道路前进时，应该踩着路边的荆棘，因为这样走多了，就能使道路增宽。","status":"维修","phone":"13333825099"},
{"code":"800406050","create":"能丰","createdt":"1980-04-06","type":"叶片裂纹","winder":"牡丹园风场","remark":"新路开始常是狭窄的，但它却是自己延伸拓宽的序曲。","status":"维修","phone":"13333828199"},
{"code":"891009244","create":"计翎妍","createdt":"1989-10-09","type":"风化脱漆","winder":"芳城园风场","remark":"闲适和宁静，对于浪花，意味着死亡。","status":"维修","phone":"18039111171"},
{"code":"790802041","create":"阎乐晨","createdt":"1979-08-02","type":"过热起火","winder":"甜水园风场","remark":"如果脆弱的心灵创伤太多，朋友，追求才是愈合你伤口最好的良药。","status":"维修","phone":"18003719110"},
{"code":"860516168","create":"吕采南","createdt":"1986-05-16","type":"风沙侵蚀","winder":"中粮广场风场","remark":"马行软地易失蹄，人贪安逸易失志。","status":"维修","phone":"18103710926"},
{"code":"910802190","create":"堵昕燕","createdt":"1991-08-02","type":"叶片断裂","winder":"新东安风场","remark":"松驰的琴弦，永远奏不出时代的强音。","status":"维修","phone":"18137666629"},
{"code":"790318263","create":"萧传军","createdt":"1979-03-18","type":"叶片裂纹","winder":"苏州桥风场","remark":"撒进奋斗的沃土，一滴汗珠就是一颗孕育希望的良种。","status":"维修","phone":"17788177588"},
{"code":"880130252","create":"邓娟","createdt":"1988-01-30","type":"风化脱漆","winder":"翠微路风场","remark":"根儿向纵深处延伸一寸，小树被狂风推倒的危险就减弱了一分。","status":"维修","phone":"17703810086"},
{"code":"940110546","create":"江智卓","createdt":"1994-01-10","type":"过热起火","winder":"交道口风场","remark":"在懒汉的眼里，汗是苦的，脏的，在勤者的心上，汗是甜的，在勤者的心上，汗是甜的，美的。","status":"维修","phone":"17335752222"},
{"code":"750123729","create":"柏肜瑛","createdt":"1975-01-23","type":"风沙侵蚀","winder":"团结湖风场","remark":"压力---在事业成功的道路上，你是无知者颓丧的前奏，更是有志者奋进的序曲。","status":"维修","phone":"18037336699"},
{"code":"940516963","create":"水成日","createdt":"1994-05-16","type":"叶片断裂","winder":"双榆树风场","remark":"在避风的港湾里，找不到昂扬的帆。","status":"完成","phone":"17788109930"},
{"code":"810101923","create":"周宏图","createdt":"1981-01-01","type":"叶片裂纹","winder":"怀柔风场","remark":"空谈家用空谈来装饰自己，实干家用实干去创造业绩。","status":"完成","phone":"17703716705"},
{"code":"790712876","create":"齐痴凝","createdt":"1979-07-12","type":"风化脱漆","winder":"昌平风场","remark":"英雄的事业必定包含着艰险，如果没有艰险也就不成为英雄了。","status":"完成","phone":"18037334789"},
{"code":"860423722","create":"郝紫瞳","createdt":"1986-04-23","type":"过热起火","winder":"潘家园风场","remark":"如果刀刃怕伤了自己而不与磨刀石接触，就永远不会锋利。","status":"完成","phone":"18037373746"},
{"code":"900215155","create":"云尘","createdt":"1990-02-15","type":"风沙侵蚀","winder":"复兴门风场","remark":"有建树的人，并非具备了比一般人更优越的条件，相反，他们要经过更多的磨练，走更艰辛的路。","status":"完成","phone":"13383855554"},
{"code":"880904620","create":"储艺璇","createdt":"1988-09-04","type":"叶片断裂","winder":"玉泉路风场","remark":"实干家在沙漠里也能开垦出绿洲，懒惰者在沃野上也不会获得丰收。","status":"完成","phone":"13082525268"},
{"code":"830402156","create":"荣海龙","createdt":"1983-04-02","type":"叶片裂纹","winder":"右安门外风场","remark":"不举步，越不守栅栏，不迈腿，登不上高山。","status":"完成","phone":"15220202026"},
{"code":"750321863","create":"卜伟成","createdt":"1975-03-21","type":"风化脱漆","winder":"和平街北口风场","remark":"消沉就角一支单调的画笔，只能给未来涂上一层灰色。","status":"完成","phone":"13001097739"},
{"code":"770809728","create":"满玲漪","createdt":"1977-08-09","type":"过热起火","winder":"清河风场","remark":"假如樵夫害怕荆棘，船只避忌风浪，铁匠畏惧火星，那么，世界就会变成另一副模样。","status":"完成","phone":"15640852345"},
{"code":"790409092","create":"马凌春","createdt":"1979-04-09","type":"风沙侵蚀","winder":"三元风场","remark":"收获是事业的雨量计；聚集着奋斗者洒落的每滴汗珠。","status":"完成","phone":"17746599939"},
{"code":"940820138","create":"傅微","createdt":"1994-08-20","type":"叶片断裂","winder":"新世界风场","remark":"无穷的伟大，也是从“一”开始的。","status":"完成","phone":"13686860858"},
{"code":"860114171","create":"凌钟吉","createdt":"1986-01-14","type":"叶片裂纹","winder":"十里画屏风场","remark":"花的生命虽然短暂，但它毕竟拥抱过春天。","status":"完成","phone":"18636751234"},
{"code":"920101135","create":"步孜娴","createdt":"1992-01-01","type":"风化脱漆","winder":"官厅水库风场","remark":"天才之舟，在汗水的河流里启程。","status":"评估","phone":"15208167567"},
{"code":"840826767","create":"侯星嘉","createdt":"1984-08-26","type":"过热起火","winder":"十度风场","remark":"在林荫路上散步不值得称赞，攀登险峰才有真正的乐趣。","status":"维修","phone":"15699999927"},
{"code":"910308989","create":"齐任安","createdt":"1991-03-08","type":"风沙侵蚀","winder":"康西草原风场","remark":"懒惰包含着永久的失望。","status":"完成","phone":"15699996944"},
{"code":"881025483","create":"柏鑫","createdt":"1988-10-25","type":"叶片断裂","winder":"八达岭风场","remark":"希望是美好的，她令人神往、追求、但是希望伴随着风浪。贪图安逸的人，他的希望不过是一带道路、一种幻境，只有敢于和狂风巨浪拚搏的人，希望才会开出鲜花，结出硕果。","status":"评估","phone":"18810000908"},
{"code":"750107938","create":"饶忆丹","createdt":"1975-01-07","type":"叶片裂纹","winder":"新王府井风场","remark":"小溪---在生命的长河里，你前进的步伐每时每刻都拨动着大海心中的琴弦。","status":"维修","phone":"13821825399"},
{"code":"801120073","create":"宿柯朱","createdt":"1980-11-20","type":"风化脱漆","winder":"东大桥风场","remark":"如果把成才比作登天，自学便是成才的天梯。","status":"完成","phone":"18088676767"},
{"code":"900905779","create":"孟广斌","createdt":"1990-09-05","type":"过热起火","winder":"华威风场","remark":"只有脚踏实地的人，大地才乐意留下他的脚印。","status":"评估","phone":"13821138505"},
{"code":"891021519","create":"安悦","createdt":"1989-10-21","type":"风沙侵蚀","winder":"京宝风场","remark":"钢钎与顽石的碰撞声，是一首力的歌曲。","status":"维修","phone":"18600000346"},
{"code":"770816566","create":"鲁白桃","createdt":"1977-08-16","type":"叶片断裂","winder":"劲松风场","remark":"贪图省力的船夫，目标永远下游。","status":"完成","phone":"15699999974"},
{"code":"800115945","create":"平勇","createdt":"1980-01-15","type":"叶片裂纹","winder":"海淀风场","remark":"浪花永不凋萎的秘诀：永远追求不安闲的生活。","status":"评估","phone":"15122391000"},
]
};

