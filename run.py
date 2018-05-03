#encoding:utf8
import pdb
from tools import *
from flask import Flask

if __name__ == "__main__":
    #pdb.set_trace()
    app = Flask(__name__)
    #app.secret_key = '1The2quick3brown4fox5jumps6over7the8lazy9dog0'
    #app.config['JSON_AS_ASCII'] = False        

    from views import main as main_bp
    app.register_blueprint(main_bp)
    
    app.run( host="0.0.0.0" )
    #from gevent import pywsgi
    #from geventwebsocket.handler import WebSocketHandler
    #log = CLog();
    #server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler, log=log,error_log=log)
    #server.serve_forever()

#暂未限制Query对User的查询
#添加QueryUser接口，密码处理，所在单位处理
#风场面板中还没有相关人员显示。

