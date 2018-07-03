$("html").on("change", function (event) {
    var node = event.target;
    if (node.tagName == "INPUT" && node.type == "file") { // 可点击换图的图片列表
        if ($(node).parent().parent().hasClass("imagelistlive") && $(node).parent().nextAll().length == 0) {
			var file = node.files[0];
			var reader = new FileReader();
			reader.onload = function (e) { $(node).prev().attr("src", e.target.result); };
			reader.readAsDataURL(file);
			imgls = $(node).parent().parent();
			var id=imgls.attr("data_id");
			if ( id == undefined )
				imgls.append(xrimagelive2("")); // 列表情况下，保证尾部有空白图
			else{
				var name = id+"_"+imgls.children().length
				imgls.append(xrimagelive2("", "", name)); // 列表情况下，保证尾部有空白图
			}
        }
    }
});

// 直接为数组用这一版
function RenderSelect(ar, selid, type) {
    var r = "";
    if (selid == "" )
        r += '<option selected></option>';
    else
        r += '<option></option>';

    ar.forEach(x=>{
        if (typeof (type) != "undefined" && x.type != type)
            return;

        if (x["id"] == selid || x["name"] == selid )
            r += '<option value="' + x["id"] + '" selected>' + x["name"] + '</option>';
        else
            r += '<option value="' + x["id"] + '">' + x["name"] + '</option>';
    });
    return r;
}

// 使用data采用这一版
function RenderSelect2(res, selid) {
    var r = "";
    if (selid=="")
        r += '<option selected></option>';
    else
        r += '<option></option>';
    res.data.forEach((x,i)=>{
        if (x["id"] == selid || x["name"] == selid)
            r += '<option value="' + x["id"] + '" selected>' + x["name"] + '</option>';
        else
            r += '<option value="' + x["id"] + '">' + x["name"] + '</option>';
    });
    return r;
}

function RenderSelectSkill(val) {
    if (val == "") val = "　";
    var cnt = db_skill.map(x => { return val.indexOf(x.name) == -1 ? ("<div>" + x.name + "</div>") : ('<div class="selected">' + x.name + "</div>") });
    return `<div class="xCombox"><span>` + val + `</span><div class="xMenu">` + cnt.join("") + `</div></div>`;
}

function xrimagelist(img) {
    var tpl = `<label for="{id}"><img style="width: 100%; height: 100%;" {img} />
                        <input type="file" id="{id}" accept="image/*"></label>`;
    return tpl.format({ id: "img_"+rndstr(8), img: (img == "" ? "" : 'src="' + img + '"') });
}

//背景带十字，点击可换图（换图处理在开头的$("html").on("change", function (event)）
function xrimagelive(img) {
    var image = img == "" ? "" : 'src="' + img + '"';
    var clss = arguments[1] ? 'class="' + arguments[1] + '"' : "";
    var width = arguments[2] ? arguments[2] : "100%";
    var heigh = arguments[3] ? arguments[3] : "100%";
    var tpl = `<label {clss} for="{id}"><img style="width: {width}; height: {heigh};" {image} />
                        <input type="file" id="{id}" name="{id}" accept="image/*"></label>`;
    return tpl.format({ id: "img_"+rndstr(8), clss: clss, image: image, width: width, heigh: heigh });
}
//背景带十字，点击可换图的列表（换图处理在开头的$("html").on("change", function (event)）
function xrimagelistlive(imglist) {
	if (imglist[imglist.length-1]!="")
		imglist.push("");
    return `<div class="imagelistlive">` + imglist.map(x => xrimagelive(x)) + `</div>`;
}

//背景带十字，点击可换图(第2版，参数多)（换图处理在开头的$("html").on("change", function (event)）
function xrimagelive2(img, id, name, clss, style) {
    var image = img == "" ? "" : 'src="' + img + '"';
    id = id ? id : "img_"+rndstr(8);
    name = 'name="' + (name ? name :id)+'"';
    clss = clss ? clss : "";
    style = style ? 'style="' + style + '"': "";
    var tpl = `<label class="imagelive {clss}" {style} for="{id}"><img style="width:100%;height:100%;" {image} />
                        <input type="file" id="{id}" {name} accept="image/*"></label>`;
    return tpl.format({ id:id, name:name, clss: clss, image: image, style: style });
}
//背景带十字，点击可换图的列表(第2版，参数多)（换图处理在开头的$("html").on("change", function (event)）
function xrimagelistlive2(id, imglist) {
	if (imglist[imglist.length-1]!="") // 空白图是最后的十字架
		imglist.push("");
    return `<div data_id="`+id+`" class="imagelistlive">` + imglist.map((x,i) => xrimagelive2(x,"",id+"_"+i)).join("") + `</div>`;
}

//菜单项
function xrmenuin(ar, pre) {
    var tpl = `<div id="` + pre + `{id}">{name}</div>`;
    return ar.map(x => tpl.format(x)).join("");
}

// 字段数组专用的排序函数，数组自带的为毛不好用
function xfieldsort(ar) {
    ar.forEach((x, i) => {
        if (!x.hasOwnProperty("forder"))
            x.forder = "";
        if (x.forder == "") {
            if (i == 0) x.forder = "0";
            else x.forder = ar[i - 1].forder;
        }
    });
    for (var i = 0; i < ar.length; i++) {
        for (var j = i + 1; j < ar.length; j++) {
            if (int(ar[i].forder) > int(ar[j].forder)) {
                var t = ar[i];
                ar[i] = ar[j];
                ar[j] = t;
            }
        }
    }
}

// div组件 可定制类名和style
function cbCube(cls, css) {
    this.cls = cls;
    this.css = attr;
    this.subs = new Array();
}
cbCube.prototype.Add = function (sub) {
    this.subs.push(sub);
} 
cbCube.prototype.toString = function () {
    var ret = "<div";
    if (this.cls) ret += ' class="' + cls + '"';
    if (this.css) ret += ' style="' + css + '"';
    ret += '>';
    for (var i in this.sub) r += this.sub[i].toString();
    ret += '</div>';
    return ret;
} 

//对话框组件
function cbDlg(title, css, subs) {
    this.id = "cbdlg" + Math.ceil(Math.random() * 1000000).toString();
    this.css = css? css:"width:450px";
    this.title = title ? title:"标题";
    this.subs = new Array();
    if (subs)
        this.subs.push(subs);
    this.btndel = false;
}
cbDlg.prototype.Add = function (sub) {
    this.subs.push(sub);
}
cbDlg.prototype.Show = function () {
    var html = '<div class="modal fade" id="' + this.id + '" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="false">'
        + '<div class="modal-dialog" style="' + this.css + '">'
        + '<div class="modal-content">'
        + '    <div class="modal-header">'
        + '        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'
        + '        <h4 class="modal-title" id="ModalDlgTitle">' + this.title + '</h4>'
        + '   </div>'
        + '    <div id="ModalDlgContent" class="modal-body" style="padding:5px">';
    this.subs.forEach(x => { html += x.toString() });
    html += '    </div>'
        + ` <div class="modal-footer">
                <div style="float:left;">`+
                    (this.btndel ? `<button type="button" class="btn btn-default" style="color:#aaaaaa">删除</button>` : "") +
                    `<div id="msg" style="display:inline-block;"></div>
                </div>
                <button type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
        </div><!-- /.modal -->`;
    $("body").append(html);
    $('#' + this.id).find("button").on("click", '', { This: this }, function (ev) {
        if (ev.target.innerText == "提交") ev.data.This.submit(ev.data.This);
        else if (ev.target.innerText == "关闭") ev.data.This.closedlg(ev.data.This);
        else if (ev.target.innerText == "删除") ev.data.This.remove(ev.data.This);
    });

    $('#' + this.id).on('hide.bs.modal', "", { This: this }, function (ev) {ev.data.This.closedlg(); });
    $('#' + this.id).modal('show');
}
cbDlg.prototype.closedlg = function () {
    $('#' + this.id).remove();
}

//form对话框组件
function cbFormDlg(title, css, subs) {
    this.id = "cbFormDlg" + Math.ceil(Math.random() * 1000000).toString();
    this.css = css? css:"width:450px";
    this.title = title ? title:"标题";
    this.subs = new Array();
    if (subs)
        this.subs.push(subs);
}
cbFormDlg.prototype.Add = function (sub) {
    this.subs.push(sub);
}
cbFormDlg.prototype.Show = function (cls) {
    var html = '<div class="modal fade" id="' + this.id + '" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="false">'
        + '<div class="modal-dialog" style="' + this.css + '">'
        + '<div class="modal-content">'
        + '    <div class="modal-header">'
        + '        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>'
        + '        <h4 class="modal-title" id="ModalDlgTitle">' + this.title + '</h4>'
        + '   </div>'
        + '   <form id="ModalDlgContent" class="modal-body '+cls+'" style="padding:5px">';
    this.subs.forEach(x => { html += x.toString() });
    html += '    </form>'
        + ` <div class="modal-footer">
                <div style="float:left;">`+
                    (this.urlremove ? `<button type="button" class="btn btn-default" style="color:#aaaaaa">删除</button>` : "") +
                    `<div id="msg" style="display:inline-block;"></div>
                </div>
                <button type="button" class="btn btn-primary">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
            </div>
        </div><!-- /.modal-content -->
        </div><!-- /.modal -->`;
    $("body").append(html);
    $('#' + this.id).find("button").on("click", '', { This: this }, function (ev) {
        if (ev.target.innerText == "提交") ev.data.This.submit();
        else if (ev.target.innerText == "关闭") ev.data.This.closedlg();
        else if (ev.target.innerText == "删除") ev.data.This.remove();
    });

    $('#' + this.id).on('hide.bs.modal', "", { This: this }, function (ev) {ev.data.This.closedlg(); });
    $('#' + this.id).modal('show');
}
cbFormDlg.prototype.closedlg = function (reason) {
	if ( this.closing )
		this.closing(reason);
    $('#' + this.id).remove();
}
cbFormDlg.prototype.submit = function () {
    var fd = new FormData(document.getElementById("ModalDlgContent"));
	if ( this.check && !this.check(fd) )
		return;
	postform( this.urlsubmit, fd, this, function(res, ctx){
		ctx.res=res;
		if (res.result == 200){
			alert("提交成功！");
			ctx.closedlg("submit");
		}
	});
}
cbFormDlg.prototype.remove = function () {
	Reqdata( this.urlremove, this, function(res,ctx){
		ctx.res=res;
		if (res.result == 200) { 
			alert("删除成功！");
			ctx.closedlg("remove");
		}
	});
}

function RenderPane(ar, idx, fun) {
    var r = "";
    ar.fields.sort(function (a, b) { return parseInt(a.forder) - parseInt(b.forder); });
    for (var i = 0; i < ar.fields.length; i++) {
        var field = ar.fields[i];
        if (field.name == "id")
            continue;
        var val = ar.data[idx][field.name];
        var attr = "";
        if (field.name.indexOf("_") != -1)
            attr = 'id="' + field.name + "_" + val + '" ';

        if (field.ftype == "input_long" || field.ftype == "div_long")
            attr += 'style="width:490px;"';
        else if (field.ftype == "textarea")
            attr += 'style="overflow-y: scroll;width:490px;max-height:45px;"';

        r += "<div><label>" + field.title + "</label><div " + attr + ">" + (fun ? fun(ar.data[idx], field) : val) + "</div></div>";
    }
    return r;
}

function RenderPane2(entity, fields, fun) {
    var r = "";
    for (var i = 0; i < fields.length; i++) {
        var field = fields[i];
        if (field.forder == -1 || field.ftype == "none")
            continue;
        var attr = "";
        if (field.ftype == "input_long" || field.ftype == "div_long")
            attr += 'style="width:490px;"';
        else if (field.ftype == "textarea")
            attr += 'style="overflow-y: scroll;width:490px;max-height:45px;"';
        r += "<div><label>" + field.title + "</label><div " + attr + ">" +
            (fun != undefined ? fun(entity, field) : entity[field.name]) + "</div></div>";
    }
    return r;
}

// 与第二版区别是增加了x2Form的包装div
function RenderPane3(entity, fields, fun) {
    var r = '<div class="x2Form">';
    for (var i = 0; i < fields.length; i++) {
        var field = fields[i];
        if (field.forder == -1 || field.ftype == "none")
            continue;
        var attr = "";
        if (field.ftype == "input_long"|| field.ftype == "div_long")
            attr += 'style="width:490px;"';
        else if (field.ftype == "textarea")
            attr += 'style="overflow-y: scroll;width:490px;max-height:45px;"';
        r += "<div><label>" + field.title + "</label><div " + attr + ">" +
            (fun != undefined ? fun(entity, field) : entity[field.name]) + "</div></div>";
    }
    r += "</div>"
    return r;
}


// 渲染表单,三步
//1.仅渲染控件，（在表格中，不需要前面的标签）
function RenderFormItem(type, attr, val )
{
    var r = "";
    if (type == "div")
        r += "<div " + attr + ">" + val + "</div>";
    else if (type == "div_long")
        r += "<div " + attr + ' style="width: 490px;">' + val + "</div>";
    else if (type == "input")
        r += '<input ' + attr + ' value="' + val + '"/>';
    else if (type == "input_long")
        r += '<input ' + attr + ' style="width:490px;" value="' + val + '" />';
    else if (type == "textarea")
        r += '<textarea ' + attr + ' style="resize:none;width:490px;max-height:45px;">' + val + '</textarea>';
    else if (type == "select")
        r += '<select ' + attr + '>' + val + '</select>';
    else if (type == "date")
        r += '<input ' + attr + ' value="' + val + '" onClick="xrlaydate(this)" />';
    else if (type == "multiselect")
        r += RenderSelectSkill(val);
    return r;
}
//2.控件加标签
function RenderFormIn(entity, fields, cb) {
    var r = "";
    fields.forEach(field => {
        if (field.ftype == "none")
            return;

        var val = entity[field.name];
        var attr = 'name="' + field.name+'" ';
        if (field.name.indexOf("_") != -1)
            attr += 'id="' + field.name + "_" + val + '"';

        var val = cb != undefined ? cb(entity, field) : val;

        r += "<div><label>" + field.title + "</label>";
		if ( field.ftype=="div" || field.ftype=="div_long" ){
			r += `<input type="hidden" name="`+field.name+`" value="`+entity[field.name]+`">`;
			attr = ""; // 清空避免name重复
		}
        r += RenderFormItem(field.ftype, attr, val);
        r += "</div>";
    });
    return r;
}
//3.控件加标签加表单
function RenderForm4(entity, fields, cb) {
    var r = '<div class="x2Form">';
    r +=RenderFormIn(entity, fields, cb);
    r += "</div>";
    return r;
}

//与第4版区别是外包idv改成了form，并增加参数表单的id
function RenderForm5(id, entity, fields, cb) {
    var r = '<form id="{0}" class="x2Form">'.format(id);
    r +=RenderFormIn(entity, fields, cb);
    r += "</form>";
    return r;
}

function xCreateNode(param) {
    var pm = Object(); 
    pm.name = param.name == undefined ? "div" : param.name;
    pm.id = param.id == undefined ? "" : 'id="' + param.id + '"';
    pm.class = param.class == undefined ? "" : 'class="' + param.class + '"';
    pm.style = param.style == undefined ? "" : 'style="' + param.style + '"';
    pm.body = param.body == undefined ? "" : param.body;
    return '<{name} {id} {class} {style} >{body}</{name}>'.format(pm);
}

// 渲染表格--------------begin------------
// twidth:0不显示，无此属性或为-1表示默认宽度
g_TableCurRow = new Object();
function RenderTable2(res, style, fun) {
    var r = "<table id=\"" + res.ls + "\" class=\"xTable\"><thead><tr>";
    if (style)
        r = "<table id=\"" + res.ls + "\" class=\"xTable\" style=\"" + style + "\"><thead><tr>";
    res.fields.forEach(field => {
        if (!field.hasOwnProperty("twidth"))
            field.twidth = -1;
        if (typeof field.twidth == "string") {
            if (field.twidth.length > 0)
                field.twidth = parseInt(field.twidth);
            else
                field.twidth = -1;
        }

        if (field.twidth == -1)
            r += "<th>" + field.title + "</th>";
        else if (field.twidth > 0)
            r += "<th width=\"" + field.twidth + "\">" + field.title + "</th>";
    });
    r += "</tr></thead>\n";

    r += "<tbody>";
    res.data.forEach(x => {
        r += "<tr data_id=\"" + x.id + "\">";
        res.fields.forEach(field => {
            var val = x[field.name];
            if (field.twidth != 0) {
                if (field.tstyle)
                    r += "<td style=\"" + field.tstyle + "\">" + (fun ? fun(x, field) : val) + "</td>";
                else
                    r += "<td>" + (fun ? fun(x, field) : val) + "</td>";
            }
        });
        r += "</tr>";
    });
    r += "</tbody></table>";

    if (res.ls == "dev")
        console.log("tableid=" + res.ls + ",idx=(" + g_TableCurRow[res.ls] + "=>-1)")
    g_TableCurRow[res.ls] = -1;
    return r;
}

// 与第2版区别如下：
// 1.增加参数freeze
// 2.tr的data_id属性加了前缀，当页面中有多个表时，以进行区别
// 3.重写了函数开头部分
function RenderTable3(res, style, freeze, fun) {
	var attr = style == "" ? "" : ` style="`+style+`"`;
	attr += res.ls == "" ? "" : ` id="`+res.ls+`"`;
	attr += !freeze ? "" : ` freeze="true"`;
    var r = `<table class="xTable" ` + attr + `"><thead><tr>`;
    res.fields.forEach(field => {
        if (!field.hasOwnProperty("twidth"))
            field.twidth = -1;
        if (typeof field.twidth == "string") {
            if (field.twidth.length > 0)
                field.twidth = parseInt(field.twidth);
            else
                field.twidth = -1;
        }

        if (field.twidth == -1)
            r += "<th>" + field.title + "</th>";
        else if (field.twidth > 0)
            r += "<th width=\"" + field.twidth + "\">" + field.title + "</th>";
    });
    r += "</tr></thead>\n";

    r += "<tbody>";
    res.data.forEach(x => {
        r += "<tr data_id=\"" +res.ls+"_"+ x.id + "\">";
        res.fields.forEach(field => {
            var val = x[field.name];
            if (field.twidth != 0) {
                if (field.tstyle)
                    r += "<td style=\"" + field.tstyle + "\">" + (fun ? fun(x, field) : val) + "</td>";
                else
                    r += "<td>" + (fun ? fun(x, field) : val) + "</td>";
            }
        });
        r += "</tr>";
    });
    r += "</tbody></table>";

    if (res.ls == "dev")
        console.log("tableid=" + res.ls + ",idx=(" + g_TableCurRow[res.ls] + "=>-1)")
    g_TableCurRow[res.ls] = -1;
    return r;
}


function GetCurRowDataID( tableid ){
	var row = g_TableCurRow[tableid];
	if ( row == -1 )
		return 0;
	return $("#"+tableid+ ">tbody>:nth-child(" + row + ")").attr( "data_id");
}

function SetCurRow(tableid, idx) {
	idx++;
    console.log("tableid=" + tableid + ",idx=(" + g_TableCurRow[tableid] + "=>" + idx + ")")
    var currow = g_TableCurRow[tableid];
    if (currow != -1) {
        if (currow % 2 == 0)
            $("#"+tableid+ ">tbody>:nth-child(" + currow + ")>*").css("background-color", "#f5f5f5");
        else
            $("#"+tableid+ ">tbody>:nth-child(" + currow + ")>*").css("background-color", "#ffffff");
    }
	$("#"+tableid+ ">tbody>:nth-child(" + idx + ")>*").css("background-color", "#00f0f5");
    g_TableCurRow[tableid] = idx;
}

//点击反色
$("html").on("click", function (event) {
    var node = $(event.target);
	var table = node.parents(".xTable");
    if (node[0].localName == "td" && table.length > 0  && table.attr("freeze")==undefined ) {
        node = node.parent();
        var tbody = node.parent();
        var tag = tbody[0].localName;
        if (tag.toLowerCase() == "thead")
            return;

        var tableid = tbody.parent().attr("id");
		if ( tableid != undefined)
			SetCurRow( tableid, node.index() );
    }
});

//按钮下拉窗口，css:  .xCombox .xPopWnd
$("html").on("click", function (event) {
    var node = $(event.target);
    if (node.hasClass("xCombox")) { // 先看是否自己
        var pop = node.children(".xPopWnd");
        pop.toggle();
        $(".xPopWnd").each((i, n) => { if (pop[0] != n) $(n).hide(); });// 关闭其它菜单
    }
    else if (node.parents(".xCombox").length > 0) {
        if (node.hasClass(".xPopWnd")) { //点在菜单背景上  
        }
        else if (node.parents(".xPopWnd").length > 0) { //点在菜单子项上

        }
        else { //点在xCombox的其他子项上
            var cbx = node.parents(".xCombox");
            var pop = cbx.children(".xPopWnd");
            pop.toggle();
            $(".xPopWnd").each((i, n) => { if (pop[0] != n) $(n).hide(); }); // 关闭其它菜单
        }
    }
    else {
        $(".xPopWnd").each((i, n) => { $(n).hide(); }); // 关闭所有菜单
    }
});

//按钮下拉菜单，css  .xCombox .xMenu
//<div class="xCombox">
//    <span>msg to show</span>
//    <div class="xMenu" multi>
//        <div>a</div>
//        <div>b</div>
//        <div class="selected">c</div>
//        <div>d</div>
//    </div>
//</div>
$("html").on("click", function (event) {
    var node = $(event.target);
    if (node.hasClass("xCombox")) { // 在xCombox上
        var pop = node.children(".xMenu");
        pop.toggle();
        $(".xMenu").each((i, n) => { if (pop[0] != n) $(n).hide(); });// 关闭其它菜单
    }
    else if (node.parents(".xCombox").length > 0) {
        if (node.hasClass(".xMenu")) { //点在菜单背景上
        }
        else if (node.parents(".xMenu").length > 0) { //点在菜单子项上
			var menu = node.parents(".xMenu");
            var span = node.parents(".xCombox").children("span");
			if (menu.attr("multi") == undefined ){
				span.html(node.html());
				span.attr("id", node.attr("id"));
			}
			else{
				node.toggleClass( "selected" );
				span.html(menu.children( ".selected" ).toArray().map(x=>$(x).html()).join(","));
			}
            node.parents(".xMenu").hide();
        }
        else { //在xCombox的子项上（不包括xMenu）,例如span
            var cbx = node.parents(".xCombox");
            var pop = cbx.children(".xMenu");
            pop.toggle();
            $(".xMenu").each((i, n) => { if (pop[0] != n) $(n).hide(); });// 关闭其它菜单
        }
    }
    else {
        $(".xMenu").each((i, n) => { $(n).hide(); }); // 不在xCombox内，关闭所有菜单
    }
});


//点击图文表格列表（学历、证件、维修记录等,xpecker.css）
g_curitems = new Array();
$("html").on("click", function (event) {
    var td = $(event.target);
    if (td.parents(".listdata").length > 0) {
        var node = $(td.parents(".listdata")[0]);
        var table = $(node).parent();

        var currow = g_curitems[table.attr("id")];
        if (currow != undefined) {
            currow++;
            if (currow % 2 == 0)
                table.children(":nth-child(" + currow + ")").children().css("background-color", "#f5f5f5");
            else
                table.children(":nth-child(" + currow + ")").children().css("background-color", "#ffffff");
        }
        node.children().css("background-color", "#00f0f5");
        g_curitems[table.attr("id")] = node.index();
    }
});
