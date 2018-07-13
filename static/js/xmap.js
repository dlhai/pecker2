// UpdateCurData中的 SaveData 需要先定义
// ShowWindow中的 FieldToShow 需要先定义

// 更新当前对象
function UpdateCurData(type, data) {
    if (typeof g_curdata == "undefined"){
        g_curdata = { "type": type, "data": data };
        return;
    }
    if (type == "undefine") {
        if (g_curdata.type == "winderarea")
            g_curdata.data.plg.disableEditing();
        SaveData(g_curdata);
        return;
    }
    if (g_curdata.type == type && g_curdata.data.id == data.id)
        return;

    if (g_curdata.type == "winderarea")
        g_curdata.data.plg.disableEditing();

    SaveData(g_curdata);
    g_curdata = { "type": type, "data": data };
}

function SaveData(curdata) {
    if (curdata.type == undefined)
        return;
    if (curdata.type == "winderarea")
        position = curdata.data.plg.getPath();
    else
        position = [curdata.data.mk.getPosition()];

    var val = `{"ls":"{ls}","id":"{id}","val":{"position":"{position}"}}`.format({
        "ls": curdata.type, "id": curdata.data.id,
        "position": position.map(x => x.lng + " " + x.lat).join(",")
    });
    console.log(val);
    ReqdataP("/wt?ls=" + curdata.type, val);
}

function IsCurData(type, data) {
    if (typeof g_curdata == "undefined" && type == "undefine")
        return true;

    if (typeof g_curdata == "undefined") 
        return false;
    if (type == "undefine")
        return false;

    if (g_curdata.type == type && g_curdata.data.id == data.id)
        return true;
}

function CreateMap( id ) {
    g_map = new BMap.Map(id);
    g_map.centerAndZoom(new BMap.Point(116.404, 39.915), 6); //设置中心点坐标和地图级别
    g_map.addControl(new BMap.ScaleControl({ anchor: BMAP_ANCHOR_BOTTOM_RIGHT })); // 左下角，添加比例尺
    g_map.addControl(new BMap.NavigationControl({ anchor: BMAP_ANCHOR_TOP_RIGHT })); //左上角，添加默认缩放平移控件
    g_map.enableScrollWheelZoom();//开启鼠标滚轮缩放
    return g_map;
}

function CreateMark(iconname, data, type, fields, cbclick) {
    var marker = new BMap.Marker(CreatePoint(data.position), { icon: GetIcon(iconname) });
    var label = new BMap.Label("name" in data ? data.name : data.code, { offset: new BMap.Size(-10, 32) });
    label.setStyle({ border: "0px", color: "blue" });
    marker.setLabel(label);
    g_map.addOverlay(marker);
    data.mk = marker;
    marker.addEventListener("dragend", function (map_type, target, pixel, point) { UpdateCurData(type, data); });
    marker.addEventListener("click", function (e) { cbclick != undefined ? cbclick(type, data, fields, e) : ShowWindow(type, data, fields, e); });
    label.addEventListener("click", function (e) { cbclick != undefined ? cbclick(type, data, fields, e) : ShowWindow(type, data, fields, e); });
}

// 与CreateMark区别：
// 使用data.face作为地图上显示的图标，有的对象没有face属性，因此CreateMark不能被代替
function CreateMark2(data, type, fields, cbclick) {
    var marker = new BMap.Marker(CreatePoint(data.position), { icon: GetIcon(data.face) });
    var label = new BMap.Label("name" in data ? data.name : data.code, { offset: new BMap.Size(-10, 32) });
    label.setStyle({ border: "0px", color: "blue" });
    marker.setLabel(label);
    g_map.addOverlay(marker);
    data.mk = marker;
    marker.addEventListener("dragend", function (map_type, target, pixel, point) { UpdateCurData(type, data); });
    marker.addEventListener("click", function (e) { cbclick != undefined ? cbclick(type, data, fields, e) : ShowWindow(type, data, fields, e); });
    label.addEventListener("click", function (e) { cbclick != undefined ? cbclick(type, data, fields, e) : ShowWindow(type, data, fields, e); });
}

function CreateArea(area, cbclick) {
    area.plg = CreatePolygon(area.position);
    g_map.addOverlay(area.plg);
    area.lbl = CreateAreaLabel(area);
    g_map.addOverlay(area);
    area.plg.addEventListener("click", function (type, target, point, pixel) { cbclick(type, target, point, pixel,area); });
    area.plg.addEventListener("lineupdate", function (type, target) {
       // filterpoint(area.plg.getPath());
        area.lbl.setPosition(CalCenter(area.plg.getPath()));
    });
}

function filterpoint(ar) {
    if (ar.length <= 3)
        return false;
}

function GetIcon(iconname) {
    icons = new Object();
    if (!(iconname in icons)) {
		if ( -1 == iconname.indexOf( "/" ))
		{	//使用默认图标
			var name = "/static/img/" + iconname + ".png";
			icons[iconname] = new BMap.Icon(name, new BMap.Size(32, 32));
			icons[iconname].imageSize = new BMap.Size(32, 32);
		}
		else
		{	//使用自带图标
			icons[iconname] = new BMap.Icon(iconname, new BMap.Size(32, 32));
			icons[iconname].imageSize = new BMap.Size(32, 32);
		}
    }
    return icons[iconname];
}

var g_usecenter = 0;
function CreatePoint(pos) {
	if ( pos == undefined || pos == "" ){
		g_usecenter +=1;
		return g_map.getCenter();
	}
    var ar = pos.split(" ");
    return new BMap.Point(parseFloat(ar[0]), parseFloat(ar[1]));
}

function CreatePolygon(pos) {
    var ar = pos.split(",").map(x => CreatePoint(x));
    return new BMap.Polygon(ar, { strokeColor: "Chocolate", strokeWeight: 2, strokeOpacity: 0.5 });
}

function points2str( ar ) {
    return ar.map(x => x.lnt + " " + x.lat).join(",");
}

// 计算中心点位置
function CalCenter(path) {
    var lng = 0, lat = 0;
    path.forEach(pt=>{
        lng += pt.lng;
        lat += pt.lat;
    });
    return new BMap.Point(lng / path.length, lat / path.length);
}
function CreateAreaLabel(area) {
    var opts = {
        position: CalCenter(area.plg.getPath()),
        offset: new BMap.Size(-6 * area.name.length, -6)    //设置文本偏移量
    }
    var label = new BMap.Label(area.name, opts);  // 创建文本标注对象
    label.setStyle({
        border: "0px",
        color: "Chocolate",
        fontSize: "12px",
        height: "20px",
        lineHeight: "20px",
        fontFamily: "微软雅黑"
    });
    g_map.addOverlay(label);
    return label;
}


function ShowWindow(type, data, fields, e) {
    var p = e.target;
    var point = new BMap.Point(p.getPosition().lng, p.getPosition().lat);
    var content = '<div class="xRndAngle x2Form" style="overflow-y: scroll;height:290px;padding:5px 0px">' + RenderPane2(data, fields, FieldToShow) + '</div>';
    var infoWindow = new BMap.InfoWindow(content, {
        width: 619,     // 信息窗口宽度
        title: GetTbl(type).title + " 信息", // 信息窗口标题
        enableMessage: true//设置允许信息窗发送短息
    });  // 创建信息窗口对象 
    g_map.openInfoWindow(infoWindow, point); //开启信息窗口
}

//-----------------ModeControl begin------------------------------------------------
// 定义模式控件,即function
function ModeControl( x,y, onmodechange) {
    var x = arguments[0] ? arguments[0] : 10;
    var y = arguments[1] ? arguments[1] : 10;

    // 默认停靠位置和偏移量
    this.defaultAnchor = BMAP_ANCHOR_TOP_LEFT;
    this.defaultOffset = new BMap.Size(x,y);
    this.onmodechange = onmodechange;
    this.editmode = false;
}
// 通过JavaScript的prototype属性继承于BMap.Control
ModeControl.prototype = new BMap.Control();
// 自定义控件必须实现自己的initialize方法,并且将控件的DOM元素返回
// 在本方法中创建个div元素作为控件的容器,并将其添加到地图容器中
ModeControl.prototype.initialize = function (map) {
    // 创建一个DOM元素
    var div = document.createElement("div");
    div.innerHTML = '浏览';
    div.style.backgroundColor = "white";
    div.style.border = "1px solid lavender";
    div.style.boxShadow = "1px 1px 1px rgba(0,0,0,.1)";
    div.style.padding = "5px 10px";
    $(div).addClass("xRndAngle");
    $(div).on("click", "", { This: this}, function (ev) {
        ev.data.This.editmode = !ev.data.This.editmode;
        div.innerHTML = ev.data.This.editmode ? '编辑' : '浏览';
        ev.data.This.onmodechange(ev.data.This.editmode);
    });

    // 添加DOM元素到地图中
    g_map.getContainer().appendChild(div);
    // 将DOM元素返回
    return div;
}
// -----------------ModeControl end---------------------------
