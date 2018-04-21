// 共用函数
function xremploylive(entity, fields) {
    var ximg = { style: "float:left;display:inline-block;", body: xrimagelive2(entity.image, "image", "image") };
    var xform = { class: "x2Form", style: "display:inline-block; width:620px;", body: RenderFormIn(entity, fields) };
    return xCreateNode(ximg) + xCreateNode(xform);
}
function xremployshow(data) {
    var tpl = `{% it.forEach((x,i)=>{ %}
            <div class="listdata" data_id="{%=x.id%}">
                <div><img src="{%=x.image%}" /> </div>
                <div class="x2Form">
                    <div><label>工作单位</label><div>{%=x.Organization%}</div></div>
                    <div><label>岗位</label><div>{%=x.position%}</div></div>
                    <div><label>开始时间</label><div>{%=x.startdate%}</div></div>
                    <div><label>结束时间</label><div>{%=x.enddate%}</div></div>
                </div>
            </div>
            {% }); %}`
    return dtpl(tpl)(data);
}

function employcheck() {
    var formdata = new FormData(document.getElementById("employ_live"));
    if (formdata.get("Organization") == "") {
        $("#msg").html("工作单位不能为空！");
        return;
    }
    if (formdata.get("position") == "") {
        $("#msg").html("岗位不能为空！");
        return;
    }
    if (formdata.get("startdate") == "") {
        $("#msg").html("开始时间不能为空！");
        return;
    }
    if (formdata.get("enddate") == "") {
        $("#msg").html("结束时间不能为空！");
        return;
    }
    formdata.append("user_id", g_focus.id);
    return formdata;
}

// 专用函数
function employupdate() {
    Reqdata("/rd?ls=employ&user_id=" + g_focus.id, "", function (res) {
        g_employs = res;
        $("#employ").html(xremployshow(res.data));
    });
}

function onemployadd() {
    var dlg = new cbDlg("新建 证件", "width:600px");
    dlg.Add(`<form id="employ_live">` + xremploylive(Create(g_employs.fields), g_employs.fields) + `</form>`);
    dlg.Show();
    dlg.submit = function (thisdlg) {
        var fd = employcheck();
        if (fd == undefined)
            return;
        Sendform('/cr?ls=employ', fd, "", employupdate);
        thisdlg.closedlg();
    };
}
function onemployedit() {
    var idx = g_curitems["employ"];
    if (idx == undefined)
        return;
    var data_id = $("#employ").children(":nth-child(" + (int(idx) + 1) + ")").attr("data_id");
    var employ = GetSub(g_employs.data, "id", data_id);

    var dlg = new cbDlg("编辑 证件", "width:600px");
    dlg.btndel = true;
    dlg.Add(xremploylive(employ, g_employs.fields));
    dlg.Show();
    dlg.submit = function (thisdlg) {
        var fd = employcheck();
        if (fd == undefined)
            return;
        Sendform('/wt?ls=employ', fd, "", employupdate);
        thisdlg.closedlg();
    };
    dlg.remove = function (thisdlg) {
        Reqdata('/rm?ls=employ&id=' + employ.id, "", employupdate);
        thisdlg.closedlg();
    }
}
