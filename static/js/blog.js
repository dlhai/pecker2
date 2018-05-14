function f_follow(This, user_id) {
    alert("haha!");
    Reqdata("/follow?user_id=" + user_id, "", function (res) {
        if (res.result=="200")
            $(This).attr("value","取消关注");
        else
            alert(res.msg);
    });
}

function f_leave(user_id ){

}

function f_message(user_id) {

}

function f_praise(writing_id ) {

}

function f_blame(writing_id) {

}

function f_replay(writing_id) {

}

function f_writing() {

}

