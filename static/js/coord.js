// 案件界面，用于调度、专家、风场场主、驻场、队长等，当前仅含案件编辑功能的内容，后面会加入案件显示的内容。

var fault_matstatus = {"": "未指派","0": "未提交" ,"1": "已提交" ,"2": "正在备货" ,"3": "等待审批" ,
			"4": "等待发货" ,"5": "等待收货" ,"6": "风场已收" ,"-1": "退回" }

//------------------------人员选择对话框------------------------------------------
function crd_showuserselectdlg() {
    var us = `<div id="rolelist" class="xCombox xRndAngle" style="margin-top:5px; display:inline-block;"><span>调度人员</span><div class="xMenu">
                <div class="selected">调度人员</div><div>风场人员</div><div>设备人员</div><div>仓库人员</div><div>专家</div><div>维修人员</div>
            </div></div>
            <div id="userfilter" class="xCombox xRndAngle" style="margin-top:5px; display:inline-block;">
                <span>所有</span><div id="userfiltertree" class="xMenu" style="max-height:600px;overflow-y:auto;"><div class="selected">调度人员</div></div>
            </div>
            <div id="filteruserlist" class="xRndAngle xScroll" style="margin-top:5px; width:590px;height:250px;padding:5px;"></div>`

    var dlg = new cbDlg("人员选择", "width:610px");
    dlg.Add(us);
    dlg.Show();
}

var ud_sels=[] // 当前已选中的人员列表(含专家组、风场人员等外部)
var ud_chats=[] // 当前已选中的人员列表（仅聊天部分）
var ud_filter2 = "";
function ud_userdlg( filter1, filter2, sels, cb) {
	ud_sels = sels;
	ud_filter2 = filter2;
    var us = 
			`<div id="rolelist" class="xCombox xRndAngle" style="margin-top:5px; display:inline-block;">
				<span></span>
				<div class="xMenu"></div>
			</div>
            <div id="userfilter" class="xCombox xRndAngle" style="margin-top:5px; display:inline-block;">
                <span></span>
				<div id="userfiltertree" class="xMenu" style="max-height:600px;overflow-y:auto;">
				</div>
            </div>
            <div id="filteruserlist" class="xRndAngle xScroll" style="margin-top:5px; width:590px;height:250px;padding:5px;"></div>`
    var dlg = new cbDlg("人员选择", "width:610px");
    dlg.Add(us);
    dlg.Show();
	dlg.submit = function(thedlg){
		var ar = $("#filteruserlist input").toArray().filter(x=>$(x).prop('checked')).map(x=>$(x).attr("data_id"));
		if ( cb(ar) ){
			thedlg.closedlg();
		}
	}

	var roles = filter1 != "" ? filter1: ["调度人员","风场人员","设备人员","仓库人员","专家","维修队"];
	ud_cbx("rolelist",roles, roles[0] );
	onclkrole(roles[0],filter2);
}

function ud_cbx(id, items, dft ) {
	$("#"+id+" span").html(dft);
	if (typeof items[0] == "string")
		$("#"+id+" div").html(items.map(x=>"<div>"+x+"</div>").join(""));
	else
		$("#"+id+" div").html(items.map(x=>`<div data_id="{id}" >{name}</div>`.format(x)).join(""));
}

//点在菜单项上
$("html").on("click", function (event) {
    var node = $(event.target);
    if (node.parent().hasClass("xMenu")) { //点在菜单背景上
        var parentid = node.parent().parent().attr("id");
        if (parentid == "rolelist") {
           onclkrole($(node).html(),ud_filter2);
        }
        else if (parentid == "userfilter") {
			var filter2 = node.attr("data_id");
			if ( filter2 == undefined )
				filter2 = node.html();
			onclkfilter(filter2);
        }
    }
});

function rd_checkuser(user) {
    var tpl = `<label style="margin-right:10px;font-weight:normal;"><input data_id="{0}" type="checkbox" {2} >{1}</label>`;
    return tpl.format(user.id,rd_brief(user), ud_sels.some(x=>x.id==user.id)? "checked":"");
}

function onclkrole(text, filter2){
	if (text == "当前") {
		var ar = ["所有"];
		ud_cbx("userfilter",ar, ar[0] );
		$("#filteruserlist").html(ud_chats.map(x => rd_checkuser(x)));
    }
	else if (text == "调度人员") {
        $("#userfilter span").html('所有　　');
        $("#userfiltertree").addClass('xMenu');
        $("#userfiltertree").removeClass('xPopWnd');
        $("#userfiltertree").html('<div class="selected">所有　　</div>');
        Reqdata("/user/briefs?job=" + GetsubJob(GetSub(db_job, "name", "调度超级帐号").id, "string"), "", function (res) {
			res.users.forEach(x=>x.prof=GetSub(db_job, "id", x.job).sname);
            $("#filteruserlist").html(res.users.map(x => rd_checkuser(x)));
        });
    }
    else if (text == "风场人员") {
        $("#userfilter span").html('　　　　　　');
        $("#userfiltertree").html('');
        $("#userfiltertree").addClass('xPopWnd');
        $("#userfiltertree").removeClass('xMenu');
        $("#filteruserlist").html("");
        g.userfiltertree = new x4Tree("#userfiltertree", "winderco", "", "winder", function (type, id, node) {
            if (type == "winder") {
                $("#userfilter>span").html(node.html());
                $("#userfilter .xPopWnd").toggle();
                Reqdata("/user/briefs?depart_id=" + id + "&depart_table=" + GetTbl("winder").id, "", function (res) {
					res.users.forEach(x=>x.prof=GetSub(db_job, "id", x.job).sname);
                    $("#filteruserlist").html(res.users.map(x => rd_checkuser(x)));
                });
            }
            else {
                g.userfiltertree.Extend("#" + type + "_" + id);
            }
        });
    }
    else if (text == "设备人员") {
        $("#userfilter span").html('　　　　　　');
        $("#userfiltertree").addClass('xPopWnd');
        $("#userfiltertree").removeClass('xMenu');
        $("#userfiltertree").html('');
        $("#filteruserlist").html('');
        g.userfiltertree = new x4Tree("#userfiltertree", "devwh", "", "devwh", function (type, id, node) {
            if (type == "devwh") {
                $("#userfilter>span").html(node.html());
                $("#userfilter .xPopWnd").toggle();
                Reqdata("/user/briefs?depart_id=" + id + "&depart_table=" + GetTbl("devwh").id, "", function (res) {
					res.users.forEach(x=>x.prof=GetSub(db_job, "id", x.job).sname);
                    $("#filteruserlist").html(res.users.map(x => rd_checkuser(x)));
                });
            }
            else {
                g.userfiltertree.Extend("#" + type + "_" + id);
            }
        });
    }
    else if (text == "仓库人员") {
        $("#userfilter span").html('　　　　　　');
        $("#userfiltertree").addClass('xPopWnd');
        $("#userfiltertree").removeClass('xMenu');
        $("#userfiltertree").html('');
        $("#filteruserlist").html('');
        g.userfiltertree = new x4Tree("#userfiltertree", "matprov", "", "matwh", function (type, id, node) {
            if (type == "matwh") {
                $("#userfilter>span").html(node.html());
                $("#userfilter .xPopWnd").toggle();
                Reqdata("/user/briefs?depart_id=" + id + "&depart_table=" + GetTbl("matwh").id, "", function (res) {
					res.users.forEach(x=>x.prof=GetSub(db_job, "id", x.job).sname);
                    $("#filteruserlist").html(res.users.map(x => rd_checkuser(x)));
                });
            }
            else {
                g.userfiltertree.Extend("#" + type + "_" + id);
            }
        });
    }
    else if (text == "专家") {
        $("#userfilter span").html('所有　　　　');
        $("#userfiltertree").addClass('xMenu');
        $("#userfiltertree").removeClass('xPopWnd');
        $("#userfiltertree").html('<div id="user_0">所有</div>' + xrmenuin(db_skill, "skill_"));
        Reqdata("/user/briefs?job=14", "", function (res) {
			res.users.forEach(x=>x.prof=GetSub(db_job, "id", x.job).sname);
            $("#filteruserlist").html(res.users.map(x => rd_checkuser(x)));
        });
    }
    else if (text == "维修队") {
        $("#userfiltertree").addClass('xMenu');
        $("#userfiltertree").removeClass('xPopWnd');
        Reqdata("/user/briefs?job=16", "", function (res) {
			if (filter2 != "")
				res.users = res.users.filter(x=>x.id==filter2);
			if (res.users.length == 1){
				ud_cbx("userfilter",res.users, res.users[0].name );
				onclkfilter(res.users[0].id);
			}
			else{
				ud_cbx("userfilter",res.users, "　　　　" );
				$("#filteruserlist").html("");
				}
        });
    }
    else if (text == "维修人员") {
        $("#userfiltertree").addClass('xMenu');
        $("#userfiltertree").removeClass('xPopWnd');

		var ar = filter2 != "" ? [filter2]: ["所有","队长","技工"];
		ud_cbx("userfilter",ar, ar[0] );
		onclkfilter(ar[0]);
    }
}

	function onclkfilter(filter2){
        var role = $("#rolelist span").html();
        if (role == "专家") {
            Reqdata("/user/briefs?job=14", "", function (res) {
				if (filter2 != "所有")
					res.users = res.users.filter(x=>x.skill.indexOf(filter2)!= -1);
				res.users.forEach(x=>x.prof=GetSub(db_job, "id", x.job).sname);
                $("#filteruserlist").html(res.users.map(x => rd_checkuser(x)));
            });
        }
        else if (role == "维修队") {
            Reqdata("/rdteam?user_id=" + filter2, "", function (res) {
				res.data.forEach(x=>x.prof=GetSub(db_job, "id", x.job).sname);
                $("#filteruserlist").html(res.data.map(x => rd_checkuser(x)));
            });
        }
        else if (role == "维修人员") {
			var job = filter2=="队长"?16:filter2=="技工"?17:"(16,17)";
            Reqdata("/user/briefs?job=" + job, "", function (res) {
				res.users.forEach(x=>x.prof=GetSub(db_job, "id", x.job).sname);
                $("#filteruserlist").html(res.users.map(x => rd_checkuser(x)));
            });
        }
	}


//----------------------案件显示基本函数---------------------------------------------------------------
function crd_faultcard(obj) {
    var tpl = `<div class="fault_card" data_id="{id}">
            <div class="header">
                <div class="type">报修单</div>
                <div class="title">{type}</div>
            </div>
            <div class="body" style="text-align:left;">
                <div><strong>单号：</strong>{code}</div>
                <div><strong>报修人：</strong>{report_name}</div>
                <div><strong>联系电话：</strong>{phone}</div>
                <div><strong>单位：</strong>{winder_name}</div>
            </div>
        </div>`
    return tpl.format(obj);
}

function crd_render_fault(fault, fields) {
	var r =`<details open class="xDetail2"><summary style="border-top:0px;">报修</summary><div>`
    r += '<div class="x2Form narrow">' + RenderPane2(fault, fields, f2s) +'</div>';
	if ( fault.imgs.length == 0 )
		fault.imgs =[{"name":"img/blank.png"}];
    r+= `<div class="xHImgList" style="margin:10px;">`+fault.imgs.map(x=>`<img src="`+x.name+`"/>`).join("")+`</div>`;
	r+=`</div></details>`;
    return r;
}

function rd_frozenleft(title, cnt) {
    var r = `<div class="frozenleft"><label>`+title+`</label>`+cnt+"</div>";
    return r;
}

function rd_buttonright(id, cnt) {
    var r = `<div id="`+id+`"class="buttonright"><div>` + cnt +`</div><div id="btn_`+id+`" >编辑</div></div>`;
    return r;
}

// 文档组合框
function rd_doc(id, docs ) {
	var type={"eval1":"评估报告","eval2":"二次评估"};
	var namedocs = docs.map(x=>`<div><a href="{src}">{type}_{name}_{date}</a></div>`.format({
		"src":x.name,"type":type[id],"date":x.date.substr(5,11),
		"name":GetSub(g_focus.chatmen, "id", x.user_id).name }));

    var r = `<div id="{id}" class="buttonright" style="width:100px;">
				<div class="xCombox">
					<span>{cursel}</span>
					<div class="xPopWnd xdoclist">{itemlist}</div>
				</div>
				<div id="btn_{id}"><label>上传<input type="file"/></label></div>
			</div>`.format({id:id,cursel:( namedocs.length > 0 ? namedocs[0] :"　"), itemlist:namedocs.join("")});
    return r;
}

// 带签字的文档组合框
function rd_doc2(id, docs, signs, signers) {
	var type={"plan":"维修方案","report":"维修报告"};
	var img = {"2":"img/风场.png","3":"img/驻场.png","11":"img/调度长.png","16":"img/队长.png"};

	var signdocs = docs.map(x=>`<div><a href="{src}">{type}_{name}_{date} {signs}</a></div>`.format({
		"src":x.name,"type":type[id],"date":x.date.substr(5,11),"name":GetSub(g_focus.chatmen, "id", x.user_id).name,
		"signs":signs.filter(y=>y.a_id==x.id).map(y=>`<span class="sign"><img src="`+img[y.remark]+`">`+GetSub( signers, "id", y.b_id).name+`</span>`).join(" ")
		}));

    var html_docs = 
		`<div id="{id}" class="buttonright" style="width:100px;">
			<div class="xCombox">
				<span>{cursel}</span>
				<div class="xPopWnd xdoclist">{itemlist}</div>
			</div>
			<div id="btn_{id}"><label>上传<input type="file"/></label></div>
		</div>`.format({id:id,cursel:( signdocs.length > 0 ? signdocs[0] :"　"), itemlist:signdocs.join("")});

	var html_sign = `<div id=`+id+`_sign" class="buttonright" style="width:100px;"><div>`
				+ ( signs.length == 0 ? "　":signs.map(y=>{
					var u = GetSub( signers, "id", y.b_id);
					return `<span class="sign"><img src="`+img[y.remark]+`">`+u.name+`</span>` // y.remark是签字时的职业
				}).join(" "))+`</div><div id="btn_`+id+`sign" style="width:70px;">我要签字</div></div>`; // 签字
    return html_docs + html_sign;
}

function rd_brief(user) {
	var tpl = `<div class="brief"><img src="{face}"/>【{prof}】{name}</div>`;
    return tpl.format(user);
}

function rd_statusright(html,status) {
	return `<div class="statusright"><div>`+html+`</div><div>`+status+`</div></div>`;
}

// 维修用料
function rd_matrec( matoutrec ) {
	var mat = GetSub(g_mats.data, "id", matoutrec.mat_id);
	return rd_statusright(mat.name+"("+mat.type+")", fault_matstatus[matoutrec.status]);
}

// 维修设备
function rd_device( devwork ) {
	var clss = GetSub(db_devclss, "id", devwork.clss).name;
	return rd_statusright(clss+"("+devwork.type+")", GetSub(status_devwork,"id",devwork.status).name);
}

// 维修记录
function rd_repairlog( logs,imgs,users ) {
	logs.forEach((x,i)=>{
		x.imgs = imgs.filter(y=>y.ref_id==x.id);
		x.user = users.filter(y=>y.id==x.user_id)[0];
	});

	var tpl = doT.template(`<table class="xTable">
	<thead><tr><th>现场图片</th><th>说明</th><th>发表人</th></tr></thead>
	{% it.forEach((x,i)=>{ %}
	<tr>
		<td>
			<div class="xHImgList" style="border:0px;">
			{% x.imgs.forEach((y,i)=>{ %}
			<img src="{%=y.name%}"/>
			{% }); %}
			</div>
		</td>
		<td  style="max-width: 250px;">{%=x.remark%}</td>
		<td>
			<div><span class="SmallHead"><img src="{%=x.user.face%}"/>【{%=x.user.prof%}】{%=x.user.name%}</span></div>
			<div>{%=x.date.substr(5,11)%}</div>
		</td>
	</tr>
	{% }); %}
	</table>`);
	return tpl(logs);
}

function rd_speech(speech) {
    if (speech.user_id != g_user.id) {
        var user=GetSub(g_focus.chatmen,"id",speech.user_id);

		tpl=`<div class="lspeech">
				<div><img src="{face}" /></div>
				<div>
					<span>【{prof}】{name}</span>
					{date}
					<div>{say}</div>
				</div>
			</div>`
        r = tpl.format(mix(speech,user))
    }
    else {
        r =`<div class="rspeech">
				<div>
					{date}
					<span>【{prof}】{name}</span>
					<div>{say}</div>
				</div>
				<div><img src="{face}" /></div>
        </div>`.format(mix(speech,g_user))
    }
    return r;
}