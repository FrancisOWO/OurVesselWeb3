from flask import render_template  # , flash, redirect, url_for
from app import app, login
from app.app_carbon import carbon_bp
from .models import *
from .forms import *

from app.wtc_demo import demolinks  # 导航栏链接
import app.utils.myvessel as mvsl


# @carbon_bp.route('/carbon', methods=['GET', 'POST'])
# def hello_map():
#     return render_template(
#         "helloMap.html",
#         title="地图示例",
#         ak=ak,
#         demolinks=demolinks,
#     )

Ship = {
    "中海才华": 477464900,
    "中海海王星": 477598400,
}

@carbon_bp.route('/carbon_BaseInfo', methods=['GET', 'POST'])
def carbon_BaseInfo():
    ship_info = mvsl.get_shipInfo_by_code(Ship["中海才华"])
    ship_status = mvsl.get_shipStatus_by_code(Ship["中海才华"])
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
    string_track_predict = ship_track_predict_output_data[0]
    for i in range(1, len(ship_track_predict_output_data)):
        string_track_predict = string_track_predict + "," + ship_track_predict_output_data[i]
    #   获取船舶碳排放数据
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
    #   获取船舶CII数据
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
    print(ship_cii_output_data)
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
        # text_list=text_list,
    )
