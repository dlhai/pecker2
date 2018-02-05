//update:
// 0205 改进和移动 xpecker:function RenderForm3(ar, idx) => cube: function RenderForm4(entity, fields, cb )
// 0205 移动位置 xpecker:function RenderTable2(it, style, fun) => cube: function RenderTable2(it, style, fun)
// 0205 移动位置 xpecker:function TableBindClick3(tableid, callback) => cube: function TableBindClick3(tableid, callback)

//表格点击反色
function TableBindClick() {
    var tbc_currow = -1;
    $("tr").click(function () {
        var tag = $(this).parent()[0].localName;
        if (tag.toLowerCase() == "thead")
            return;
        if (tbc_currow != -1) {
            tbc_currow++;
            if (tbc_currow % 2 == 0)
                $(this).parent().children(":nth-child(" + tbc_currow + ")").children().css("background-color", "#f5f5f5");
            else
                $(this).parent().children(":nth-child(" + tbc_currow + ")").children().css("background-color", "#ffffff");
        }
        tbc_currow = $(this).index();
        $(this).children().css("background-color", "#00f0f5");
    });
}
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

function RenderForm3(ar, idx) {
    alert("已改更改为cube::RenderForm4，注意参数有变");
    var r = '<div class="x2Form">';
    for (var i = 0; i < ar.fields.length; i++) {
        var field = ar.fields[i];
        var val = ar.data[idx][field.name];
        if (field.name == "id")
            continue;

        var attr = "";
        if (field.name.indexOf("_") != -1)
            attr = 'id="' + field.name + "_" + val + '"';

        r += "<div><label>" + field.title + "</label>";
        if (field.ftype == "div")
            r += "<div "+attr+">"+val + "</div>";
        else if (field.ftype == "input")
            r += '<input '+attr+' name="' + field.name+'" value="'+ val + '"/>';
        else if (field.ftype == "input_long")
            r += '<input ' + attr +' style="width:490px;" name="' + field.name + '" value="' + val + '" />';
        else if (field.ftype == "textarea")
            r += '<textarea ' + attr +' style="resize:none;width:490px;max-height:45px;" name="' + field.name + '">' + val + '</textarea>';
        else if (field.ftype == "select")
            r += '<select '+attr+' name="'+field.name+'"></select>';
        r += "</div>";
    }
    r += "</div>";
    return r;
}

function RenderPane(ar, idx, fun){
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

        if (field.ftype == "input_long")
            attr += 'style="width:490px;"';
        else if (field.ftype == "textarea")
            attr += 'style="overflow-y: scroll;width:490px;max-height:45px;"';

        r += "<div><label>" + field.title + "</label><div " + attr + ">" + (fun? fun(ar.data[idx],field):val) + "</div></div>";
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
        if (field.ftype == "input_long")
            attr += 'style="width:490px;"';
        else if (field.ftype == "textarea")
            attr += 'style="overflow-y: scroll;width:490px;max-height:45px;"';
        r += "<div><label>" + field.title + "</label><div " + attr + ">" +
            (fun != undefined ? fun(entity, field) : entity[field.name]) + "</div></div>";
    }
    return r;
}


function RenderSelect(ar, selid, type) {
    var r = "";
    for (var i in ar) {
        var x = ar[i];
        if (typeof (type) != "undefined" && x.type != type)
            continue;

        if (x["id"] == selid || x["name"] == selid )
            r += '<option value="' + x["id"] + '" selected>' + x["name"] + '</option>';
        else
            r += '<option value="' + x["id"] + '">' + x["name"] + '</option>';
    }
    return r;
}

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

function RenderForm2(ar, i) {
    alert("使用了旧接口：RenderForm2已被RenderPane替代");
    return "";
    //var r = "";
    //for (var x = 0; x < ar.fields.length; x++) {
    //    if (ar.fields[x].ftype == "bigtext")
    //        r += "<div class=\"xFormItem\"><label>" + ar.fields[x].title + "</label><div style=\"overflow-y: scroll;width:500px;max-height:45px;\">"
    //            + ar.data[i][ar.fields[x].name] + "</div></div>"
    //    else if (ar.fields[x].ftype == "image")
    //        r += "<div class=\"xImgSFZ\"><img src=\"" + ar.data[i][ar.fields[x].name] + "\"/></div>";
    //    else
    //        r += "<div class=\"xFormItem\"><label>" + ar.fields[x].title + "</label><div>" + ar.data[i][ar.fields[x].name] + "</div></div>"
    //}
    //return r;
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

function EFanPane(check ) {
    var tpl = '<div class="xEFanPanel">'
        + '    <header>';
    if (check) tpl += '<input type="checkbox" style="margin-top:0px;">';
    tpl += '            <img src="img/diy/3.png" style="vertical-align:top;"/>'
        + '          <strong>编号:</strong><span>{%=it.code%}</span>'
        + '           <strong>型号:</strong><span>{%=it.type%}</span>'
        + '          <strong>生产厂家:</strong><span class="efanvender_id">{%=it.efanvender_id%}</span>'
        + '          <div style="float: right;">'
        + '              <a id="{%=it.id%}" onClick="EditEfan(this)">编辑</a>'
        + '          </div>'
        + '      </header>'
        + '      <table>'
        + '          <thead><tr><th>编号</th><th>主要材料</th><th>出厂时间</th><th>挂机时间</th><th>生产厂家</th></tr></thead>'
        + '          <tbody>'
        + '              {% for (var j in it.leafs) { %}'
        + '              <tr>'
        + '                  <td>{%=it.leafs[j].code%}</td>'
        + '                  <td>{%=it.leafs[j].mat%}</td>'
        + '                  <td>{%=it.leafs[j].producedate%}</td>'
        + '                  <td>{%=it.leafs[j].putondate%}</td>'
        + '                  <td class="leafvender_id">{%=it.leafs[j].leafvender_id%}</td>'
        + '              </tr>'
        + '              {% } %}'
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
        + '   <strong>生产厂家:</strong><select class="efanvender_id" data-id="{%=it.efanvender_id%}" name="efanvender_id" style="margin-right:0px;"></select>'
        + '</form>'
        + '<form id="form_leaf0" /><form id="form_leaf1" /><form id="form_leaf3" />'
        + '<table>'
        + '    <thead><tr><th>编号</th><th>主要材料</th><th>出厂时间</th><th>挂机时间</th><th style="width:90px">生产厂家</th></tr></thead>'
        + '    <tbody>'
        + '        {% for (var i = 0; i < it.leafs.length; i++) { %}'
        + '        <tr>'
        + '            <td><input form="form_leaf{%=it.leafs[i]%}" name="code" value="{%=it.leafs[i].code%}" /></td>'
        + '            <td><input form="form_leaf{%=it.leafs[i]%}" name="mat" value="{%=it.leafs[i].mat%}" /></td>'
        + '            <td><input form="form_leaf{%=it.leafs[i]%}" name="producedate" value="{%=it.leafs[i].producedate%}" onClick="laydate()" /></td>'
        + '            <td><input form="form_leaf{%=it.leafs[i]%}" name="putondate" value="{%=it.leafs[i].putondate%}" onClick="laydate()" /></td>'
        + '            <td><select form="form_leaf{%=it.leafs[i]%}" class="leafvender_id" name="leafvender_id" data-id="{%=it.leafs[i].leafvender_id%}" ></select></td>'
        + '        </tr>'
        + '        {% } %}'
        + '    </tbody>'
        + '</table>'
        + '</div>');
}
EfanForm.prototype.Render = function (efan) {
    return this.tpl(efan);
}

// 树控件

// ID 根节点类型, 叶节点类型, 点击回调函数
function x3Tree(id, ls, param, leaf, ItemClick ) {
    this.leaf = leaf;
    this.ItemClick = ItemClick;
    this.Req(id, ls, param);
    this.root = true;

    this.branch = {
        "devwh": { "sub": "", "image": "img/devwh.png", },

        "root": { "sub": "winderco", "image": "", },
        "winderco": {"sub": "winderprov", "image": "img/diy/1_open.png" },
        "winderprov": { "sub": "winder", "image": "img/folder.gif" },
        "winder": { "sub": "winderarea", "image": "img/diy/3.png" },
        "winderarea": { "sub": "efan", "image": "img/page.gif" },
        "efan": { "sub": "leaf", "image": "" },
        "leaf": { "sub": "", "image": "" },
    }
}
x3Tree.prototype.Req = function (id, ls, param) {
    Reqdata("/rd?ls=" + ls + (param ? "&" + param:""), this, function (res, ctx) {
        var html = "";
        var data = res.data;
        for (var i in res.data) {
            if (ls == ctx.leaf) { // 叶节点，少了左边的加号，为缩进对齐加了一层div
                if (this.root){
                    html += "<div><div id=\"" + ls + "_" + data[i].id + "\"><span><img src=\""
                        + ctx.branch[ls].image + "\">" + data[i].name + "</span></div></div>\n"
                }
                else {
                    html += "<div id=\"" + ls + "_" + data[i].id + "\"><span><img src=\""
                        + ctx.branch[ls].image + "\">" + data[i].name + "</span></div>\n"
                }
            }
            else { // 
                html += "<div id=\"" + ls + "_" + data[i].id + "\">"
                    + "<img src=\"img/nolines_plus.gif\"><span><img src=\""
                    + ctx.branch[ls].image + "\">" + data[i].name + "</span></div>\n"
            }
            this.root = false;
        }

        $("#" + id).append(html);
        $("#" + id).children("img").attr("src", "img/nolines_minus.gif"); // 把加号改成减号
        $(".xTree div>img").off("click", "", ctx.ItemExpand);
        $(".xTree div>span").off("click", "", ctx.ItemClick);
        $(".xTree div>img").on("click", "", {}, ctx.ItemExpand);
        $(".xTree div>span").on("click", "", {}, ctx.ItemClick);
    });
}
//点击树节点的加号
x3Tree.prototype.ItemExpand = function () {
    alert("hahah!");
    var siblings = $(ev.target).siblings("div");
    if (siblings.length == 0) {
        var id = $(ev.target).parent().attr("id");
        var at = id.split("_");
        Req(id, branch[ls].sub, at[0] + "_id=" + at[1])
    }
    else if (siblings.css("display") == "none") {
        $(event.srcElement).attr("src", "img/nolines_minus.gif");
        siblings.css("display", "block");
    }
    else {
        $(event.srcElement).attr("src", "img/nolines_plus.gif");
        siblings.css("display", "none");
    }
}
