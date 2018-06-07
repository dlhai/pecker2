//update:
// 0205 改进和移动 xpecker:function RenderForm3(ar, idx) => cube: function RenderForm4(entity, fields, cb )
// 0205 移动位置 xpecker:function RenderTable2(it, style, fun) => cube: function RenderTable2(it, style, fun)
// 0205 移动位置 xpecker:function TableBindClick3(tableid, callback) => cube: function TableBindClick3(tableid, callback)
g = new Object();

//表格点击反色
var g_TableCurRow = new Object();
function TableBindClick2(tableid) {
    var currow = -1;
    $("#"+tableid+" tr").click(function () {
        var tag = $(this).parent()[0].localName;
        if (tag.toLowerCase() == "thead")
            return;
        if (currow != -1) {
            currow++;
            if (currow % 2 == 0)
                $(this).parent().children(":nth-child(" + currow + ")").children().css("background-color", "#f5f5f5");
            else
                $(this).parent().children(":nth-child(" + currow + ")").children().css("background-color", "#ffffff");
        }
        currow = $(this).index();
        g_TableCurRow[tableid] = $(this).attr("data_id");
        $(this).children().css("background-color", "#00f0f5");
    });
}

//文档控件
$(function () {
    $(".x3Doc>.x3Doc-handle").on("click", function ()
    {
        $(this).siblings(".x3Doc-menu").css("display", "block");
        $(this).siblings(".x3Doc-menu").addClass("x3Doc-click");
    });

    window.onclick = x3DocMenuHide;
    function x3DocMenuHide() {
        $(".x3Doc-menu:not(.x3Doc-click)").css("display", "none");
        $(".x3Doc>.x3Doc-click").removeClass("x3Doc-click");
    }
});

// 直接为数组用这一版
function RenderSelect(ar, selid, type) {
    var r = "";
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
    for (var i in res.data) {
        var x = res.data[i];
        if (x["id"] == selid || x["name"] == selid)
            r += '<option value="' + x["id"] + '" selected>' + x["name"] + '</option>';
        else
            r += '<option value="' + x["id"] + '">' + x["name"] + '</option>';
    }
    return r;
}

function ID2Name(ar, idx) {
    var param = new Array();
    for (var i in ar.fields) {
        var name = ar.fields[i].name;
        var val = ar.data[idx][name];
        if (name.indexOf("_") != -1 && val != "" && ar.fields[i].type != "select" )
            param.push(name + "=" + val);
    }
    if (param.length == 0)
        return;

    Reqdata("/id2name?" + param.join("&"), "", function (d) {
        for (var j in d) {
            $("#"+j).html(d[j]);
            $("#"+j).removeAttr("id"); // 清除ID属性是因为弹出表单时，有可能导致ID重复
        }
    });
}

function fillselect(ar, idx) {
    for (var i in ar.fields) {
        var fields = ar.fields[i];
        if (fields.ftype == "select") {
            var at = fields.name.split("_");
            Reqdata("/rd?ls=" + at[0], function (d) {
                var selid = ar.data[idx][fields.name];
                $("#" + fields.name + "_" + selid).html(RenderSelect(d, selid));
            });
        }
    }
}

function EFanCreate(fields1, fields2, winder_id, area_id) {
    var efan = Create(fields1);
    efan.winder_id = g_user.depart_id;
    efan.winderarea_id = g_winderarea_id;
    efan.leafs = [Create(fields2), Create(fields2), Create(fields2)];
    efan.leafs[0].winder_id = g_user.depart_id;
    efan.leafs[0].winderarea_id = g_winderarea_id;
    efan.leafs[1].winder_id = g_user.depart_id;
    efan.leafs[1].winderarea_id = g_winderarea_id;
    efan.leafs[2].winder_id = g_user.depart_id;
    efan.leafs[2].winderarea_id = g_winderarea_id;
    return efan;
}

function xrefan(efan) {
    var tpl = doT.template(`<div class="xEFanPanel">
            <header>
                <img src="img/diy/3.png" style="vertical-align:top;"/>
                <strong>编号:</strong><span>{%=it.code%}</span>
                <strong>型号:</strong><span>{%=it.type%}</span>
                <strong>生产厂家:</strong><span>{%=ShowField(it,"efanvender_id")%}</span>
             </header>
             <table>
                 <thead><tr><th>编号</th><th>主要材料</th><th>出厂时间</th><th>挂机时间</th><th>生产厂家</th></tr></thead>
                 <tbody>
                     {% it.leafs.forEach(leaf=> { %}
                     <tr>
                         <td>{%=leaf.code%}</td>
                         <td>{%=leaf.mat%}</td>
                         <td>{%=leaf.producedate%}</td>
                         <td>{%=leaf.putondate%}</td>
                         <td>{%=ShowField(leaf,"leafvender_id")%}</td>
                     </tr>
                     {% }); %}
                 </tbody>
             </table>
         </div>`);
    return tpl(efan);
}

function EFanPane(check ) {
    var tpl = '<div class="xEFanPanel">'
        + '    <header>';
    if (check) tpl += '<input type="checkbox" style="margin-top:0px;">';
    tpl += //'            <img src="img/diy/3.png" style="vertical-align:top;"/>'+
         '          <strong>编号:</strong><span>{%=it.code%}</span>'
        + '           <strong>型号:</strong><span>{%=it.type%}</span>'
        + '          <strong>生产厂家:</strong><span>{%=FieldToShow(it,"efanvender_id")%}</span>'
        + '          <div style="float: right;">'
        + '              <a id="{%=it.id%}" onClick="EditEfan(this)">编辑</a>'
        + '          </div>'
        + '      </header>'
        + '      <table>'
        + '          <thead><tr><th>编号</th><th>主要材料</th><th>出厂时间</th><th>挂机时间</th><th>生产厂家</th></tr></thead>'
        + '          <tbody>'
        + '              {% it.leafs.forEach(leaf=> { %}'
        + '              <tr>'
        + '                  <td>{%=leaf.code%}</td>'
        + '                  <td>{%=leaf.mat%}</td>'
        + '                  <td>{%=leaf.producedate%}</td>'
        + '                  <td>{%=leaf.putondate%}</td>'
        + '                  <td>{%=FieldToShow(leaf,"leafvender_id")%}</td>'
        + '              </tr>'
        + '              {% }); %}'
        + '          </tbody>'
        + '      </table>'
        + '  </div>';
    this.tpl = doT.template(tpl);
}

EFanPane.prototype.Render = function( efan ){
    return this.tpl(efan);
}

function EfanForm() {
    this.tpl = doT.template('<div class="xEFanForm">'
        + '<form id="form_efan">'
        + '    <strong>编号:</strong><input name="code" value="{%=it.code%}" />'
        + '    <strong>型号:</strong><input name="type" value="{%=it.type%}" />'
        + '   <strong>生产厂家:</strong><select name="efanvender_id" style="margin-right:0px;">{%=FieldToEdit(it,"efanvender_id")%}</select>'
        + '</form>'
        + '<form id="form_leaf0" /><form id="form_leaf1" /><form id="form_leaf3" />'
        + '<table>'
        + '    <thead><tr><th>编号</th><th>主要材料</th><th>出厂时间</th><th>挂机时间</th><th style="width:90px">生产厂家</th></tr></thead>'
        + '    <tbody>'
        + '        {% for (var i = 0; i < it.leafs.length; i++) { %}'
        + '        <tr>'
        + '            <td><input form="form_leaf{%=it.leafs[i]%}" name="code" value="{%=it.leafs[i].code%}" /></td>'
        + '            <td><input form="form_leaf{%=it.leafs[i]%}" name="mat" value="{%=it.leafs[i].mat%}" /></td>'
        + '            <td><input form="form_leaf{%=it.leafs[i]%}" name="producedate" value="{%=it.leafs[i].producedate%}" onClick="xrlaydate(this)" /></td>'
        + '            <td><input form="form_leaf{%=it.leafs[i]%}" name="putondate" value="{%=it.leafs[i].putondate%}" onClick="xrlaydate(this)" /></td>'
        + '            <td><select form="form_leaf{%=it.leafs[i]%}" name="leafvender_id" data-id="{%=FieldToEdit(it.leafs[i],"leafvender_id")%}" ></select></td>'
        + '        </tr>'
        + '        {% } %}'
        + '    </tbody>'
        + '</table>'
        + '</div>');
}
EfanForm.prototype.Render = function (efan) {
    return this.tpl(efan);
}

// 树控件，与第3版的区别:
// 1.事件使用了委托，不再要绑定
// 2.使用expr，不用ID，更加灵活
// <div id="{ls_id}">
//     <img src="plus.gif">
//     <span><img src="{face.jpg}">{text}</span>
//     <div>next grade</div>
//     <div>next grade</div>
//     ......
// </div>
// ID 根节点类型, 叶节点类型, 点击回调函数
function x4Tree(expr, ls, param, leaf, useritemclick) {
    $(expr).addClass("x4Tree");
    $(expr).attr("x4Tree");
    this.leaf = leaf;
    this.onTreeItemClick = useritemclick;
    this.Req(expr, ls, param);
    this.root = true;

    if (typeof g_treebranch == "undefined") {
        g_treebranch = {
            "devwh": { "sub": "", "image": "img/devwh.png", },

            "matprov": { "sub": "matwh", "image": "img/folder.gif", },
            "matwh": { "sub": "", "image": "img/devwh.png", },

            "root": { "sub": "winderco", "image": "", },
            "winderco": { "sub": "winderprov", "image": "img/diy/1_open.png" },
            "winderprov": { "sub": "winder", "image": "img/folder.gif" },
            "winder": { "sub": "winderarea", "image": "img/diy/3.png" },
            "winderarea": { "sub": "efan", "image": "img/page.gif" },
            "efan": { "sub": "leaf", "image": "" },
            "leaf": { "sub": "", "image": "" },
        }
    }
}
x4Tree.prototype.Req = function (expr, ls, param) {
    Reqdata("/rd?ls=" + ls + (param ? "&" + param : ""), this, function (res, ctx) {
        var html = "";
        var data = res.data;
        res.data.forEach(x => {
            if (ls == ctx.leaf) { // 叶节点，少了左边的加号，为缩进对齐加了一层div
                if (ctx.root) { // 根节点是叶节点时，不要加外层div
                    html += "<div id=\"" + ls + "_" + x.id + "\"><span><img src=\""
                        + g_treebranch[ls].image + "\">" + x.name + "</span></div>\n"
                }
                else {
                    html += "<div><div id=\"" + ls + "_" + x.id + "\"><span><img src=\""
                        + g_treebranch[ls].image + "\">" + x.name + "</span></div></div>\n"
                }
            }
            else { // 
                html += "<div id=\"" + ls + "_" + x.id + "\">"
                    + "<img src=\"img/nolines_plus.gif\"><span><img src=\""
                    + g_treebranch[ls].image + "\">" + x.name + "</span></div>\n"
            }
        });
        ctx.root = false;

        $(expr).append(html);
        $(expr).children("img").attr("src", "img/nolines_minus.gif"); // 把加号改成减号
    });
}
x4Tree.prototype.Extend = function (expr) {
    var node = $(expr);
    var children = node.children("div");
    if (children.length == 0) { // 无子项,去请求
        var at = expr.slice(1).split("_");
        this.Req(expr, g_treebranch[at[0]].sub, at[0] + "_id=" + at[1]);
    }
    else if (children.css("display") == "none") { // 有子项,展开
        $(event.srcElement).attr("src", "img/nolines_minus.gif");
        children.css("display", "block");
    }
    else { // 有子项,合并
        $(event.srcElement).attr("src", "img/nolines_plus.gif");
        children.css("display", "none");
    }
}

// 树控件的事件处理
$("html").on("click", function (event) {
    if (event.target.tagName != "IMG" && event.target.tagName != "SPAN")
        return;
    var node = $(event.target);
    if (node.parents(".x4Tree").length == 0)
        return;
    var treeid = node.parents(".x4Tree").attr("id");
    if ( g[treeid] == undefined)
        return;
    if (event.target.tagName == "IMG" && node.parent()[0].tagName == "DIV") { // 点在加号上
        var id = node.parent().attr("id");
        g[treeid].Extend("#" + id);
    }
    else { //  点在标签上
        if (event.target.tagName == "IMG")
            var id = node.parent().parent().attr("id");
        else
            var id = node.parent().attr("id");
        if (g[treeid].onTreeItemClick != undefined){
            var at = id.split("_");
            g[treeid].onTreeItemClick(at[0], at[1], node); // 回调
        }
    }
});


// 树控件，与第4版的区别:
// 1.事件委托位置优化到x5Tree
// 2.onTreeItemClick的参数node为span节点，3版可能为faceimg
// <div id="{ls_id}">
//     <img src="plus.gif">
//     <span><img src="{face.jpg}">{text}</span>
//     <div>next grade</div>
//     <div>next grade</div>
//     ......
// </div>
// ID 根节点类型, 叶节点类型, 点击回调函数
function x5Tree(expr, ls, param, leaf, useritemclick) {
	this.expr = expr;
	this.ls = ls;
    this.param = param;
    this.leaf = leaf;
    this.onTreeItemClick = useritemclick;

    this.Req(expr, ls, param);

	// 树控件的事件处理
	var tree = $(expr);
    tree.addClass("xTree");
	tree.on("click", function (event) {
		if (event.target.tagName != "IMG" && event.target.tagName != "SPAN")
			return;
		var node = $(event.target);
		var treeid = node.parents(".xTree").attr("id");
		if ( g[treeid] == undefined){
			alert("找不到xTree对象");
			return;
		}
		if (event.target.tagName == "IMG" && node.parent()[0].tagName == "DIV") { // 点在加号上
			var id = node.parent().attr("id");
			g[treeid].Extend("#" + id);
		}
		else { //  点在标签上
			if (g[treeid].onTreeItemClick != undefined){
				if (event.target.tagName == "IMG")
					node = node.parent();
				node = node.parent();
				var at = node.attr("id").split("_");
				g[treeid].onTreeItemClick(at[0], at[1], node); // 回调
			}
		}
	});
}

// 重置节点的子节点列表(暂无用途故屏蔽)
// x5Tree.prototype.reset = function (expr) {
// 	if (!expr || expr == "")
// 		expr ="#root";
// 	$(expr).html("");
// 	this.Req(expr, this.ls, this.param);
// }

// 设置节点文本
x5Tree.prototype.update = function (res) {
	res.data.forEach(x => {
		$("#"+res.ls+"_"+x.id).html("<span><img src=\"" + img + "\">" + x.name + "</span>");
	}
}

// 添加子节点
x5Tree.prototype.addchild = function (expr,res) {
    var html = "";
	var ls = res.ls;
	var img = g_treebranch[ls].image;
	res.data.forEach(x => {
        if (ls == ctx.leaf) { // 叶节点，少了左边的加号，为缩进对齐加了一层div
            if (ctx.root) { // 根节点是叶节点时，不要加外层div
                html += "<div id=\"" + ls + "_" + x.id + "\"><span><img src=\""
                    + img + "\">" + x.name + "</span></div>\n"
            }
            else {
                html += "<div><div id=\"" + ls + "_" + x.id + "\"><span><img src=\""
                    + img + "\">" + x.name + "</span></div></div>\n"
            }
        }
        else { // 
            html += "<div id=\"" + ls + "_" + x.id + "\">"
                + "<img src=\"img/nolines_plus.gif\"><span><img src=\""
                + img + "\">" + x.name + "</span></div>\n"
		}
    });
    $(expr).append(html);
}

// 删除子节点
x5Tree.prototype.remove = function (res) {
	res.data.forEach(x => {
		$("#"+res.ls+"_"+x.id).remove();
	}
}

x5Tree.prototype.Req = function (expr, ls, param) {
    Reqdata("/rd?ls=" + ls + (param ? "&" + param : ""), this, function (res, ctx) {
		addchild(res);
        $(expr).children("img").attr("src", "img/nolines_minus.gif"); // 把加号改成减号
    });
}
x5Tree.prototype.Extend = function (expr) {
    var node = $(expr);
    var children = node.children("div");
    if (children.length == 0) { // 无子项,去请求
        var at = expr.slice(1).split("_");
        this.Req(expr, g_treebranch[at[0]].sub, at[0] + "_id=" + at[1]);
    }
    else if (children.css("display") == "none") { // 有子项,展开
        $(event.srcElement).attr("src", "img/nolines_minus.gif");
        children.css("display", "block");
    }
    else { // 有子项,合并
        $(event.srcElement).attr("src", "img/nolines_plus.gif");
        children.css("display", "none");
    }
}
