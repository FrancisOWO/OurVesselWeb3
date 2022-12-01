from app import app
from app import db
from app.app_account import models
from app.app_demo import models

with app.app_context():
	db.create_all()
