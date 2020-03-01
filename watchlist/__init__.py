import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'  # 如果是windows系统,三个斜杠
else:
    prefix = 'sqlite:////'  # 如果是Mac, Linux系统,四个斜杠

# 配置
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE',
                                                                                                        'sqlite.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

db = SQLAlchemy(app)

# Flask-login 初始化操作
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数, 接受用户ID作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'
login_manager.login_message = '没有登录'
login_manager.needs_refresh_message = '刷新登录!'


@app.context_processor  # 模板上下文处理函数
def inject_user():
    from watchlist.models import User
    try:
        user = User.query.filter_by(id=current_user.id).first()
        return dict(user=user)
    except AttributeError:
        return dict(user='')


from watchlist import views, error, commands
