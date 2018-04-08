//用户信息界面，用于用户内容显示和编辑，在初始化12345步，和用户详细信息处均有用到。

function xruserform(user, fields) {
    var ui2 = `
                <div style="float:left;display:block;height:240px;width:280px;margin-top:5px;">
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
    }) + RenderForm4(g_user, fields, function (user, field) {
        var name = field.name ? field.name : field;
        var val = user[name];
        if (field.name == "sex") return RenderSelect(db_sex, val);
        else if (field.name == "job") return RenderSelect(GetsubJob(g_user.job, "array"), val);
        else if (field.name == "ethnic") return RenderSelect(g_ethnic, val);
        else return user[name];
    });
}
