

function f2s(data, field) {
	var fn = (typeof field == "string") ? field : field.name;
    if (fn == "clss") return data[fn] == "" ? "" :GetSub(db_devclss, "id", data[fn]).name;
    else if (fn == "devwh_id")
		return data[fn] == "" ? "" :GetSub(g_devwhs.data, "id", data[fn]).name;
    else if (fn == "status") return data[fn] == "" ? "" :GetSub(status_dev, "id", data[fn]).name;
    else if (fn == "vender_id") return data[fn] == "" ? "" :GetSub(g_devvenders.data, "id", data[fn]).name;
    else if (fn == "driver_id") 
		return data[fn] == "" ? "" :GetSub(g_driver.data, "id", data[fn]).name;
    else return data[fn];
}
function f2e(data, field) {
    if (field.name == "clss") return RenderSelect(db_devclss, data[field.name]);
    else if (field.name == "devwh_id") return g_user.depart.name;
    else if (field.name == "status") return RenderSelect(status_dev, data[field.name]);
    else if (field.name == "vender_id") return RenderSelect(g_devvenders.data, data[field.name]);
    else if (field.name == "driver_id") return RenderSelect(g_driver.data, data[field.name]);
    else return data[field.name];
}
function devcheck(formdata) {
	var img = formdata.get("face");
	if (img.size == 0)
		formdata.delete("face");
	var img = formdata.get("img");
	if (img.size == 0)
		formdata.delete("img");
	return true;
}
function devpane(dev, fields) {
	var ui2 = `
		<div style="float:left;display:block;height:240px;width:280px;margin-top:5px;margin-left:10px;">
			<div style="float:left;display:block;height:78px;width:78px;">
				<img style="width:100%;height:100%;" src="{face}">
			</div>
			<div class="x2Form narrow">
				<div style="margin-top:0px;"><label>编号</label><div style="display:inline-block;">{code}</div></div>
				<div><label>型号</label><div>{type}</div></div>
			</div>
			<div style="width:280px;height:160px;margin-top:5px">
				<img style="width:100%;height:100%;" src="{img}" >
			</div>
		</div>`;
	return ui2.format(dev).replace(/src=""/g, '') + RenderPane3(dev, fields, f2s);
}

function devform(dev, fields) {
	var ui2 = `
		<div style="float:left;display:block;height:240px;width:280px;margin-top:5px;margin-left:10px;">
			<div style="float:left;display:block;">
				<label class="imagelive" style="height:78px;width:78px;" for="face">
					<img style="width:100%;height:100%;"  src="{face}" >
					<input name="face" type="file" id="face" name="face" accept="image/*">
				</label>
			</div>
			<div class="x2Form narrow">
				<div style="margin-top:0px;"><label>编号</label><input name="code" type="text" value="{code}" style="display:inline-block;" /></div>
				<div><label>型号</label><input name="type" type="text" value="{type}" style="display:inline-block;" /></div>
			</div>
			<label class="imagelive" style="width:280px;height:160px;margin-top:5px" for="img">
				<img style="width:100%;height:100%;" src="{img}" >
				<input name="img" type="file" id="img" name="img" accept="image/*">
			</label>
		</div>`;
    return ui2.format(dev).replace(/src=""/g, '') + xCreateNode({ "name": "div", "class": "x2Form",
		"style": "min-height:250px;", "body": RenderFormIn(dev, fields, f2e) } );
}