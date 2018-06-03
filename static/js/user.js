//共用函数
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

    return ui2.format({"account": user.account, face: (user.face == "" ? "" : 'src="' + user.face + '"'),
            idimg: (user.idimg == "" ? "" : 'src="' + user.idimg + '"')})
        + RenderPane3(user, fields, ValToView);
}

function ValToView(user, field) {
    var name = field.name ? field.name : field;
    if (name == "sex") return GetSub(db_sex, "id", user.sex).name;
    else if (name == "job") return GetSub(db_job, "id", user.job).name;
    else if (name == "depart_id") return GetSub(g_departs.data, "id", user.depart_id).name;
    else return user[name];
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

function ondlgusersave(dlg) {
    onusersave(dlg.user);
}

function onusersave(user) {
    delete g_chged.pwd;
    delete g_chged.newpwd1;
    delete g_chged.newpwd2;

    var formdata = new FormData(document.getElementById("form_useredit"));
	if ( formdata.get("name")=="" ){
		alert("姓名不能为空");
		return;
	}

    var fd = new FormData();
	var count = 0;
    for (var x in g_chged) {
        if (x == "face" || x == "idimg")
            fd.append(x, $("#" + x).get(0).files[0]);
        else
            fd.append(x, formdata.get(x));
		count++;
    }
    for (var x in g_datechged){
		fd.append(x, formdata.get(x));
		count++;
	}
	if ( count == 0)
		return;

	g_chged = new Object();
	g_datechged = new Object();

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
    if (node.tagName == "INPUT" || node.tagName == "SELECT"){
		var name=$(node).attr("name");
        g_chged[name] = true;
	}
});

//专用函数
function onuseradd() {
    var tpl =
        `<div class="x2Form" style="padding: 0px 0px 0px 30px;">
                        <div style="float: left; margin:0px;"><img style="width: 100px;height: 180px;" src="img/bird.jpg" /></div>
                        <div><label>帐号</label><input id="username" /></div>
                        <div><label>密码</label><input id="pwd1" type="password"/></div>
                        <div><label>密码</label><input id="pwd2" type="password"/></div>
                    </div>`;

    var dlg = new cbDlg("新建 用户", "", tpl);
    dlg.submit = function () {
        var newuser = Create(g_user.fields);
        newuser.account = $("#username").val();
        newuser.pwd = $("#pwd1").val();
        var pwd2 = $("#pwd2").val();
        if (newuser.account == "") { alert("帐号不能为空"); return; }
        if (newuser.pwd != pwd2) { alert("两次输入的密码不一致"); return; }
        if (newuser.pwd == "") { alert("密码不能为空"); return; }

        var val = `{"ls":"user","val":{"account":"{account}","pwd":"{pwd}"}}`.format({
            "account": newuser.account, "pwd": newuser.pwd
        });
        ReqdataP('/cr', val, "", function (res) {
            if (res.result != 200) { alert("新建失败！"); return; }
            newuser.id = res.id;
            dlg.closedlg();
        });

        newuser.depart_id = g_user.depart_id;
        newuser.depart_table = g_user.depart_table;
        var dlg2 = new cbDlg("新建 用户", "width:900px");
        dlg2.Add(`<form id="form_useredit" style="height:350px;">` + xruserlive(newuser, g_user.fields) + `</form>`);
        dlg2.Show();
		dlg2.user = newuser;
        dlg2.submit = ondlgusersave;
    }
    dlg.Show();
}
function onuseredit() {
    var dlg = new cbDlg("编辑 用户", "width:900px");
    dlg.btndel = true;
	dlg.Add(`<form id="form_useredit" style="height:350px;">` + xruserlive(g_focus, g_user.fields) + `</form>`);
    dlg.Show();
	dlg.user = g_focus;
    dlg.submit = ondlgusersave;
	dlg.remove = function (dlg){ 
		Reqdata( "/user/remove?id="+dlg.user.id, "", function(res){
            if (res.result != 200) { alert("删除失败！"); return; }
            dlg.closedlg();
		});
	};
}

