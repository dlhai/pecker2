//update:
// 0205 改进和移动 xpecker:function RenderForm3(ar, idx) => cube: function RenderForm4(entity, fields, cb )
// 0205 移动位置 xpecker:function RenderTable2(it, style, fun) => cube: function RenderTable2(it, style, fun)
// 0205 移动位置 xpecker:function TableBindClick3(tableid, callback) => cube: function TableBindClick3(tableid, callback)
g = new Object();

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
// 3.增加update、addchild、remove等方法
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
    var img = g_treebranch[res.ls].image;
    res.data.forEach(x => {
        $("#" + res.ls + "_" + x.id +">span" ).html("<img src=\"" + img + "\">" + x.name);
    });
}

// 添加子节点
x5Tree.prototype.addchild = function (expr,res) {
    var html = "";
	var ls = res.ls;
	var img = g_treebranch[ls].image;
	res.data.forEach(x => {
        if (ls == this.leaf) { // 叶节点，少了左边的加号，为缩进对齐加了一层div
            if (this.expr == expr) { // 根节点是叶节点时，不要加外层div
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
        $("#" + res.ls + "_" + x.id).remove();
    });
}

x5Tree.prototype.Req = function (expr, ls, param) {
    Reqdata("/rd?ls=" + ls + (param ? "&" + param : ""), this, function (res, ctx) {
		ctx.addchild(expr, res);
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
