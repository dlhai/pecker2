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
        + '    <div id="ModalDlgContent" class="modal-body" style="padding:5px 0px">';
    for (var i in this.subs) html += this.subs[i].toString();
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

// 渲染表单
function RenderForm4(entity, fields, cb ) {
    var r = '<div class="x2Form">';
    for (var i in fields ) {
        var field = fields[i];
        if (field.ftype == "none")
            continue;

        var val = entity[field.name];
        var val = cb != undefined ? cb(entity, field):val;
        var attr = "";
        if (field.name.indexOf("_") != -1)
            attr = 'id="' + field.name + "_" + val + '"';

        r += "<div><label>" + field.title + "</label>";
        if (field.ftype == "div")
            r += "<div " + attr + ">" + val + "</div>";
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
    }
    r += "</div>";
    return r;

}

// 渲染表格
// twidth:0不显示，无此属性或为-1表示默认宽度
function RenderTable2(res, style, fun) {
    var r = "<table id=\"" + res.ls + "\" class=\"xTable\"><thead><tr>";
    if (style)
        r = "<table id=\"" + res.ls+ "\" class=\"" + style + "\"><thead><tr>";
    for (var c in res.fields) {
        if (res.fields[c].hasOwnProperty("twidth")) {
            if (typeof res.fields[c].twidth == "string")
                res.fields[c].twidth = parseInt(res.fields[c].twidth);
        }
        else
            res.fields[c].twidth = -1;
        if (res.fields[c].twidth == -1)
            r += "<th>" + res.fields[c].title + "</th>";
        else if (res.fields[c].twidth > 0)
            r += "<th width=\"" + res.fields[c].twidth + "\">" + res.fields[c].title + "</th>";
    }
    r += "</tr></thead>\n";

    r += "<tbody>";
    for (var x in res.data) {
        r += "<tr data_id=\"" + res.data[x].id + "\">";
        for (c in res.fields) {
            var field = res.fields[c];
            var val = res.data[x][field.name];
            if (res.fields[c].twidth != 0) {
                if (field.tstyle)
                    r += "<td style=\"" + field.tstyle + "\">" + (fun ? fun(res.data[x], field) : val) + "</td>";
                else
                    r += "<td>" + (fun ? fun(res.data[x], field) : val) + "</td>";
            }
        }
        r += "</tr>";
    }
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
