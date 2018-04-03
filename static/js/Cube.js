$("html").on("change", function () {
    var node = event.target;
    if (node.tagName == "INPUT" && node.type == "file") {
        var file = node.files[0];
        var reader = new FileReader();
        reader.onload = function (e) { $(node).prev().attr("src", e.target.result); };
        reader.readAsDataURL(file);
        var parent = $(node).parent().parent();
        if (parent.next().length == 0) {
            parent.append(xrimagelive(""));
        }
    }
});

function xrimagelist(img) {
    var tpl = `<label for="{id}"><img style="width: 100%; height: 100%;" {img} />
                        <input type="file" id="{id}" accept="image/*"></label>`;
    return tpl.format({ id: rndstr(8), img: (img == "" ? "" : 'src="' + img + '"') });
}

//背景带十字，点击可换图
function xrimagelive(img) {
    var image = img == "" ? "" : 'src="' + img + '"')
    var width = arguments[1] ? arguments[1] : "100%";
    var heigh = arguments[2] ? arguments[2] : "100%";
    var tpl = `<label for="{id}"><img style="width: {width}; height: {heigh};" {image} />
                        <input type="file" id="{id}" accept="image/*"></label>`;
    return tpl.format({ id: rndstr(8), image: image, width: width, height: heigh });
}
//背景带十字，点击可换图的列表
function xrimagelistlive(imglist) {
    return `<div class="imagelistlive">` + imglist.map(x => xrimagelive(x)) + `</div>`;
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
        + '    <div class="modal-footer">';
    if (this.btndel) html += '        <div style="float:left;"><button type="button" class="btn btn-default" style="color:#aaaaaa">删除</button></div>';
    html += '        <button type="button" class="btn btn-primary">提交</button>'
        + '        <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>'
        + '    </div>'
        + '</div><!-- /.modal-content -->'
        + '</div><!-- /.modal -->';
    $("body").append(html);
    var btn = $('#' + this.id).find("button");
    btn.on("click", '', { id: this.id, closedlg: this.closedlg, submit: this.submit }, function (ev) {
        if (ev.target.innerText == "提交") ev.data.submit();
        else if (ev.target.innerText == "关闭") ev.data.closedlg();
        $('#' + ev.data.id).remove();
    });
    $('#' + this.id).modal('show');
}
function showDlg() {
    var dlg = new cbDlg();
    dlg.Show();
}

// 渲染表单,三步
//1.仅渲染控件，（在表格中，不需要前面的标签）
function RenderFormItem(type, attr, val )
{
    var r = "";
    if (type == "div")
        r += "<div " + attr + ">" + val + "</div>";
    else if (type == "input")
        r += '<input ' + attr + '" value="' + val + '"/>';
    else if (type == "input_long")
        r += '<input ' + attr + ' style="width:490px;" value="' + val + '" />';
    else if (type == "textarea")
        r += '<textarea ' + attr + ' style="resize:none;width:490px;max-height:45px;">' + val + '</textarea>';
    else if (type == "select")
        r += '<select ' + attr + '">' + val + '</select>';
    else if (type == "date")
        r += '<input ' + attr + '" value="' + val + '" onClick="laydate()" />';
    return r;
}
//2.控件加标签
function RenderFormIn(entity, fields, cb) {
    var r = "";
    fields.forEach(field => {
        if (field.ftype == "none")
            return;

        var val = entity[field.name];
        var attr = "";
        if (field.name.indexOf("_") != -1)
            attr = 'id="' + field.name + "_" + val + '"';

        var val = cb != undefined ? cb(entity, field) : val;

        r += "<div><label>" + field.title + "</label>";
        if (field.ftype == "div")
            r += "<div " + attr + ">" + val + "</div>";
        if (field.ftype == "div_long")
            r += "<div " + attr + ' style="width: 490px;">' + val + "</div>";
        else if (field.ftype == "input")
            r += '<input ' + attr + ' name="' + field.name + '" value="' + val + '"/>';
        else if (field.ftype == "input_long")
            r += '<input ' + attr + ' style="width:490px;" name="' + field.name + '" value="' + val + '" />';
        else if (field.ftype == "textarea")
            r += '<textarea ' + attr + ' style="resize:none;width:490px;max-height:45px;" name="' + field.name + '">' + val + '</textarea>';
        else if (field.ftype == "select")
            r += '<select ' + attr + ' name="' + field.name + '">' + val + '</select>';
        else if (field.ftype == "date")
            r += '<input ' + attr + ' name="' + field.name + '" value="' + val + '" onClick="laydate()" />';
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

// 渲染表格
// twidth:0不显示，无此属性或为-1表示默认宽度
function RenderTable2(res, style, fun) {
    var r = "<table id=\"" + res.ls + "\" class=\"xTable\"><thead><tr>";
    if (style)
        r = "<table id=\"" + res.ls + "\" class=\"" + style + "\"><thead><tr>";
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
    return r;
}
function TableBindClick3(tableid, callback) {
    var currow = -1;
    $("#" + tableid + " tr").click(function () {
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
        $(this).children().css("background-color", "#00f0f5");

        currow = $(this).index();
        g_TableCurRow[tableid] = $(this).attr("data_id");

        if (callback)
            callback($(this).attr("data_id"));
    });
}

//按钮下拉窗口，css:  .xCombox .xPopWnd
$("html").on("click", function () {
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
$("html").on("click", function () {
    var node = $(event.target);
    if (node.hasClass("xCombox")) { // 先看是否自己
        var pop = node.children(".xMenu");
        pop.toggle();
        $(".xMenu").each((i, n) => { if (pop[0] != n) $(n).hide(); });// 关闭其它菜单
    }
    else if (node.parents(".xCombox").length > 0) {
        if (node.hasClass(".xMenu")) { //点在菜单背景上  
        }
        else if (node.parents(".xMenu").length > 0) { //点在菜单子项上
            var span = node.parents(".xCombox").children("span");
            span.html(node.html());
            span.attr("id", node.attr("id"));
            node.parents(".xMenu").hide();
        }
        else { //点在xCombox的其他子项上
            var cbx = node.parents(".xCombox");
            var pop = cbx.children(".xMenu");
            pop.toggle();
            $(".xMenu").each((i, n) => { if (pop[0] != n) $(n).hide(); });// 关闭其它菜单
        }
    }
    else {
        $(".xMenu").each((i, n) => { $(n).hide(); }); // 关闭所有菜单
    }
});

