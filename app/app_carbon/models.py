from app import db
import datetime

class CarbonTransaction(db.Model):
    __tablename__ = "carbon_transaction"
    # 字段
    TransactionId = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id
    BuyOrSell = db.Column(db.Integer, nullable=False)  # 1为购买 0为出售
    ShipMmsi = db.Column(db.String(16), nullable=False)  # 船舶mmsi
    Price = db.Column(db.Float, nullable=False)  # 价格
    Number = db.Column(db.Integer, nullable=False)  # 数量
    txid = db.Column(db.String(64), nullable=False)  # 存证哈希，64位
    time = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)  # 时间

    def __init__(self, BuyOrSell, ShipMmsi, Price, Number, txid):
        self.BuyOrSell = BuyOrSell
        self.ShipMmsi = ShipMmsi
        self.Price = Price
        self.Number = Number
        self.txid = txid


class CarbonTransactionInfoALL(db.Model):
    __tablename__ = "carbon_transaction_info_all"
    # 字段
    TransactionId = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id
    BuyerMmsi = db.Column(db.String(16), nullable=False)  # 买方mmsi
    SellerMmsi = db.Column(db.String(16), nullable=False)  # 卖方mmsi
    Price = db.Column(db.Float, nullable=False)  # 价格
    Number = db.Column(db.Integer, nullable=False)  # 数量
    txid = db.Column(db.String(64), nullable=False)  # 存证哈希，64位
    time = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)  # 时间

    def __init__(self, BuyerMmsi, SellerMmsi, Price, Number, txid):
        self.BuyerMmsi = BuyerMmsi
        self.SellerMmsi = SellerMmsi
        self.Price = Price
        self.Number = Number
        self.txid = txid



class CarbonTransactionInfoMyself(db.Model):
    __tablename__ = "carbon_transaction_info_myself"
    # 字段
    TransactionId = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id
    BuyerMmsi = db.Column(db.String(16), nullable=False)  # 买方mmsi
    SellerMmsi = db.Column(db.String(16), nullable=False)  # 卖方mmsi
    Price = db.Column(db.Float, nullable=False)  # 价格
    Number = db.Column(db.Integer, nullable=False)  # 数量
    txid = db.Column(db.String(64), nullable=False)  # 存证哈希，64位
    time = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)  # 时间

    def __init__(self, BuyerMmsi, SellerMmsi, Price, Number, txid):
        self.BuyerMmsi = BuyerMmsi
        self.SellerMmsi = SellerMmsi
        self.Price = Price
        self.Number = Number
        self.txid = txid
