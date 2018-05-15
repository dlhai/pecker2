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

function f_message(user_id) {

}


function f_replay(writing_id) {

}

function f_writing() {

}

