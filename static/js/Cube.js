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