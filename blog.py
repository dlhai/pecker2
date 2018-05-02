#各博客页面
@app.route('/blog/*')
def blog():
    param = request.args.to_dict()
    user = loaduser("account='%s'"%param["account"])
    if user is not None and user.pwd == param["pwd"]:
        login_user(User(user))
        fmt = '{"login":"%s","result":"200","nexturl":"%s"}'
        if 0<user.status<6:
            return fmt%(param['account'], '/static/user_init'+str(user.status)+'.html')
        else:
            return fmt%(param['account'], '/static/frame.html')
    else:
        return '{"login":"'+param['account']+'","result":404}\n'

#发表文章、评论/回复、发消息
@app.route("/publish")
@login_required
def publish():
    ret = QueryObj( "select * from user where id="+str(current_user.id))
    if len(ret) <= 0:
        return '{"roleuser":"'+param['account']+'","result":404}\n'
    user = ret[0]
    del user.pwd

    #找到用户的所在单位，若所在单位是风场，则需要读取风区列表
    if atoi(user.depart_table) != 0: 
        tbl = gettbl(user.depart_table)
        user.depart = QueryObj( "select id, name from "+tbl["name"]+" where id="+str(user.depart_id))[0]
        if tbl["name"] == "winder":
            user.sub = QueryObj( "select id, name from winderarea where winder_id="+str(user.depart_id))
    ret=obj()
    ret.fun="curuserinf"
    ret.result = "200"
    ret.data = user
    ret.fields=QueryObj(select(base.sl).where(base.c.table=="user"))
    return Response(tojson(ret), mimetype='application/json')

#推荐、关注 
@app.route('/recom', methods=['POST'])
@login_required
def recom():
    jsn = json.loads(request.data)
    ret=obj(fun="chgpwd", result="200")
    if current_user.id != int(jsn["id"]):
        ret.result = "1002"
        ret.msg = "你不能修改别人的密码"
    if current_user.pwd != jsn["pwd"]:
        ret.result = "1002"
        ret.msg = "旧密码不正确"
    if ret.result == "200":
        sql = "update user set pwd='{0}' where id={1}".format(jsn["newpwd"], jsn["id"])
        conn.execute(sql)
    return Response(tojson(ret), mimetype='application/json')
 
