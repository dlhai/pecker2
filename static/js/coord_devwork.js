var g_devwhs, g_focus_devwork;
function onclickfaultdevs(){
	if (g_devwhs == undefined)
		Reqdata("/rd?ls=devwh", "", function (res) {g_devwhs = res;});

	var dlg = new devdlg(g_focus.fault);
	dlg.Show();
}

//对话框组件
function devdlg(fault) {
    this.id = "devdlg" + Math.ceil(Math.random() * 1000000).toString();
	this.fault=fault;
}

devdlg.prototype.Show = function () {
    var html = '<div class="modal fade" id="' + this.id + '" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="false">'
        + '<div class="modal-dialog" style="width:900px">'
        + '<div class="modal-content">'
		+ `    <div class="xFCsrow" >	
				   <div class="modal-header" style="width:100px;">
					   <h4 class="modal-title" id="ModalDlgTitle">调用设备</h4>
				  </div>
				  <div class="xFIfixed radio_group" style="padding-top:30px;">
				      <div class="active">查看任务</div><div>查看位置</div>
				  </div>
				  <div class="modal-header" style="width:100px;" >
					   <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
				  </div>
              </div>
			  <div class="modal-body" style="padding:5px;height:450px;"></div>
			  <div class="modal-footer">
            </div>
        </div><!-- /.modal-content -->
        </div><!-- /.modal -->`;
    $("body").append(html);
    $('#' + this.id).on('hide.bs.modal', "", { This: this }, function (ev) {ev.data.This.closedlg(); });
    $('#' + this.id).modal('show');
    $('#' + this.id+" .radio_group").on("click", '', { This: this }, function (ev) {ev.data.This.onRadioGroup(ev);});
	g_focus_devwork=undefined;
	this.refresh();
}
devdlg.prototype.closedlg = function () {
    $('#' + this.id).remove();
}

devdlg.prototype.onRadioGroup = function (ev) {
	$(ev.target).addClass("active");
	$(ev.target).siblings().removeClass("active");
	if (ev.target.innerText=="查看任务"){
		this.refresh();
	}
	else{
		$('#' + this.id+" .modal-body").html(`<div id="bdmap" style="width:100%;height:100%;"></div>`);
		g_map=CreateMap("bdmap");

		// 显示风场
		Reqdata("/rd?ls=winder&id=" + g_focus.fault.winder_id, "", function (res) {
			res.data.forEach((x, i) => CreateMark("winder", x, res.ls, res.fields));
			if (res.data.length > 0 )
				g_map.centerAndZoom(CreatePoint(res.data[0].position), 14); 
		});

		// 显示设备
		Reqdata("/rd?ls=dev&id=("+this.devworks.data.map(x=>x.dev_id).join(",")+")", "", function (res) {
			res.data.forEach(x=>CreateMark2(x, res.ls, res.fields));
		});
	}
}

devdlg.prototype.onclickCard = function (ev) {
    $("#"+ this.id + " .fault_card ").removeClass("fault_card_focus");
    $(ev.delegateTarget).addClass("fault_card_focus");

	var id = $(ev.delegateTarget).attr("data_id");
	g_focus_devwork = GetSub(this.devworks.data, "id", id);
	this.refreshdetail();
}

devdlg.prototype.onclickButton = function (ev) {
	if ( ev.target.innerText == "新建" ){
		g_focus_devwork = Create( this.devworks.fields);
		g_focus_devwork.fault_id = g_focus.fault.id;
		g_focus_devwork.detail = new Object();
		g_focus_devwork.detail.fault = g_focus.fault;
		g_focus_devwork.guide_id = g_user.id;
		g_focus_devwork.detail.users = [g_user];
		g_focus_devwork.guidedt = (new Date()).format("yyyy-MM-dd hh:mm:ss.S")
		g_focus_devwork.winder_id = g_focus.fault.winder_id;
		g_focus_devwork.detail.winder={"id":g_focus.fault.winder_id, "name":g_focus.fault.winder_name, "addr":""};
	
		this.justifyfields();
		$('#' + this.id+" form").html(RenderFormIn(g_focus_devwork, this.devworks.fields, f2eDevwork));
		this.refreshbtnary();
	}
	else if ( ev.target.innerText == "删除" ){
		if ( !confirm("确定要删除？"))
			return;
		if ( g_focus_devwork.id == ""){
			g_focus_devwork = undefined;
			this.refresh();
		}
		else {
			Reqdata("/dev/devworkremove?id="+g_focus_devwork.id, this, function (res,ctx) {
				if (res.result==200){
					g_focus_devwork = undefined;
					ctx.refresh();
				}
			});
		}
	}
	else if ( ev.target.innerText == "保存" ){
		var fd = new FormData($('#' + this.id+" form")[0]);
		if ( g_focus_devwork.id == ""){
			postform("/dev/devworkcreate", fd, this, function (res,ctx) {
				if (res.result==200){
					g_focus_devwork.id=res.data.id;
					ctx.refresh();
				}
			});
		}
		else {
			postform("/dev/devworkmodify?id="+g_focus_devwork.id, fd, this, function (res,ctx) {
				if (res.result==200)
					ctx.refresh();
			});
		}
	}
	else {
		this.chgstatus(ev.target.innerText);
	}
}

devdlg.prototype.chgstatus = function(text){
	if (-1==!$.inArray(text, ["提交","撤回","接单","退回","确认到达","任务结束"])){
		alert("不认识的操作类型");
		return;
	}

    var fd = new FormData();
    fd.append("id", g_focus_devwork.id);
    fd.append("action", text);
    fd.append("status", g_focus_devwork.status);
	fd.append("maxid", g_focus_devwork.detail.flows[0].id);
    postform("/dev/devworkchgstatus", fd, this, function (res,ctx) {
        if (res.result == "200") {
			ctx.refresh();
            alert("操作成功！");
        }
    });
}

devdlg.prototype.refresh = function() {
	Reqdata("/dev/devworkquery?fault_id="+this.fault.id, this, function (res, ctx) {
		var tpl=`<div class="xFCsrow" style="height:100%;">
				<section class="xPanel2 xFIfixed" style="width: 240px;">
					<header>调用单列表<div style="float: right;"><a>新建</a></div></header>
					<div id="fault_cards" style="overflow-y: auto;">{0}</div>
				</section>
				<div style="padding:10px 15px;">
					<form class="x2Form" style="height:360px;"></form>
					<div class="btnarray" style="padding:20px 50px 0px 15px;"></div>
				</div>
			</div>`;
		ctx.devworks=res;
		res.fields.insertaftername( "winder_id", { title: "风场地址", name: "winder_addr", ftype:"div", twidth: "120" } );
		var ttt = tpl.format(res.data.map(dw=>rdcard_devwork(dw)).join(""));
		$('#' + ctx.id+" .modal-body").html(tpl.format(res.data.map(dw=>rdcard_devwork(dw)).join("")));
		$("#fault_cards .fault_card").on('click', "", { This: ctx }, function (ev) {ev.data.This.onclickCard(ev); });
		$("#"+ctx.id+" header a").on('click', "", { This: ctx }, function (ev) {ev.data.This.onclickButton(ev); });
		if ( g_focus_devwork != undefined ){
			ctx.refreshdetail();
			$("#"+ctx.id+" [data_id="+g_focus_devwork.id+"]").addClass("fault_card_focus");
		}
		else
			ctx.refreshbtnary();
	});
}

devdlg.prototype.refreshdetail = function () {
	Reqdata("/dev/devworkdetail?id="+g_focus_devwork.id, this, function (res, ctx) {
		g_focus_devwork = res.devwork;
		g_focus_devwork.detail = res;
		ctx.justifyfields();
		$('#' + ctx.id+" form").html(RenderFormIn(g_focus_devwork, ctx.devworks.fields, f2eDevwork));
		ctx.refreshbtnary();
	});
}

devdlg.prototype.refreshbtnary = function () {
	var btnary="";
	$("#"+this.id+" header a").hide();
	if ( g_focus_devwork==undefined)
		return;
	if (g_user.job == 11 || g_user.job == 12){// 调度长或调度
		if ( g_focus_devwork.status == 0 || g_focus_devwork.status == -1 ){
			btnary=`<button id="btndw_delete" type="button" class="btn btn-default" style="color:#aaaaaa">删除</button>
				<div style="float: right;">
					<button id="btndw_save" type="button" class="btn btn-primary">保存</button>
					<button id="btndw_submit" type="button" class="btn btn-primary">提交</button>
				</div>`;
		}
		else if ( g_focus_devwork.status == 1 ){
			btnary=`<button id="btndw_recall" type="button" class="btn btn-default" style="color:#aaaaaa">撤回</button>`;
		}
		$("#"+this.id+" header a").show();
	}
//	else if (g_user.job == 5 ){// 驻地长
//		btnary=`<div style="float: right;">
//				<button id="btndw_accept" type="button" class="btn btn-primary">接单</button>
//				<button id="btndw_decline" type="button" class="btn btn-primary">退回</button>
//			</div>`
//	}
	else if (g_user.job == 2 || g_user.job == 3 ){// 风场长和驻场
		if ( g_focus_devwork.status == 2 ){
			btnary=`<div style="float: right;">
					<button id="btndw_decline" type="button" class="btn btn-primary">确认到达</button>
				</div>`
		}
		else if ( g_focus_devwork.status == 3 ){
			btnary=`<div style="float: right;">
					<button id="btndw_decline" type="button" class="btn btn-primary">任务结束</button>
				</div>`
		}
	}

	$('#' + this.id+" .btnarray").html(btnary);
	$('#' + this.id+" .btnarray button").on('click', "", { This: this }, function (ev) {ev.data.This.onclickButton(ev); });
}

devdlg.prototype.justifyfields = function () {
	if (g_focus_devwork.status == -1){
		GetSub( this.devworks.fields, "name", "deal_id").ftype="div";
		GetSub( this.devworks.fields, "name", "dealdt").ftype="div";
		GetSub( this.devworks.fields, "name", "dev_id").ftype="none";
		GetSub( this.devworks.fields, "name", "driver_id").ftype="none";
	}
	else if (g_focus_devwork.status == 0 || g_focus_devwork.status == 1 ){
		GetSub( this.devworks.fields, "name", "deal_id").ftype="none";
		GetSub( this.devworks.fields, "name", "dealdt").ftype="none";
		GetSub( this.devworks.fields, "name", "dev_id").ftype="none";
		GetSub( this.devworks.fields, "name", "driver_id").ftype="none";
	}
	else {
		GetSub( this.devworks.fields, "name", "deal_id").ftype="div";
		GetSub( this.devworks.fields, "name", "dealdt").ftype="div";
		GetSub( this.devworks.fields, "name", "dev_id").ftype="div";
		GetSub( this.devworks.fields, "name", "driver_id").ftype="div";
	}

	// 调度长或调度可编辑
	if ( (g_user.job == 11 || g_user.job == 12) && (g_focus_devwork.status == -1 || g_focus_devwork.status == 0) ){
		GetSub( this.devworks.fields, "name", "clss").ftype="select";
		GetSub( this.devworks.fields, "name", "type").ftype="input";
		GetSub( this.devworks.fields, "name", "devwh_id").ftype="select";
		GetSub( this.devworks.fields, "name", "timelen").ftype="input";
		GetSub( this.devworks.fields, "name", "remark").ftype="input_long";
	}
	else{ // 所有字段仅只读
		GetSub( this.devworks.fields, "name", "clss").ftype="div";
		GetSub( this.devworks.fields, "name", "type").ftype="div";
		GetSub( this.devworks.fields, "name", "devwh_id").ftype="div";
		GetSub( this.devworks.fields, "name", "timelen").ftype="div";
		GetSub( this.devworks.fields, "name", "remark").ftype="div_long";
	}

	if (g_user.job == 5 && g_focus_devwork == 1 ){// 驻地长
		GetSub( this.devworks.fields, "name", "dev_id").ftype="select";
		GetSub( this.devworks.fields, "name", "driver_id").ftype="select";
	}
}

function f2eDevwork(u,fd) {
	function rd_status(status, items, users ) {
		`<div class="xCombox">
			<span>{text}</span>
			<div class="xPopWnd xdoclist">{items}</div>
		</div>`

		// 只需要内部的东西
		return `<span>{text}</span><div class="xPopWnd xdoclist">{items}</div>`.format({
			"text":GetSub(status, "id",u[f]).name, 
			"items":items.map(x=>"<div>"+x.id+" "+ x.date.substr(5,11)+ " " 
				+ GetSub(users, "id", x.user_id ).name + " "+ x.remark + "</div>" ).join("")
		});
	}

	var f = (typeof fd == "string"?fd:fd.name);
	if ( f == "status"){ 
		if ( u[f]=="") return "新建";
		return rd_status(status_devwork, g_focus_devwork.detail.flows, g_focus_devwork.detail.users );
	}
	else if ( f=="guide_id") return u[f]==""?"":GetSub(g_focus_devwork.detail.users, "id", u[f]).name;
	else if ( f=="guidedt") return u[f]==""?"":u[f].substr(5,11);
	else if ( f=="fault_id") return u[f]==""?"":g_focus_devwork.detail.fault.code;
	else if ( f=="timelen")	return u[f]==""?"":u[f]+"天";
	else if ( f=="winder_id")	return u[f]==""?"":g_focus_devwork.detail.winder.name;
	else if ( f=="winder_addr")	return u["winder_id"]==""?"":g_focus_devwork.detail.winder.addr;
	else if ( f=="deal_id")	return u[f]==""?"":GetSub(g_focus_devwork.detail.users, "id", u[f]).name;
	else if ( f=="dealdt")	return u[f]==""?"":u[f].substr(5,11);
	else if ( f=="clss"){
		if ( fd.ftype=="select")
			return RenderSelect(db_devclss, u[f]);
		else
			return u[f]==""?"":GetSub(db_devclss, "id", u[f]).name;
	}
	else if ( f == "devwh_id"){
		if ( fd.ftype=="select")
			return RenderSelect(g_devwhs.data, u[f]);
		else
			return u[f]==""?"":GetSub(g_devwhs.data, "id", u[f]).name;
	}
	else if ( f=="dev_id"){
//		if ( fd.ftype=="select")
//			return RenderSelect(this.devs, u[f]);
//		else
			return u[f]==""?"":g_focus_devwork.detail.dev.code;
	}
	else if ( f=="driver_id"){
//		if ( fd.ftype=="select")
//			return RenderSelect(this.drivers, u[f]);
//		else
		return u[f]==""?"":GetSub(g_focus_devwork.detail.users, "id", u[f]).name;
	}

	return u[f];
}

function rdcard_devwork(dw){
	var tpl1 = `<div class="fault_card" data_id="{id}">
			<div class="header">
				<div class="type">调用单</div>
				<div class="title">{clss}</div>
			</div>
			<div class="body" style="text-align:left;">
				<div><strong>型号：</strong>{type}</div>
				<div><strong>所属驻地：</strong>{devwh_id}</div>
			</div>
		</div>`;

	var tpl2 = `<div class="fault_card" data_id="{id}">
			<div class="header">
				<div class="type">调用单</div>
				<div class="title">{clss}</div>
			</div>
			<div class="body" style="text-align:left;">
				<div><strong>型号：</strong>{type}</div>
				<div><strong>所属驻地：</strong>{devwh_id}</div>
				<div><strong>调用设备：</strong>{dev_id}</div>
				<div><strong>司机：</strong>{driver_id}</div>
			</div>
		</div>`;
	
	function toshow(obj){
		var r=new Object();
		for ( var x in obj){
			if (x == "clss") r[x] = GetSub(db_devclss, "id", obj[x]).name;
			else if (x == "devwh_id") r[x] = obj[x]=="" ? "":GetSub(g_devwhs.data, "id", obj[x]).name;
			else if (x == "dev_id") r[x] = obj["dev_code"];
			else if (x == "driver_id") r[x] = obj["driver_name"];
			else r[x]=obj[x];
		}
		return r;
	}
	return dw.status >= 2 ? tpl2.format(toshow(dw)):tpl1.format(toshow(dw));
}
