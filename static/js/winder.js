function tpl(wr, chk){
	var r = ""
	+ ((wr== true )? '<div id="efan_{%=it.id%}" class="xEFanPanel">':"")
    + '    <header>'
	+ ((chk== true )? '<input data_id="{%=it.id%}" type="checkbox" style="margin-top:0px;">':"")
    //+ '          <img src="img/diy/3.png" style="vertical-align:top;"/>'
    + '          <strong>编号:</strong><span>{%=it.code%}</span>'
    + '          <strong>型号:</strong><span>{%=it.type%}</span>'
    + '          <strong>生产厂家:</strong><span>{%=f2s(it,"efanvender_id")%}</span>'
    + '          <div style="float: right;">'
    + '              <a onClick="onEditEfan({%=it.id%})">编辑</a>'
    + '          </div>'
    + '      </header>'
    + '      <table>'
    + '          <thead><tr><th>编号</th><th>主要材料</th><th>出厂时间</th><th>挂机时间</th><th>生产厂家</th></tr></thead>'
    + '          <tbody>'
    + '              {% it.leafs.forEach(leaf=> { %}'
    + '              <tr>'
    + '                  <td>{%=leaf.code%}</td>'
    + '                  <td>{%=leaf.mat%}</td>'
    + '                  <td>{%=leaf.producedate%}</td>'
    + '                  <td>{%=leaf.putondate%}</td>'
    + '                  <td>{%=f2s(leaf,"leafvender_id")%}</td>'
    + '              </tr>'
    + '              {% }); %}'
    + '          </tbody>'
    + '      </table>'
    + ((wr== true )? '  </div>':"");
	return r;
}

var tplEfanPane = doT.template(tpl(true,false));
var tplEfanPaneIn = doT.template(tpl(false,false));
var tplEfanCheckPane = doT.template(tpl(true,true));
var tplEfanCheckPaneIn = doT.template(tpl(false,true));

var tplEfanForm = doT.template(
        '<header>'
		+ `    <input type="hidden" name="winderarea_id" value="{%=it.winderarea_id%}">`
		+ `    <input type="hidden" name="winder_id" value="{%=it.winder_id%}">`
        + '    <strong>编号:</strong><input name="code" value="{%=it.code%}" />'
        + '    <strong>型号:</strong><input name="type" value="{%=it.type%}" />'
    + '   <strong>生产厂家:</strong><select name="vender_id" style="margin-right:0px;width:100px;">{%=f2e(it,"efanvender_id")%}</select>'
        + '</header>'
        + '<table>'
        + '    <thead><tr><th>编号</th><th>主要材料</th><th>出厂时间</th><th>挂机时间</th><th style="width:90px">生产厂家</th></tr></thead>'
        + '    <tbody>'
        + '        {% for (var i = 0; i < it.leafs.length; i++) { %}'
        + '        <tr>'
		+ `            <input type="hidden" name="{%=i%}id" value="{%=it.leafs[i].id%}">`
		+ `            <input type="hidden" name="{%=i%}winderarea_id" value="{%=it.winderarea_id%}">`
		+ `            <input type="hidden" name="{%=i%}winder_id" value="{%=it.winder_id%}">`
        + '            <td><input name="{%=i%}code" value="{%=it.leafs[i].code%}" /></td>'
        + '            <td><input name="{%=i%}mat" value="{%=it.leafs[i].mat%}" /></td>'
        + '            <td><input name="{%=i%}producedate" value="{%=it.leafs[i].producedate%}" onClick="xrlaydate(this)" /></td>'
        + '            <td><input name="{%=i%}putondate" value="{%=it.leafs[i].putondate%}" onClick="xrlaydate(this)" /></td>'
        + '            <td><select name="{%=i%}vender_id" >{%=f2e(it.leafs[i],"leafvender_id")%}</select></td>'
        + '        </tr>'
        + '        {% } %}'
        + '    </tbody>'
        + '</table>');

function f2s(u, field) {
    var fn = field;
    if (typeof field != "string")
        fn = field.name;
    if (fn == "winderco_id" || fn == "winderprov_id" || fn == "winder_id") {
        return $("#" + fn.split("_")[0] + "_" + u[fn]).children("span").text();
    }
    else if (fn == "leafvender_id")
        return u["vender_id"]=="" ? "": GetSub(g_leafvenders.data, "id", u["vender_id"]).name;
    else if (fn == "efanvender_id")
        return u["vender_id"]=="" ? "": GetSub(g_efanvenders.data, "id", u["vender_id"]).name;
    return u[fn];
};

function f2e(u, field) {
    var fn = field;
    if (typeof field != "string")
        fn = field.name;
    if (fn == "winderco_id" || fn == "winderprov_id" || fn == "winder_id") {
        return $("#" + fn.split("_")[0] + "_" + u[fn]).children("span").text();
    }
    else if (fn == "leafvender_id") 
        return RenderSelect(g_leafvenders.data, u["vender_id"]);
    else if (fn == "efanvender_id")
        return RenderSelect(g_efanvenders.data, u["vender_id"]);
    return u[fn];
};

function onEditEfan(id) {
	var title = "编辑风电机";
    var idx = GetIdx(g_focussubs.data, "id", id);
	var cnt = tplEfanForm(g_focussubs.data[idx]);

	var dlg = new cbFormDlg(title, "width:610px", cnt);
	dlg.urlsubmit = "/winder/efanmodify?id="+g_focussubs.data[idx].id;
	dlg.urlremove = "/winder/efanremove?id="+g_focussubs.data[idx].id;
	dlg.closing = function (reason){
		if ( reason == "remove"){
			$("#efan_"+id).remove();
		}
        else if (reason == "submit") {
			g_focussubs.data[idx]=dlg.res.data[0];
			$("#efan_"+id).html(tplEfanPaneIn(dlg.res.data[0]));
		}
	}
    dlg.Show("xEFanForm");
}
