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
}

@carbon_bp.route('/carbon_BaseInfo', methods=['GET', 'POST'])
def carbon_BaseInfo():
    ship_info = mvsl.get_shipInfo_by_code(Ship["中海才华"])
    ship_status = mvsl.get_shipStatus_by_code(Ship["中海才华"])

    ship_track_input_data = {
        "mmsi": ship_info["mmsi"],
        "startTime": ship_status["startPostime"],
        "endTime": ship_status["statusTime"],
        "sparse": 1,
        "withWeather": 0,
    }
    # print(mvsl.get_shipStatus_by_code(Ship["中海才华"]))
    ship_track_output_data = mvsl.get_shipTrack_by_code(ship_track_input_data)

    ship_track_predict_input_data = {
        "mmsi": ship_info["mmsi"],
        "dest": ship_status["legEndPortCode"],
        "speed": ship_status["calculateSpeed"],
        "softLink": True,
    }
    ship_track_predict_output_data = mvsl.get_shipTrackPredict_by_code(ship_track_predict_input_data)
    print(ship_track_predict_output_data)
    return render_template(
        "carbon_BaseInfo.html",
        title='碳排放基本信息',
        demolinks=demolinks,
        tabletitle="碳排放"
        # text_list=text_list,
    )
