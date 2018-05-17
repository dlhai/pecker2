var db_board = [
    { "id": "1", "name": "新闻" },
    { "id": "2", "name": "博客" },
    { "id": "3", "name": "文库" },
]
var db_label = ["牛仔装","牛仔裤","牛仔服","耳环","帽厂","中国印染","电熨斗",
    "旗袍","棉纺织品","毛皮","衬衣","男女皮鞋","鸭绒枕","被褥","芭蕾舞衣",
    "长统袜","毛纺织业","真丝服装","罗口手套","手套","裤袜","印染棉布","中国丝绸"]

function f_follow(This, user_id) {
	if ( $(This).attr("value")=="关注他"){
		Reqdata("/follow?user_id=" + user_id, "", function (res) {
			if (res.result=="200")
				$(This).attr("value","取消关注");
			else
				alert(res.msg);
		});
	}
	else{
		Reqdata("/leave?user_id=" + user_id, "", function (res) {
			if (res.result=="200")
				$(This).attr("value","关注他");
			else
				alert(res.msg);
		});
	}
}

function f_praise(writing_id,type ) {
	Reqdata("/praise?writing_id=" + writing_id +"&type="+type, "", function (res) {
        if (res.result == "200") {
            classpraise = (type == 1 ? 'class="me"' : "");
            classblame = (type == -1 ? 'class="me"' : "");
			html=`<div {classpraise} onclick="f_praise({writing_id},1)"><img src="kindedit/plugins/emoticons/images/79.gif"><div>{praise}</div></div>
			<div {classblame} onclick="f_praise({writing_id},-1)"><img src="kindedit/plugins/emoticons/images/80.gif"><div>{blame}</div></div>`;
            $(".praise").html(html.format({classpraise:classpraise,classblame:classblame,
                writing_id:writing_id,praise:res.praise,blame:res.blame}));
		}
		else
			alert(res.msg);
	});
}

function f_message(user_id,user_name) {
	var dlg = new cbDlg("留言给 "+$("#user_name").html(),"width:670px");
	dlg.Add(`<textarea id="kemsg" style="width:100%;height:300px;"></textarea>`);
	dlg.Show();
	kemsg = KindEditor.create('#kemsg', { uploadJson: '/cr', items:[ 'selectall', 'cut', 'copy', 'paste','undo', 'redo', '|',
		'formatblock', 'fontname', 'fontsize', 'forecolor', 'hilitecolor', 'bold','italic', 'underline', 'strikethrough',
		'lineheight', 'removeformat', '|',  'justifyleft', 'justifycenter', 'justifyright','justifyfull', 'insertorderedlist', 
		'insertunorderedlist', 'indent', 'outdent', '|', 'link', 'unlink', '|', 'fullscreen',]});
    dlg.submit = function (thisdlg) {
		kereplay.sync();
        var value_content = $("#kemsg").val();
        thisdlg.closedlg();
    };
}


function f_replay(writing_id) {
    kereplay.sync();//将KindEditor的数据同步到textarea标签。
    var value_content = $("#kereplay").val();
	ReqdataP("/publish?board=4&writing_id=" + writing_id, value_content, "", function (res) {
		location.reload();
	});
}

function f_writing() {
    var board = db_board.map(x => '<input id="'+x.id+'" type="radio" value="' + x.name + '">').join("");
    var label = db_label.map(x => '<input type="check" value="' + x + '">').join("");

    var dlg = new cbDlg("发表文章","width:900px");
    var content = `<form class="kewriting">
		<div><label>标题</label><input id="courier" /></div>
		<div><label>分类</label>`+ board+`</div>
		<div><label>标签</label>`+ label+`</div>
		<div><label>正文</label><textarea id="kewriting" style="width:100%;height:400px;"></textarea></div>
		</form>`
	dlg.Add(content);
	dlg.Show();
    kemsg = KindEditor.create('#kewriting', { uploadJson: '/cr', items:[ 'selectall', 'cut', 'copy', 'paste','undo', 'redo', '|',
		'formatblock', 'fontname', 'fontsize', 'forecolor', 'hilitecolor', 'bold','italic', 'underline', 'strikethrough',
		'lineheight', 'removeformat', '|',  'justifyleft', 'justifycenter', 'justifyright','justifyfull', 'insertorderedlist', 
		'insertunorderedlist', 'indent', 'outdent', '|', 'link', 'unlink', '|', 'fullscreen',]});
    dlg.submit = function (thisdlg) {
		kereplay.sync();
        var value_content = $("#kewriting").val();
        thisdlg.closedlg();
    };
}

