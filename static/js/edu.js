// 共用函数
function xredulive(entity, fields) {
    var ximg = { style: "float:left;display:inline-block;", body: xrimagelive2(entity.image1, "image1", "image1") + xrimagelive2(entity.image2, "image2", "image2") };
    var xform = { class: "x2Form", style: "display:inline-block; width:620px;", body: RenderFormIn(entity, fields) };
    return xCreateNode(ximg) + xCreateNode(xform);
}
function xredushow(data) {
    var tpl = `{% it.forEach((x,i)=>{ %}
            <div class="listdata" data_id="{%=x.id%}">
                <div><img src="{%=x.image1%}" /><img src="{%=x.image2%}" /></div>
                <div class="x2Form">
                    <div><label>开始时间</label><div>{%=x.startdate%}</div></div>
                    <div><label>截止时间</label><div>{%=x.enddate%}</div></div>
                    <div><label>学历</label><div>{%=x.degree%}</div></div>
                    <div><label>教育机构</label><div>{%=x.issue%}</div></div>
                </div>
            </div>
            {% }); %}`
    g_curitems["edu"] = -1;
    return dtpl(tpl)(data);
}
function educheck() {
    var formdata = new FormData(document.getElementById("edu_live"));
    var img = formdata.get("image1");
    if (img.size == 0)
        formdata.delete("image1");
    var img = formdata.get("image2");
    if (img.size == 0)
        formdata.delete("image2");
    if (formdata.get("startdate") == "") {
        $("#msg").html("开始时间不能为空！");
        return;
    }
    if (formdata.get("enddate") == "") {
        $("#msg").html("截止时间不能为空！");
        return;
    }
    if (formdata.get("degree") == "") {
        $("#msg").html("学历不能为空！");
        return;
    }
    if (formdata.get("issue") == "") {
        $("#msg").html("颁发机构不能为空！");
        return;
    }

    formdata.append("user_id", g_focus.id);
    return formdata;
}

// 专用函数
function eduupdate() {
    Reqdata("/rd?ls=edu&user_id=" + g_focus.id, "", function (res) {
        g_edus = res;
        $("#edu").html(xredushow(res.data));
    });
}

function oneduadd() {
    var dlg = new cbDlg("新建 教育经历", "width:600px");
    dlg.Add(`<form id="edu_live">` + xredulive(Create(g_edus.fields), g_edus.fields) + `</form>`);
    dlg.Show();
    dlg.submit = function (thisdlg) {
        var fd = educheck();
        if (fd == undefined)
            return;
        postform('/cr?ls=edu', fd, "", eduupdate);
        thisdlg.closedlg();
    };
}
function oneduedit() {
    var idx = g_curitems["edu"];
    if (idx == -1) {
        alert("请选择一个项目");
        return;
    }
    var data_id = $("#edu").children(":nth-child(" + (int(idx) + 1) + ")").attr("data_id");
    var edu = GetSub(g_edus.data, "id", data_id);

    var dlg = new cbDlg("编辑 教育经历", "width:600px");
    dlg.btndel = true;
    dlg.Add(`<form id="certif_live">` + xredulive(edu, g_edus.fields) + `</form>`);
    dlg.Show();
    dlg.submit = function (thisdlg) {
        var fd = educheck();
        if (fd == undefined)
            return;
        postform('/wt?ls=edu&id=' + edu.id, fd, "", eduupdate);
        thisdlg.closedlg();
    };
    dlg.remove = function (thisdlg) {
        Reqdata('/rm?ls=edu&id=' + edu.id, "", eduupdate);
        thisdlg.closedlg();
    }
}
