// 案件界面，用于调度、专家、风场场主、驻场、队长等，当前仅含案件编辑功能的内容，后面会加入案件显示的内容。
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

var ud_filter={"role":"","filter":""};
function ud_userdlg( filter1, filter2) {
	ud_filter = {"role":filter1,"filter":filter2};
    var us = 
			`<div id="rolelist" class="xCombox xRndAngle" style="margin-top:5px; display:inline-block;">
				<span></span>
				<div class="xMenu"></div>
			</div>
            <div id="userfilter" class="xCombox xRndAngle" style="margin-top:5px; display:inline-block;">
                <span></span>
				<div id="userfiltertree" class="xMenu" style="max-height:600px;overflow-y:auto;">
				</div>
            </div>
            <div id="filteruserlist" class="xRndAngle xScroll" style="margin-top:5px; width:590px;height:250px;padding:5px;"></div>`
    var dlg = new cbDlg("人员选择", "width:610px");
    dlg.Add(us);
    dlg.Show();

	var roles = filter1 != "" ? filter: ["调度人员","风场人员","设备人员","仓库人员","专家","维修队"];
	ud_cbx("rolelist",roles, "调度人员" );
	onclkrole(default);
}

function ud_cbx(id, items, default ) {
	$("#id span").html(default);
	$("#id div").html(items.map(x=>"<div>"+x+"</div>").join(""));
}

//点在菜单项上
$("html").on("click", function (event) {
    var node = $(event.target);
    if (node.parent().hasClass("xMenu")) { //点在菜单背景上
        var parentid = node.parent().parent().attr("id");
        if (parentid == "rolelist") {
           onclkrole($(node).html());
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
            else if (role == "维修队") {
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



function crd_userwithface(user) {
    var tpl = dtpl(`<label style="margin-right:10px;font-weight:normal;"><input type="checkbox"><div class="brief"><img src="{%=it.face%}" />【{%=GetSub(db_job, "id",it.job).name%}】{%=it.name%}</div></label>`);
    return tpl(user);
}

function onclkrole(text, filter){
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
    else if (text == "设备人员") {
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
    else if (text == "仓库人员") {
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
    else if (text == "专家") {
        $("#userfilter span").html('所有　　　　');
        $("#userfiltertree").addClass('xMenu');
        $("#userfiltertree").removeClass('xPopWnd');
        $("#userfiltertree").html('<div id="user_0">所有</div>' + xrmenuin(db_skill, "skill_"));
        Reqdata("/rduser?job=" + GetSub(db_job, "name", "专家").id, "", function (res) {
            $("#filteruserlist").html(res.data.map(x => crd_userwithface(x)));
        });
    }
    else if (text == "维修队") {
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

