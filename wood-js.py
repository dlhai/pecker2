from flask_sqlalchemy import SQLAlchemy  
from flask import Flask, redirect, url_for, request, flash, render_template  
from flask_login import LoginManager, login_user, login_required, logout_user  
  
app = Flask(__name__)  
app.secret_key = "The quick brown fox jumps over the lazy dog"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/pecker.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  
app.debug = True  
  
db = SQLAlchemy(app)  
login_manager = LoginManager()  
login_manager.init_app(app)  
  
login_manager.login_view = "login"  # 定义登录的 视图  
login_manager.login_message = '请登录以访问此页面'  # 定义需要登录访问页面的提示消息  


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = password

    def verify_password(self, password):
        password_hash = self.get_password_hash()
        if password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def get_password_hash(self):
        return self.password_hash

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        if self.username is not None:
            try:
                with open(PROFILE_FILE) as f:
                    user_profiles = json.load(f)
                    if self.username in user_profiles:
                        return user_profiles[self.username][1]
            except IOError:
                pass
            except ValueError:
                pass
        return unicode(uuid.uuid4())

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            with open(PROFILE_FILE) as f:
                user_profiles = json.load(f)
                for user_name, profile in user_profiles.iteritems():
                    if profile[1] == user_id:
                        return User(user_name)
        except:
            return None
        return None
 
 
@login_manager.user_loader  # 使用user_loader装饰器的回调函数非常重要，他将决定 user 对象是否在登录状态  
def user_loader(id):  # 这个id参数的值是在 login_user(user)中传入的 user 的 id 属性  
    user = User.query.filter_by(id=id).first()  
    return user  
  
  
# 添加登录视图，如果是GET方法，返回一个简单的表单  
 
@app.route('/login/', method=['GET', 'POST'])  
def login():  
    from model.model import User  
    if request.method == 'POST':  
        name = request.form.get('name')  
        user = User.query.filter_by(name=name).first()  
        if not user:  
            flash('该用户不存在')  
        elif request.form.get('pwd') != user.pwd:  
            flash('密码错误')  
        else:  
            login_user(user, remember=True)  
            next_url = request.args.get('next')  
            return redirect(next_url or url_for('login_success'))  
    return render_template('login.html')  # 如果密码是 123 就会跳转到视图函数 index 上  
 
 
@app.route('/')  
@login_required  
def index():  
    return 'Hello Tank'  
 
 
@app.route('/succees/')  
@login_required  
def login_success():  
    return render_template('base.html')  
 
 
@app.route('/logout/')  
@login_required  
def logout():  
    logout_user()  # 登出用户  
    return '已经退出登录'  
 
 
@app.errorhandler(404)  
def page_not_found(error):  
    return render_template('page_not_found.html'), 404  
  
  
if __name__ == '__main__':  
    app.run()  