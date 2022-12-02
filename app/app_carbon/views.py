from flask import render_template  # , flash, redirect, url_for
from app import app, login
from app.app_carbon import carbon_bp
from .models import *
from .forms import *

from app.app_demo import demolinks  # 导航栏链接
import app.utils.myvessel as mvsl
import json

Ship = {
    "中海才华": 477464900,
    "中海海王星": 477598400,
}

SC = {
    'name': '73a295a5b15dd9c7ed19b0fa60fe96f10d7ba191450ec62d1012a9313c1146c8',
    'txId': 'a1f733e68fc7a9e0f7f99461c9524739afde1508458af27723b2db5ce52343db'
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
        ship_sail_output_data=ship_sail_output_data,
        ship_cii_output_data=ship_cii_output_data,
        ship_carbon_output_data=ship_carbon_output_data,
        # text_list=text_list,
    )


@carbon_bp.route('/carbon_Transaction', methods=['GET', 'POST'])
def carbon_Transaction():
    main_ship = "中海才华"

    results = CarbonTransactionInfoMyself.query.all()    # 获取个人交易全部记录
    transaction_myself = []
    row_id = 1
    # 读 CarbonTransactionInfoMyself 表的记录
    for res in results:
        if res.BuyerMmsi == str(Ship["中海才华"]):
            res.BuyerMmsi = "我"
        if res.SellerMmsi == str(Ship["中海才华"]):
            res.SellerMmsi = "我"
        transaction_myself.append([row_id, res.BuyerMmsi, res.SellerMmsi, res.Price, res.Number, res.txid, str(res.time)[:-7]])
        row_id += 1
    print(transaction_myself)
    return render_template(
        "carbon_Transaction.html",
        title='碳交易列表',
        demolinks=demolinks,
        tabletitle="碳排放",
        main_ship=main_ship,
        shipnames=Ship.keys(),
        transaction_myself=transaction_myself
        # text_list=text_list,
    )


def add_date():
    transaction = CarbonTransactionInfoMyself("中远海运", "477464900", 0, -18753.5,
                                              "b4d2f795681c906c696b880a20ac8ca210ef083d6293ac228ace8a0608bf347c")
    db.session.add(transaction)
    db.session.commit()
