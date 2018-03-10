function crd_showuserselectdlg() {
    var us = `<div id="rolelist" class="xCombox xRndAngle" style="margin-top:5px; display:inline-block;"><span>调度人员</span><div class="xMenu">
                <div class="selected">调度人员</div><div>风场人员</div><div>设备人员</div><div>仓库人员</div><div>专家</div><div>维修人员</div>
            </div></div>
            <div id="userfilter" class="xCombox xRndAngle" style="margin-top:5px; display:inline-block;">
                <span>所有</span><div id="userfiltertree" class="xMenu" style="max-height:600px;overflow-y:auto;"><div class="selected">调度人员</div></div>
            </div>
            <div id="filteruserlist" class="xRndAngle xScroll" style="margin-top:5px; width:590px;height:250px;padding:5px;"></div>`

    var dlg = new cbDlg("人员选择", "width:610px");
    dlg.Add(us);
    dlg.Show();
}
function crd_userwithface(user) {
    var tpl = dtpl(`<label><input type="checkbox"><div class="SmallHead"><img src="{%=it.face%}" />【{%=GetSub(db_job, "id",it.job).name%}】{%=it.name%}</div></label>`);
    return tpl(user);
}

//点在菜单项上
$("html").on("click", function () {
    var node = $(event.target);
    if (node.parent().hasClass("xMenu")) { //点在菜单背景上
        var parentid = node.parent().parent().attr("id");
        if (parentid == "rolelist") {
            var text = $(node).html();
            if (text == "调度人员") {
                $("#userfilter span").html('所有　　');
                $("#userfiltertree").addClass('xMenu');
                $("#userfiltertree").removeClass('xPopWnd');
                $("#userfiltertree").html('<div class="selected">所有　　</div>');
                Reqdata("/rduser?job=" + GetsubJob(GetSub(db_job, "name", "调度超级帐号").id, "string"), "", function (res) {
                    $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
                });
            }
            else if (text == "风场人员") {
                $("#userfilter span").html('　　　　　　');
                $("#userfiltertree").html('');
                $("#userfiltertree").addClass('xPopWnd');
                $("#userfiltertree").removeClass('xMenu');
                $("#filteruserlist").html("");
                g.userfiltertree = new x4Tree("#userfiltertree", "winderco", "", "winder", function (type, id, node) {
                    if (type == "winder") {
                        $("#userfilter>span").html(node.html());
                        $("#userfilter .xPopWnd").toggle();
                        Reqdata("/rduser?depart_id=" + id + "&depart_table=" + GetTbl("winder").id, "", function (res) {
                            $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
                        });
                    }
                    else {
                        g.userfiltertree.Extend("#" + type + "_" + id);
                    }
                });
            }
            else if ($(node).html() == "设备人员") {
                $("#userfilter span").html('　　　　　　');
                $("#userfiltertree").addClass('xPopWnd');
                $("#userfiltertree").removeClass('xMenu');
                $("#userfiltertree").html('');
                $("#filteruserlist").html('');
                g.userfiltertree = new x4Tree("#userfiltertree", "devwh", "", "devwh", function (type, id, node) {
                    if (type == "devwh") {
                        $("#userfilter>span").html(node.html());
                        $("#userfilter .xPopWnd").toggle();
                        Reqdata("/rduser?depart_id=" + id + "&depart_table=" + GetTbl("devwh").id, "", function (res) {
                            $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
                        });
                    }
                    else {
                        g.userfiltertree.Extend("#" + type + "_" + id);
                    }
                });
            }
            else if ($(node).html() == "仓库人员") {
                $("#userfilter span").html('　　　　　　');
                $("#userfiltertree").addClass('xPopWnd');
                $("#userfiltertree").removeClass('xMenu');
                $("#userfiltertree").html('');
                $("#filteruserlist").html('');
                g.userfiltertree = new x4Tree("#userfiltertree", "matprov", "", "matwh", function (type, id, node) {
                    if (type == "matwh") {
                        $("#userfilter>span").html(node.html());
                        $("#userfilter .xPopWnd").toggle();
                        Reqdata("/rduser?depart_id=" + id + "&depart_table=" + GetTbl("matwh").id, "", function (res) {
                            var tt = res.data.map(x => crd_userwithface(x));
                            $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
                        });
                    }
                    else {
                        g.userfiltertree.Extend("#" + type + "_" + id);
                    }
                });
            }
            else if ($(node).html() == "专家") {
                $("#userfilter span").html('所有　　　　');
                $("#userfiltertree").addClass('xMenu');
                $("#userfiltertree").removeClass('xPopWnd');
                $("#userfiltertree").html('<div id="user_0">所有</div>' + xrmenuin(db_skill, "skill_"));
                Reqdata("/rduser?job=" + GetSub(db_job, "name", "专家").id, "", function (res) {
                    $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
                });
            }
            else if ($(node).html() == "维修人员") {
                $("#userfilter span").html('所有　　　　');
                $("#userfiltertree").addClass('xMenu');
                $("#userfiltertree").removeClass('xPopWnd');
                Reqdata("/rduser?job=" + GetSub(db_job, "name", "维修队长").id, "", function (res) {
                    $("#userfiltertree").html('<div id="user_0">所有</div>' + xrmenuin(res.data, "user_"));
                });
                Reqdata("/rduser?job=" + GetsubJob(GetSub(db_job, "name", "技工超级帐号").id, "string"), "", function (res) {
                    $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
                });
            }
        }
        else if (parentid == "userfilter") {
            var role = $("#rolelist span").html();
            if (role == "专家") {
                Reqdata("/rduser?job=" + GetSub(db_job, "name", "专家").id, "", function (res) {
                    var skill = node.html();
                    $("#filteruserlist").html(res.data.fmap(x => {
                        if (skill == "所有" || x.skill.indexOf(node.html()) != -1)
                            return crd_userwithface(x);
                    }));
                });
            }
            else if (role == "维修人员") {
                if (node.html() != "所有") {
                    Reqdata("/rdteam?user_id=" + node.attr("id").split("_")[1], "", function (res) {
                        $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
                    });
                }
                else {
                    Reqdata("/rduser?job=" + GetsubJob(GetSub(db_job, "name", "技工超级帐号").id, "string"), "", function (res) {
                        $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
                    });
                }
            }
        }
    }
});

