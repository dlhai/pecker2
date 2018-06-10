#/_tbl_/_tbl_create
@app.route("/_tbl_/_tbl_create",methods=['POST'])
@login_required
def _tbl_create():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="_tbl_/_tbl_create")

    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    conn.execute(toinsert("_tbl_",form))
    r.data = QueryObj("select * from _tbl_ where id in (select max(id) from _tbl_)")
    return toret(r,result=200)

#/_tbl_/_tbl_modify?id=
@app.route("/_tbl_/_tbl_modify",methods=['POST'])
@login_required
def _tbl_modify():
    params = request.args.to_dict()
    form =request.form.to_dict()
    r = obj(result="404",fun="_tbl_/_tbl_modify")

    if "id" not in params:
        return toret(r,msg="缺少参数id")
    if "code" not in form or form["code"]=="":
        return toret(r,msg="code不正确")

    id=params["id"]
    conn.execute(toupdate("_tbl_", form, obj(id=id)))
    r.data = QueryObj("select * from _tbl_ where id=%s"%id)
    return toret(r,result=200)

#/_tbl_/_tbl_remove?id=
@app.route("/_tbl_/_tbl_remove")
@login_required
def _tbl_remove():
    params = request.args.to_dict()
    r = obj(result="404",fun="/_tbl_/_tbl_remove")
    if "id" not in params:
        return toret(r,msg="缺少参数id")

    if querycount("xxx",obj(xxx="xxx",id=params["id"])) > 0:
        return toret(r,msg="已xxx，不能删除")

    id = params["id"]
    conn.execute(todelete("_tbl_", obj(id=id)))
    return toret(r,result=200)

