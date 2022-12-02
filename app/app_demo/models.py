from app import db

# Demo: Hello World!
class RecGreetings(db.Model):
    __tablename__ = "rec_greetings"
    # 字段
    rec_id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # id
    msg = db.Column(db.String(256), nullable=False) # 一段信息，如："Hello World!"
    time = db.Column(db.DateTime, nullable=False)   # 时间
    txid = db.Column(db.String(64), nullable=False) # 存证哈希，64位
