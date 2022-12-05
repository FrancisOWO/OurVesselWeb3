import json

from flask import render_template, request, jsonify
from app import app, login
from app.app_map import map_bp
from .models import *
from .forms import *

from app.app_demo import demolinks # 导航栏链接
from app.utils.config import ak

from app.app_carbon import Ship

import app.utils.wutongchain as wtc
import app.utils.myvessel as mvsl


@map_bp.route('/helloMap', methods=['GET','POST'])
def hello_map():
    return render_template(
        "helloMap.html",
        title = "地图示例",
        ak = ak,
        demolinks = demolinks,
    )


@map_bp.route('/portInfo', methods=['GET'])
def get_port_info():
    print("HelloHelloHelloHelloHelloHello")
    port = request.args.get("port")
    last_code = request.args.get("last_code")
    print(port)

    port_list = {
        "CNYSN": "上海-洋山 [CN]",
        "CNYAN": "烟台 [CN]",
    }

    # 搜索匹配的key或value
    port_code = None
    port_name = None
    for key in port_list.keys():
        # 搜索内容==港口代码 或 搜索内容在完整名称中(模糊搜索)
        if (port == key) or (port in port_list[key]):
            port_code = key
            port_name = port_list[key]
            break

    # 什么都没找到
    err_ret = {"status": False}
    if port_code == None:
        return jsonify(err_ret)

    # 和上次查询的港口一样，不重复查询
    if port_code == last_code:
        print("#### 无需重复查询 ####")
        return jsonify({"status": "same"})

    print(port_code, port_name)

    # 根据港口代码请求港口信息
    port_info = mvsl.get_port_by_code(port_code)
    print(port_info)

    # 请求失败
    if port_info == None:
        return jsonify(err_ret)

    port_info["status"] = True
    return jsonify(port_info)


@map_bp.route('/holidays', methods=['GET'])
def get_holidays():
    ctryCode = request.args.get("ctryCode")
    year = request.args.get("year")
    month = request.args.get("month")
    print(ctryCode, year, month)

    # 根据港口代码请求港口信息
    holidays = mvsl.get_holiday_list([ctryCode], year, month)
    print(holidays)

    # err_ret = {"status": False}
    # 请求失败
    # if holidays == None:
    #     return jsonify(err_ret)

    # ok_ret = {
    #     "status": True,
    #     "holidays": holidays
    # }
    return jsonify(holidays)


@map_bp.route('/forecast', methods=['GET'])
def get_forecast():
    portCode = request.args.get("portCode")
    print(portCode)

    # 根据港口代码请求港口信息
    forecast = mvsl.get_forecast([portCode])
    print(forecast["current"]["windDegCn"])

    return jsonify(forecast)


@map_bp.route("/shipInfo", methods=['GET'])
def get_ship_info():
    content = request.args.get("ship")
    last_mmsi = request.args.get("last_mmsi")

    ship_name = None
    ship_mmsi = None
    for key in Ship.keys():
        # 搜索内容在完整名称中(模糊搜索) 或 搜索内容==mmsi
        if (content in key) or (content == str(Ship[key])):
            ship_name = key
            ship_mmsi = Ship[key]
            break

    # 什么都没找到
    err_ret = {"status": False}
    if ship_name == None:
        return jsonify(err_ret)

    # 和上次查询的港口一样，不重复查询
    if ship_mmsi == last_mmsi:
        print("#### 无需重复查询 ####")
        return jsonify({"status": "same"})

    print(ship_mmsi, ship_name)

    ship_info = mvsl.get_shipInfo_by_code(ship_mmsi)
    ship_status = mvsl.get_shipStatus_by_code(ship_mmsi)

    # 要判断返回是否为 None，再进行下一步！！！
    ok_flag = (ship_info != None and ship_status != None)

    ship_track_output_data = None
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
        ship_track_output_data = mvsl.get_shipTrackList_by_code(ship_track_input_data)
        ok_flag = (ship_track_output_data != None)

    ship_track_predict_output_data = None
    if ok_flag:
        # 获取船舶预测轨迹
        ship_track_predict_input_data = {
            "mmsi": ship_info["mmsi"],
            "dest": ship_status["legEndPortCode"],
            "speed": ship_status["calculateSpeed"],
            "softLink": True,
        }
        ship_track_predict_output_data = mvsl.get_shipTrackPredictList_by_code(ship_track_predict_input_data)
        ok_flag = (ship_track_predict_output_data != None)

    # print(ship_track_output_data)
    # print(ship_track_predict_output_data)
    
    # 字典合并
    ship_info.update(ship_status)
    print(ship_info)

    ship_info["ship_track_history"] = ship_track_output_data
    ship_info["ship_track_predict"] = ship_track_predict_output_data
    ship_info["status"] = True
    
    return jsonify(ship_info)
