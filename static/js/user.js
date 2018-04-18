//用户信息界面，用于用户内容显示和编辑，在初始化12345步，和用户详细信息处均有用到。
function xrusershow(user, fields) {
    var ui2 = `
                <div style="float:left;display:block;height:240px;width:280px;margin-top:5px;margin-left:10px;">
                    <div style="float:left;display:block;height:78px;width:78px;">
                        <img style="width:100%;height:100%;" {face}>
                    </div>
                    <div class="x2Form narrow">
                        <div style="margin-top:0px;"><label>帐号</label><div style="display:inline-block;">{account}</div></div>
                        <div><label>密码</label><div>******</div></div>
                    </div>
                    <div style="width:280px;height:160px;margin-top:5px">
                        <img style="width:100%;height:100%;" {idimg} >
                    </div>
                </div>`;

    return ui2.format({
        "account": user.account, face: (user.face == "" ? "" : 'src="' + user.face + '"'),
        idimg: (user.idimg == "" ? "" : 'src="' + user.idimg + '"')
    }) + RenderPane3(user, fields, ValToView);
}

function xruserlive(user, fields) {
    var ui2 = `
                <div style="float:left;display:block;height:240px;width:280px;margin-top:5px;margin-left:10px;">
                    <div style="float:left;display:block;">
                        <label class="imagelive" style="height:78px;width:78px;" for="face">
                            <img style="width:100%;height:100%;"  {face} >
                            <input type="file" id="face" name="face" accept="image/*">
                        </label>
                    </div>
                    <div class="x2Form narrow">
                        <div style="margin-top:0px;"><label>帐号</label><div style="display:inline-block;">{account}</div></div>
                        <div style="position:relative;">
                            <label>密码</label>
                            <div class="xCombox" style="border: 1px solid #95b7ff;">
                                <label style="color:royalblue;margin:0px;">点击修改</label>
                                <div class="xPopWnd" style="left: -6px; width: 200px; height: 115px; padding: 5px; display: none;">
                                    <label style="margin-right:5px;">旧密码</label><input name="pwd" type="password" style="width:140px;height:20px;">
                                    <label style="margin-right:5px;">新密码</label><input name="newpwd1" type="password" style="width:140px;height:20px;">
                                    <label style="margin-right:5px;">新密码</label><input name="newpwd2" type="password" style="width:140px;height:20px;">
                                    <div style="float:right"><input type="button" onclick="hidechgpwd(this)" value="确定"/> <input type="button" onclick="hidechgpwd(this)" value="取消" /></div>
                                </div>
                            </div>
                        </div>
                    </div><label class="imagelive" style="width:280px;height:160px;margin-top:5px" for="idimg">
                        <img style="width:100%;height:100%;" {idimg} >
                        <input type="file" id="idimg" name="idimg" accept="image/*">
                    </label>
                </div>`;

    return ui2.format({
        "account": user.account, face: (user.face == "" ? "" : 'src="' + user.face + '"'),
        idimg: (user.idimg == "" ? "" : 'src="' + user.idimg + '"')
    }) + RenderForm4(user, fields, function (user, field) {
        var name = field.name ? field.name : field;
        var val = user[name];
        if (field.name == "sex") return RenderSelect(db_sex, val);
        else if (field.name == "job") return RenderSelect(GetsubJob(g_user.job, "array"), val);
        else if (field.name == "ethnic") return RenderSelect(g_ethnic, val);
        else return user[name];
    });
}

function hidechgpwd(This) {
    if ($(This).attr("value") != "确定") {
        $(This).parent().parent().css("display", "none");
        return;
    }

    var formdata = new FormData(document.getElementById("form_useredit"));
    var pwd = formdata.get("pwd");
    var password1 = formdata.get("newpwd1");
    var password2 = formdata.get("newpwd2");
    if (password1 != password2) {
        alert("两次输入的密码不一致！");
        return;
    }

    var val = `{"id":"{id}","pwd":"{pwd}","newpwd":"{newpwd}"}`.format({
        "id": g_user.id, "pwd": pwd, "newpwd": password1
    });
    ReqdataP("/chgpwd", val, "修改密码", function (jsn) {
        if (jsn.result != 200) {
            alert(jsn.msg);
            return;
        }
        alert("修改成功！");
        $(This).parent().parent().css("display", "none");
    });
}

function onusersave(user) {
    delete g_chged.pwd;
    delete g_chged.newpwd1;
    delete g_chged.newpwd2;

    var formdata = new FormData(document.getElementById("form_useredit"));
    var fd = new FormData();
    for (var x in g_chged) {
        if (x == "face" || x == "idimg")
            fd.append(x, $("#" + x).get(0).files[0]);
        else
            fd.append(x, formdata.get(x));
    }

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            alert('保存成功' + xhr.responseText);
        }
    };
    xhr.open('POST', '/wt?ls=user&id=' + user.id, true);
    xhr.send(fd);
}

var g_chged = new Object();
$("html").on("change", function () {
    var node = event.target;
    if (node.tagName == "INPUT")
        g_chged[$(node).attr("name")] = true;
});

// 证件部分----------------------------------------begin----------------------
function xrcertiflive(entity, fields) {
    var ximg = { style: "float:left;display:inline-block;", body: xrimagelive2(entity.image, "image", "image") };
    var xform = { class: "x2Form", style: "display:inline-block; width:620px;", body: RenderFormIn(entity, fields) };
    return xCreateNode(ximg) + xCreateNode(xform);
}
function xrcertifshow(data) {
    var tpl = `{% it.forEach((x,i)=>{ %}
            <div class="listdata" data_id="{%=x.id%}" style="min-height: 85px;width: 100%; {% if (i%2==0) { %}background: #f5f5f5; {% } %}">
                <div class="xRndAngle" style="width: 126px; height: 84px; float: left; margin-right: 5px; ">
                    <img style="width: 126px; height: 84px;" src="{%=x.image%}" />
                </div>
                <div class="x2Form">
                    <div><label>证件名称</label><div>{%=x.name%}</div></div>
                    <div><label>证件编号</label><div>{%=x.code%}</div></div>
                    <div><label>颁发机构</label><div>{%=x.issue%}</div></div>
                    <div><label>颁发时间</label><div>{%=x.issuedate%}</div></div>
                </div>
            </div>
            {% }); %}`
    return dtpl(tpl)(data);
}

function certifcheck() {
    var formdata = new FormData(document.getElementById("certif_live"));
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
// 证件部分----------------------------------------end----------------------

// 教育经历----------------------------------------begin----------------------
function xredulive(entity, fields) {
    var ximg = { style: "float:left;display:inline-block;", body: xrimagelive2(entity.image1, "image1", "image1") + xrimagelive2(entity.image2, "image2", "image2") };
    var xform = { class: "x2Form", style: "display:inline-block; width:620px;", body: RenderFormIn(entity, fields) };
    return xCreateNode(ximg) + xCreateNode(xform);
}
function xredushow(data) {
    var tpl = `{% it.forEach((x,i)=>{ %}
            <div class="listdata" style="width: 100%; {% if (i%2==0) { %}background: #f5f5f5; {% } %}">
                <div style="display:inline-block; margin-right: 5px; width:250px;">
                    <img style="width: 120px; height: 80px;" src="{%=x.image1%}" />
                    <img style="width: 120px; height: 80px;" src="{%=x.image2%}" />
                </div>
                <div class="x2Form" style="display:inline-block">
                    <div><label>开始时间</label><div>{%=x.startdate%}</div></div>
                    <div><label>截止时间</label><div>{%=x.enddate%}</div></div>
                    <div><label>学历</label><div>{%=x.degree%}</div></div>
                    <div><label>教育机构</label><div>{%=x.issue%}</div></div>
                </div>
            </div>
            {% }); %}`
    return dtpl(tpl)(data);
}
function educheck() {
    var formdata = new FormData(document.getElementById("edu_live"));
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
// 教育经历----------------------------------------end----------------------

// 就业经历----------------------------------------begin----------------------
function xremploylive(entity, fields) {
    var ximg = { style: "float:left;display:inline-block;", body: xrimagelive2("", "image", "image") };
    var xform = { class: "x2Form", style: "display:inline-block; width:620px;", body: RenderFormIn(entity, fields) };
    var xbtns = `<div style="display:inline-block;height:20px;">
                <input type="button" onclick="onemploysave(this)" value="确定" />
                <input type="button" onclick="onemployblank(this)" value="清除" /></div>`

    var ss = xCreateNode(ximg) + xCreateNode(xform) + xbtns;
    return xCreateNode(ximg) + xCreateNode(xform) + xbtns;
}
function xremployshow(data) {
    var tpl = `{% it.forEach((x,i)=>{ %}
            <div style="min-height: 85px;width: 100%; {% if (i%2==0) { %}background: #f5f5f5; {% } %}">
                <div class="xRndAngle" style="width: 126px; height: 84px; float: left; margin-right: 5px; ">
                    <img style="width: 126px; height: 84px;" src="{%=x.image%}" />
                </div>
                <div class="x2Form">
                    <div><label>开始时间</label><div>{%=x.startdate%}</div></div>
                    <div><label>截止时间</label><div>{%=x.enddate%}</div></div>
                    <div><label>工作单位</label><div>{%=x.Organization%}</div></div>
                    <div><label>岗位</label><div>{%=x.position%}</div></div>
                </div>
            </div>
            {% }); %}`
    return dtpl(tpl)(data);
}
function onemploysave() {
    var formdata = new FormData(document.getElementById("employ_live"));
    if (formdata.get("name") == "") {
        alert("证件名称不能为空！");
        return;
    }
    if (formdata.get("issuedate") == "") {
        alert("颁发时间不能为空！");
        return;
    }
    if (formdata.get("issue") == "") {
        alert("颁发机构不能为空！");
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            Reqdata("/rd?ls=employ&user_id=" + g_user.id, "", function (ctf) {
                $("#employ_show").html(xremployshow(ctf.data));
                $("#employ_live").html(xremploylive(Create(g_ctf.fields), g_ctf.fields));
            });
        }
    };

    formdata.append("user_id", g_user.id);
    xhr.open('POST', '/cr?ls=employ', true);
    xhr.send(formdata);
}
function onemployblank() {
    $("#employ_live").html(xremploylive(Create(g_ctf.fields), g_ctf.fields));
}
// 就业经历----------------------------------------end----------------------