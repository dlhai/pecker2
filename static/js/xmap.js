// CreateMark中的 UpdateCurData 需要先定义
// ShowWindow中的 FieldToShow 需要先定义

function CreateMap( id ) {
    var map = new BMap.Map(id);
    map.centerAndZoom(new BMap.Point(116.404, 39.915), 6); //设置中心点坐标和地图级别
    map.addControl(new BMap.ScaleControl({ anchor: BMAP_ANCHOR_BOTTOM_RIGHT })); // 左下角，添加比例尺
    map.addControl(new BMap.NavigationControl({ anchor: BMAP_ANCHOR_TOP_RIGHT })); //左上角，添加默认缩放平移控件
    map.enableScrollWheelZoom();//开启鼠标滚轮缩放
    return map;
}

function CreateMark(iconname, data, type, fields) {
    var marker = new BMap.Marker(CreatePoint(data.position), { icon: GetIcon(iconname) });
    var label = new BMap.Label("name" in data ? data.name : data.code, { offset: new BMap.Size(-10, 32) });
    label.setStyle({ border: "0px", color: "blue" });
    marker.setLabel(label);
    g_map.addOverlay(marker);
    data.mk = marker;
//  marker.addEventListener("dragend", function (type, target, pixel, point) { UpdateCurData(type, data); });
    marker.addEventListener("click", function (e) { ShowWindow(type, data, fields, e); });
    label.addEventListener("click", function (e) { ShowWindow(type, data, fields, e); });
}

function GetIcon(iconname) {
    icons = new Object();
    if (!(iconname in icons)) {
        var name = "/static/img/" + iconname + ".png";
        icons[iconname] = new BMap.Icon(name, new BMap.Size(32, 32));
        icons[iconname].imageSize = new BMap.Size(32, 32);
    }
    return icons[iconname];
}

function CreatePoint(pos) {
    var ar = pos.split(" ");
    return new BMap.Point(parseFloat(ar[0]), parseFloat(ar[1]));
}

function CreatePolygon(pos) {
    var ar = pos.split(",");
    var arr = [];
    for (var i in ar)
        arr.push(CreatePoint(ar[i]));
    return new BMap.Polygon(arr, { strokeColor: "Chocolate", strokeWeight: 2, strokeOpacity: 0.5 });
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
function ModeControl(onmodechange) {
    // 默认停靠位置和偏移量
    this.defaultAnchor = BMAP_ANCHOR_TOP_LEFT;
    this.defaultOffset = new BMap.Size(10, 10);
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
