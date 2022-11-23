from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.init_app(app)
# db.create_all()

login = LoginManager(app)
login.init_app(app)
login.login_message  = '请先登录！'
login.login_view = 'account.login'
