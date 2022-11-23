from app import app
from app import db
from app.wtc_account import models
from app.wtc_demo import models

with app.app_context():
	db.create_all()
