from flask import render_template, redirect, url_for  # , flash, redirect, url_for
from app import app, login
from app.app_carbon import carbon_bp
from .models import *
from .forms import *
from app.utils import wutongchain as wtc
from app.app_demo import demolinks  # 导航栏链接
import app.utils.myvessel as mvsl
import json

Ship = {
    "中海才华": 477464900,
    "中海海王星": 477598400,
}

SC = {
    'name': '73a295a5b15dd9c7ed19b0fa60fe96f10d7ba191450ec62d1012a9313c1146c8',
    'txId': 'c6aaf6130e913a9c0e3db159690b69a903b4248c4592cb910dc3867527319b13',
    "carbon_quota": "carbon_quota",  # 额度发放(string account, float amount)
    "init": "init_account",  # 初始化账户(string account)
    "transfer": "transfer",  # 转账 参数(string from, string to, float amount)
    "getBlance": "getBlance",  # 余额查询 (string account) account为mmsi，如果查询冻结余额，则为mmsi_frozen
    "getFrozenBlance": "getFrozenBlance",  # 查询碳排放冻结余额(string account)
    "changeBlance": "changeBlance",  # 增减余额 (string account, float amount)
    "frozenBlance": "frozenBlance",  # 冻结操作 (string account, float amount)
}

Blockchain_Transaction_Id = {
    "船舶信息存证": "7dca33368851e1aadfbc67008ab07e3e2203e9c141ef825b209e4e3e6f670290",
    "船舶航运信息存证": "3f2721b5aac1cfc649021f39530215c6d7aae5c2720189893b10023b8cf26e1d"
}


@carbon_bp.route('/carbon_BaseInfo', methods=['GET', 'POST'])
def carbon_BaseInfo():
    ship_info = mvsl.get_shipInfo_by_code(Ship["中海才华"])
    ship_status = mvsl.get_shipStatus_by_code(Ship["中海才华"])

    # 要判断返回是否为 None，再进行下一步！！！
    ok_flag = (ship_info != None and ship_status != None)

    ship_track_output_data = {}
    if ok_flag:
        # 获取船舶历史轨迹数据
        ship_track_input_data = {
            "mmsi": ship_info["mmsi"],
            "startTime": ship_status["startPostime"],
            "endTime": ship_status["statusTime"],
            "sparse": 1,
            "withWeather": 0,
        }

        # print(mvsl.get_shipStatus_by_code(Ship["中海才华"]))
        ship_track_output_data = mvsl.get_shipTrack_by_code(ship_track_input_data)
        ok_flag = (ship_track_output_data != None)

    ship_track_predict_output_data = {}
    if ok_flag:
        string_track = ship_track_output_data[0]
        for i in range(1, len(ship_track_output_data)):
            string_track = string_track + "," + ship_track_output_data[i]

        # 获取船舶预测轨迹
        ship_track_predict_input_data = {
            "mmsi": ship_info["mmsi"],
            "dest": ship_status["legEndPortCode"],
            "speed": ship_status["calculateSpeed"],
            "softLink": True,
        }
        ship_track_predict_output_data = mvsl.get_shipTrackPredict_by_code(ship_track_predict_input_data)
        ok_flag = (ship_track_predict_output_data != None)

    ship_carbon_output_data = {}
    string_track_predict = ""
    if ok_flag:
        string_track_predict = ship_track_predict_output_data[0]
        for i in range(1, len(ship_track_predict_output_data)):
            string_track_predict = string_track_predict + "," + ship_track_predict_output_data[i]

        # 获取船舶碳排放数据
        ship_carbon_input_data = {
            "mmsi": ship_info["mmsi"],
            "startTime": ship_status["startPostime"],
            "endTime": ship_status["statusTime"],
            "predict": {
                "mmsi": ship_info["mmsi"],
                "startTime": ship_status["statusTime"],
                "endTime": ship_status["legEndTime"],
                "isFullLoad": ship_status["isFullLoad"],
                "lineString": string_track_predict,
            }
        }
        ship_carbon_output_data = mvsl.get_shipCarbon_by_code(ship_carbon_input_data)
        ok_flag = (ship_carbon_output_data != None)

    ship_cii_output_data = {}
    if ok_flag:
        ship_carbon_output_data["carbon_sum"] = format(sum(ship_carbon_output_data["carbon_data"]), '.2f')
        ship_carbon_output_data["carbon_predict_sum"] = format(sum(ship_carbon_output_data["carbon_data_predict"]),
                                                               '.2f')
        ship_carbon_output_data["fuel_sum"] = format(sum(ship_carbon_output_data["fuel_data"]), '.2f')
        ship_carbon_output_data["fuel_predict_sum"] = format(sum(ship_carbon_output_data["fuel_data_predict"]), '.2f')
        # ship_carbon_output_data["carbon_change"] = format((float(ship_carbon_output_data["carbon_predict_sum"]) / ship_status["restDistance"]) - (float(ship_carbon_output_data["carbon_sum"]) / ship_status["pastDistance"]), '.2f')

        # 获取船舶CII数据
        ship_cii_input_data = {
            "mmsi": ship_info["mmsi"],
            "his": {
                "startTime": ship_status["startPostime"],
                "endTime": ship_status["statusTime"],
                "fullLoad": ship_status["isFullLoad"],
                "inPortDays": 0,
                "lineString": string_track_predict,
            },
            "predict": {
                "startTime": ship_status["statusTime"],
                "endTime": ship_status["legEndTime"],
                "fullLoad": ship_status["isFullLoad"],
                "inPortDays": 0,
                "lineString": string_track_predict,
            },
        }
        ship_cii_output_data = mvsl.get_shipCII_by_code(ship_cii_input_data)
        ok_flag = (ship_cii_output_data != None)

    ship_sail_output_data = {}
    if ok_flag:
        #   获取船航行数据
        ship_sail_input_data = {
            "mmsiList": [ship_info["mmsi"]],
            "endYearMonth": "202212",
            "startYearMonth": "202201",
            "cascadeType": 0,
        }
        ship_sail_output_data = mvsl.get_shipSailData_by_code(ship_sail_input_data)
        ok_flag = (ship_sail_output_data != None)

    main_ship = "中海才华"
    return render_template(
        "carbon_BaseInfo.html",
        title='碳排放基本信息',
        demolinks=demolinks,
        tabletitle="碳排放",
        main_ship=main_ship,
        shipnames=Ship.keys(),
        ship_info=ship_info,
        ship_status=ship_status,
        Blockchain_Transaction_Id=Blockchain_Transaction_Id,
        ship_sail_output_data=ship_sail_output_data,
        ship_cii_output_data=ship_cii_output_data,
        ship_carbon_output_data=ship_carbon_output_data,
        # text_list=text_list,
    )


@carbon_bp.route('/carbon_Transaction', methods=['GET', 'POST'])
def carbon_Transaction():
    # carbon_quota(str(Ship["中海才华"]), 24000)
    # carbon_quota(str(Ship["中海海王星"]), 28000)
    # carbon_quota("413798964", 12000)
    # addCarbonTransaction(0, str(Ship["中海海王星"]), 50, 500)
    # addCarbonTransaction(1, str("413798964"), 45, 500)
    # addCarbonTransaction(0, str(Ship["中海海王星"]), 49, 1000)
    main_ship = "中海才华"
    main_ship_mmsi = Ship[main_ship]

    # addCarbonTransaction(1, "477598400", 40, 1000)

    results = CarbonTransaction.query.order_by(CarbonTransaction.TransactionId.desc()).all()  # 获取买卖交易列表
    transaction_list = []
    row_id = 1
    # 读 CarbonTransaction 表的记录
    for res in results:
        operate = 0
        if res.ShipMmsi == str(Ship["中海才华"]):
            operate = 1  # 表示本人
        transaction_list.append(
            [row_id, res.BuyOrSell, res.ShipMmsi, res.Price, res.Number, res.txid, operate])
        row_id += 1

    results = CarbonTransactionInfoALL.query.order_by(
        CarbonTransactionInfoALL.TransactionId.desc()).all()  # 获取个人交易全部记录
    transaction_all = []
    row_id = 1
    # 读 CarbonTransactionInfoMyself 表的记录
    for res in results:
        transaction_all.append(
            [row_id, res.BuyerMmsi, res.SellerMmsi, res.Price, res.Number, res.txid, str(res.time)[:-7]])
        row_id += 1

    results = CarbonTransactionInfoMyself.query.order_by(
        CarbonTransactionInfoMyself.TransactionId.desc()).all()  # 获取个人交易全部记录
    transaction_myself = []
    row_id = 1
    # 读 CarbonTransactionInfoMyself 表的记录
    for res in results:
        transaction_myself.append(
            [row_id, res.BuyerMmsi, res.SellerMmsi, res.Price, res.Number, res.txid, str(res.time)[:-7]])
        row_id += 1

    #  获取碳排放余额和冻结额度
    balance = get_balance(str(Ship[main_ship]))
    frozen_balance = get_balance(str(Ship[main_ship]) + "_frozen")

    carbon_transaction_form = CarbonTransactionForm()
    if carbon_transaction_form.submit.data:
        if carbon_transaction_form.transaction_type.data == "1":
            buy, mmsi, price, number = 0, str(Ship["中海才华"]), float(
                carbon_transaction_form.transaction_price1.data), int(
                carbon_transaction_form.transaction_number1.data)
            addCarbonTransaction(buy, mmsi, price, number)
        elif carbon_transaction_form.transaction_type.data == "2":
            buy, mmsi, price, number = 1, str(Ship["中海才华"]), float(
                carbon_transaction_form.transaction_price2.data), int(
                carbon_transaction_form.transaction_number2.data)
            addCarbonTransaction(buy, mmsi, price, number)
        elif carbon_transaction_form.transaction_type.data == "3":
            buyer = str(carbon_transaction_form.transaction_buyer.data)
            print(carbon_transaction_form.transaction_buyer.data)
            seller = str(Ship[main_ship])
            price = float(0)
            number = float(carbon_transaction_form.transaction_number3.data)
            addCarbonTransactionInfoMyself(buyer, seller, price, number)
        return redirect(url_for('carbon.carbon_Transaction'))

    carbon_transaction_operate_form = CarbonTransactionOperateForm()
    if carbon_transaction_operate_form.btn_cancel.data:
        person_p = CarbonTransaction.query.filter_by(txid=str(carbon_transaction_operate_form.hash_cancel.data)).first()
        if remove_carbon_frozen(str(person_p.ShipMmsi), float(person_p.Number)):
            db.session.delete(person_p)
            db.session.commit()
        return redirect(url_for('carbon.carbon_Transaction'))
    if carbon_transaction_operate_form.btn_buy.data:
        person_p = CarbonTransaction.query.filter_by(txid=str(carbon_transaction_operate_form.hash_buy.data)).first()
        buyer, seller, price, number, statue = str(Ship["中海才华"]), str(person_p.ShipMmsi), float(person_p.Price), float(
            person_p.Number), True
        addCarbonTransactionInfoAll(buyer, seller, price, number, statue)
        db.session.delete(person_p)
        db.session.commit()
        print("购买")
        return redirect(url_for('carbon.carbon_Transaction'))
    if carbon_transaction_operate_form.btn_sell.data:
        person_p = CarbonTransaction.query.filter_by(txid=str(carbon_transaction_operate_form.hash_sell.data)).first()
        buyer, seller, price, number, statue = str(Ship["中海才华"]), str(person_p.ShipMmsi), float(person_p.Price), float(
            person_p.Number), True
        addCarbonTransactionInfoAll(buyer, seller, price, -number, statue)
        db.session.delete(person_p)
        db.session.commit()
        print("购买")
        return redirect(url_for('carbon.carbon_Transaction'))
    return render_template(
        "carbon_Transaction.html",
        title='碳交易列表',
        demolinks=demolinks,
        tabletitle="碳排放",
        main_ship=main_ship,
        main_ship_mmsi=main_ship_mmsi,
        balance=balance,
        frozen_balance=frozen_balance,
        shipnames=Ship.keys(),
        transaction_list=transaction_list,
        transaction_myself=transaction_myself,
        carbon_transaction_form=carbon_transaction_form,
        carbon_transaction_operate_form=carbon_transaction_operate_form,
        transaction_all=transaction_all
        # text_list=text_list,
    )


#  交易
def addCarbonTransactionInfoMyself(buyer, seller, price, number):
    res = wtc.sc_invoke(SC['name'], SC['transfer'], [str(seller), str(buyer), float(number)])
    if res:
        tx_id = res["txId"]
        transaction = CarbonTransactionInfoMyself(buyer, seller, price, number, tx_id)
        db.session.add(transaction)
        db.session.commit()


# 冻结碳交易
def addCarbonTransaction(buy, mmsi, price, number):
    res = wtc.sc_invoke(SC['name'], SC['frozenBlance'], [str(mmsi), float(number)])
    if res:
        tx_id = res["txId"]
        transaction = CarbonTransaction(buy, mmsi, price, number, tx_id)
        db.session.add(transaction)
        db.session.commit()
        return True
    else:
        return False


#  查询余额
def get_balance(mmsi):
    res = wtc.sc_query(SC['name'], SC['getBlance'], [mmsi])
    if res:
        return format(float(res["result"]), '.2f')
    else:
        return False

# 解除冻结碳排放
def remove_carbon_frozen(mmsi, number):
    res = wtc.sc_invoke(SC['name'], SC['frozenBlance'], [str(mmsi), float(-number + 0.000001)])
    if res:
        return True
    else:
        return False

def addCarbonTransactionInfoAll(buyer, seller, price, number, statue):
    # 买方
    if statue:
        res = wtc.sc_invoke(SC['name'], SC['changeBlance'], [str(buyer), float(number)])
    # 卖方
    else:
        res = wtc.sc_invoke(SC['name'], SC['changeBlance'], [str(seller), float(-number)])
    if res:
        tx_id = res["txId"]
        transaction = CarbonTransactionInfoALL(buyer, seller, price, number, tx_id)
        transaction1 = CarbonTransactionInfoMyself(buyer, seller, price, number, tx_id)
        db.session.add(transaction)
        db.session.add(transaction1)
        db.session.commit()

#  碳排放配额
def carbon_quota(buyer, number):
    res = wtc.sc_invoke(SC['name'], SC['changeBlance'], [str(buyer), float(number)])
    seller = "中远海运集团"
    price = float(0)
    if res:
        tx_id = res["txId"]
        transaction = CarbonTransactionInfoMyself(buyer, seller, price, number, tx_id)
        db.session.add(transaction)
        db.session.commit()
