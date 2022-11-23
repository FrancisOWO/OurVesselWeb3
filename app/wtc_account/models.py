from app import db
from flask_login import UserMixin

# 一般用户
class User(UserMixin, db.Model):
    __tablename__ = "user"
    # 字段
    user_id = db.Column(db.String(7), primary_key=True)     # 账号
    password = db.Column(db.String(32), nullable=False)     # 密码
    username = db.Column(db.String(24), nullable=False)     # 昵称
    # gender = db.Column(db.Enum('F','M'))   # 性别
    # phone = db.Column(db.String(11))    # 手机号码
    # email = db.Column(db.String(256))   # 邮箱
    # avatar = db.Column(db.String(256))  # 头像路径

