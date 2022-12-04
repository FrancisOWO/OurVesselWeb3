import json

from flask import render_template, request, jsonify
from app import app, login
from app.app_map import map_bp
from .models import *
from .forms import *

from app.app_demo import demolinks # 导航栏链接
from app.utils.config import ak

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
    err_ret = {"status": False}

    # 搜索匹配的key或value
    port_code = None
    port_name = None
    for key in port_list.keys():
        # 港口代码
        if port == key:
            port_code = key
            port_name = port_list[key]
            break

        # 模糊搜索，字符串在完整名称中
        if port in port_list[key]:
            port_code = key
            port_name = port_list[key]
            break

    # 什么都没找到
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