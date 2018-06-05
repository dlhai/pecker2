// 共用函数
function xrcertiflive(entity, fields) {
    var ximg = { style: "float:left;display:inline-block;", body: xrimagelive2(entity.image, "image", "image") };
    var xform = { class: "x2Form", style: "display:inline-block; width:620px;", body: RenderFormIn(entity, fields) };
    return xCreateNode(ximg) + xCreateNode(xform);
}
function xrcertifshow(data) {
    var tpl = `{% it.forEach((x,i)=>{ %}
            <div class="listdata" data_id="{%=x.id%}">
                <div><img src="{%=x.image%}" /></div>
                <div class="x2Form">
                    <div><label>证件名称</label><div>{%=x.name%}</div></div>
                    <div><label>证件编号</label><div>{%=x.code%}</div></div>
                    <div><label>颁发机构</label><div>{%=x.issue%}</div></div>
                    <div><label>颁发时间</label><div>{%=x.issuedate%}</div></div>
                </div>
            </div>
            {% }); %}`
    g_curitems["certif"] = -1;
    return dtpl(tpl)(data);
}

function certifcheck() {
    var formdata = new FormData(document.getElementById("certif_live"));
    var img = formdata.get("image");
    if (img.size == 0)
        formdata.delete("image");
    if (formdata.get("name") == "") {
        $("#msg").html("证件名称不能为空！");
        return;
    }
    if (formdata.get("code") == "") {
        $("#msg").html("证件编号不能为空！");
        return;
    }
    if (formdata.get("issue") == "") {
        $("#msg").html("颁发机构不能为空！");
        return;
    }
    if (formdata.get("issuedate") == "") {
        $("#msg").html("颁发时间不能为空！");
        return;
    }
    formdata.append("user_id", g_focus.id);
    return formdata;
}

// 专用函数
function certifupdate() {
    Reqdata("/rd?ls=certif&user_id=" + g_focus.id, "", function (res) {
        g_certifs = res;
        $("#certif").html(xrcertifshow(res.data));
    });
}

function oncertifadd() {
    var dlg = new cbDlg("新建 证件", "width:600px");
    dlg.Add(`<form id="certif_live">` + xrcertiflive(Create(g_certifs.fields), g_certifs.fields) + `</form>`);
    dlg.Show();
    dlg.submit = function (thisdlg) {
        var fd = certifcheck();
        if (fd == undefined)
            return;
        postform('/cr?ls=certif', fd, "", certifupdate);
        thisdlg.closedlg();
    };
}
function oncertifedit() {
    var idx = g_curitems["certif"];
    if (idx == -1){
        alert("请选择一个项目");
        return;
    }
    var data_id = $("#certif").children(":nth-child(" + (int(idx) + 1) + ")").attr("data_id");
    var certif = GetSub(g_certifs.data, "id", data_id);

    var dlg = new cbDlg("编辑 证件", "width:600px");
    dlg.btndel = true;
    dlg.Add(`<form id="certif_live">` + xrcertiflive(certif, g_certifs.fields) + `</form>`);
    dlg.Show();
    dlg.submit = function (thisdlg) {
        var fd = certifcheck();
        if (fd == undefined)
            return;
        postform('/wt?ls=certif&id=' + certif.id, fd, "", certifupdate);
        thisdlg.closedlg();
    };
    dlg.remove = function (thisdlg) {
        Reqdata('/rm?ls=certif&id=' + certif.id, "", certifupdate);
        thisdlg.closedlg();
    }
}
