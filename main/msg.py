
############## websocket功能 ###############################################
@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send("replay:"+message+"!")

############## websocket功能 ###############################################

#to可能是管理员，需要转化
@app.route('/msgto')
def msgto_():
    param = request.args.to_dict()
    ret=check(request, wt)
    if ret.result != "200":
        return Response(tojson(ret), mimetype='application/json')

    if request.content_type == 'application/json':
        js = json.loads(request.data)
        fdv = ",\n".join([ k + "='"+ v+"'" for k,v in js["val"].items()] )
        sql = "update {0} set {1} where id={2}".format(js["ls"], fdv, js["id"])
        conn.execute(sql)
    else:
        files = request.files.to_dict()
        fields =request.form.to_dict()
        # 1. 保存附件
        fmt = "./uploads/{ls}_{fd}/{ls}_{fd}_{id}{ext}"
        for k,v in files.items(): 
            fname = fmt.format(ls=params["ls"],fd=k, id=params["id"],ext=os.path.splitext(v.filename)[1] )
            fields[k]=fname
            v.save("./static/"+fname)
        # 2. 保存字段数据
        fdv = ",\n".join([ k + "='"+ v+"'" for k,v in fields.items()] )
        sql = "update {0} set {1} where id={2}".format(params["ls"], fdv, params["id"])
        conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')

#内部用函数
def msgto(userid):
    pass

#to需要读取阅读书签，登录后下载未读消息，或定读取                                                                          
@app.route('/rdrecentmsg')
def rdrecentmsg():
    param = request.args.to_dict()
    ret=check(request, wt)
    if ret.result != "200":
        return Response(tojson(ret), mimetype='application/json')

    if request.content_type == 'application/json':
        js = json.loads(request.data)
        fdv = ",\n".join([ k + "='"+ v+"'" for k,v in js["val"].items()] )
        sql = "update {0} set {1} where id={2}".format(js["ls"], fdv, js["id"])
        conn.execute(sql)
    else:
        files = request.files.to_dict()
        fields =request.form.to_dict()
        # 1. 保存附件
        fmt = "./uploads/{ls}_{fd}/{ls}_{fd}_{id}{ext}"
        for k,v in files.items(): 
            fname = fmt.format(ls=params["ls"],fd=k, id=params["id"],ext=os.path.splitext(v.filename)[1] )
            fields[k]=fname
            v.save("./static/"+fname)
        # 2. 保存字段数据
        fdv = ",\n".join([ k + "='"+ v+"'" for k,v in fields.items()] )
        sql = "update {0} set {1} where id={2}".format(params["ls"], fdv, params["id"])
        conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')

