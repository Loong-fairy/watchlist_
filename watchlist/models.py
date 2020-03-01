import datetime
from flask_login import UserMixin

from watchlist import db
from werkzeug.security import generate_password_hash, check_password_hash


# 创建数据库模型类
# 用户表
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(20))  # 昵称
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值
    articles = db.relationship("Articles", backref="user")  # 连接博文信息表

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 博文信息表
class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))  # 博文名称
    content = db.Column(db.String(50000))  # 博文内容
    author = db.Column(db.String(20))  # 作者
    pubdate = db.Column(db.DateTime, default=datetime.datetime.now)  # 创建时间
    updated = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # 更新时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

