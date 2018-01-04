//表格点击反色 
function TableBindClick() {
    var tbc_currow = -1;
    $("tr").click(function () {
        var tag = $(this).parent()[0].localName;
        if (tag.toLowerCase() == "thead")
            return;
        if (tbc_currow != -1) {
            tbc_currow++;
            if (tbc_currow % 2 == 0)
                $(this).parent().children(":nth-child(" + tbc_currow + ")").children().css("background-color", "#f5f5f5");
            else
                $(this).parent().children(":nth-child(" + tbc_currow + ")").children().css("background-color", "#ffffff");
        }
        tbc_currow = $(this).index();
        $(this).children().css("background-color", "#00f0f5");
    });
}

//文档控件
$(function () {
    $(".x3Doc>.x3Doc-handle").on("click", function ()
    {
        $(this).siblings(".x3Doc-menu").css("display", "block");
        $(this).siblings(".x3Doc-menu").addClass("x3Doc-click");
    });

    window.onclick = x3DocMenuHide;
    function x3DocMenuHide() {
        $(".x3Doc-menu:not(.x3Doc-click)").css("display", "none");
        $(".x3Doc>.x3Doc-click").removeClass("x3Doc-click");
    }
});

function RenderTable2(it, style) {
    var r = "<table class=\"xTable\"><thead><tr>";
    if (style)
        r = "<table class=\""+style+"\"><thead><tr>";
    for (var c in it.fields) {
        if (it.fields[c].twidth) {
            if (parseInt(it.fields[c].twidth) > 0)
                r += "<th width=\"" + it.fields[c].twidth + "\">" + it.fields[c].title + "</th>";
        }
        else
            r += "<th>" + it.fields[c].title + "</th>";
    }
    r += "</tr></thead>\n";

    r += "<tbody>";
    for (var x in it.data) {
        r += "<tr>";
        for (c in it.fields) {
            if (!it.fields[c].twidth || it.fields[c].twidth && parseInt(it.fields[c].twidth) > 0) {
                if (it.fields[c].tstyle)
                    r += "<td style=\"" + it.fields[c].tstyle + "\">" + it.data[x][it.fields[c].name] + "</td>";
                else
                    r += "<td>" + it.data[x][it.fields[c].name] + "</td>";
            }
        }
        r += "</tr>";
    }
    r += "</tbody></table>";
    return r;
}

function RenderForm3(ar, idx) {
    var r = "";
    for (var i = 0; i < ar.fields.length; x++) {
        r += "<div><label>" + ar.fields[i].title + "</label>";
        if (ar.fields[i].ftype == "div")
            r += "<div>"+ar.data[idx][ar.fields[i].name] + "</div>";
        else if (ar.fields[i].ftype == "input")
            r += '<input name="' + ar.fields[i].name+'" value="'+ ar.data[idx][ar.fields[i].name] + '"/>';
        else if (ar.fields[i].ftype == "input_long")
            r += '<input style="width:500px;" name="' + ar.fields[i].name + '" value="' + ar.data[idx][ar.fields[i].name] + '" />';
        else if (ar.fields[i].ftype == "textarea")
            r += '<textarea style="resize:none;width:500px;max-height:45px;" name="' + ar.fields[i].name + '>' + ar.data[idx][ar.fields[i].name] + '"</textarea>';
        else if (ar.fields[i].ftype == "select")
            r += '<select id="' + ar.fields[i].name+'" name="' + ar.fields[i].name + '>' + ar.data[idx][ar.fields[i].name] + '"</select>';
        r += "</div>";
    }
    return r;
}

function RenderPane(ar, idx){
    var r = "";
    for (var i = 0; i < ar.fields.length; x++) {
        var attr = "";
        if (ar.fields[i].name.find("_") != -1)
            attr = 'id="' + ar.fields[i].name + "_" + ar.data[idx][ar.fields[i].name] + '" ';

        if (ar.fields[i].ftype == "input_long")
            attr += 'style="width:500px;"';
        else if (ar.fields[i].ftype == "textarea")
            attr += 'style="overflow-y: scroll;width:500px;max-height:45px;"';

        r += "<div><label>" + ar.fields[i].title + "</label><div " + attr + ">"
            + ar.data[idx][ar.fields[i].name] + "</div></div>";
    }
    return r;
}

function ID2Name(ar, idx) {
    var param = [];
    for (var i in ar.fields)
        if (ar.fields[i].name.find("_") != -1 )
            param[ar.fields[i].name] = ar.data[idx][ar.fields[i].name];
    if (param.length == 0)
        return;

    Request("/id2name?" + param.join("&"), function (d) {
        if (d.result != "ok")
            return;
        for (var j in d)
            if (j != "result")
                $(j).html(d[j]);
    });
}

function fillselect(ar, idx) {
    var param = [];
    for (var i in ar.fields)
        if (ar.fields[i].ftype == "select")
            Request("/id2name?" + param.join("&"), function (d) {
    if (param.length == 0)
        return;

    Request("/id2name?" + param.join("&"), function (d) {
        if (d.result != "ok")
            return;
        for (var j in d)
            if (j != "result")
                $(j).html(d[j]);
    });
}

function Request(url, fun) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", url, true);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            jdata = $.parseJSON(xmlhttp.responseText);
            fun(jdata);
        }
    };
    xmlhttp.send();
}

function RenderForm2(ar, i) {
    alert("使用了旧接口：RenderForm2已被RenderPane");
    return "";
    //var r = "";
    //for (var x = 0; x < ar.fields.length; x++) {
    //    if (ar.fields[x].ftype == "bigtext")
    //        r += "<div class=\"xFormItem\"><label>" + ar.fields[x].title + "</label><div style=\"overflow-y: scroll;width:500px;max-height:45px;\">"
    //            + ar.data[i][ar.fields[x].name] + "</div></div>"
    //    else if (ar.fields[x].ftype == "image")
    //        r += "<div class=\"xImgSFZ\"><img src=\"" + ar.data[i][ar.fields[x].name] + "\"/></div>";
    //    else
    //        r += "<div class=\"xFormItem\"><label>" + ar.fields[x].title + "</label><div>" + ar.data[i][ar.fields[x].name] + "</div></div>"
    //}
    //return r;
}

