import requests
import json

from app.utils.config import HEADER_AUTHORIZATION

# 这是直接访问【船视宝】的url，【船视宝】可以查港口信息，中远的api不能
HOST = "voc.myvessel.cn"
URL_PREFIX = f"https://{HOST}"


def get_host():
    return HOST


def get_url_prefix():
    return URL_PREFIX


'''
API 	: /sdc/v1/ports/code/{port_code}
请求方式	: GET
说明 	: 获取港口信息
'''


def get_port_by_code(port_code):
    # url
    url = f"{URL_PREFIX}/sdc/v1/ports/code/{port_code}"

    # 请求头：没有【User-Agent】会返回405
    headers = {
        "User-Agent": "PostmanRuntime/7.29.2",
        "Authorization": HEADER_AUTHORIZATION
    }
    # 发送请求
    res = requests.get(url=url, headers=headers)
    if res.status_code != 200:
        print(res)
        return None

    res_dict = res.json()["data"]
    my_dict = {
        "portCode": res_dict["portCode"],  # "CNYAN",
        "nameCn": res_dict["nameCn"],  # "烟台",
        "nameEn": res_dict["nameEn"],  # "YANTAI",
        # "ctryCode"	: res_dict["ctryCode"],		# "CN",
        "ctryNameCn": res_dict["ctryNameCn"],  # "中国",
        "ctryNameEn": res_dict["ctryNameEn"],  # "China",
        # "namePinyin": res_dict["namePinyin"],	# "YANTAI",
        "lon": res_dict["lon"],  # 121.400000,
        "lat": res_dict["lat"],  # 37.550000,
    }
    return my_dict


'''
API 	: /sdc/v1/vessels/{ship_mmsi}/detail
请求方式	: GET
说明 	: 获取船舶信息
返回
mmsi	：船舶mmsi
载重吨	：船舶载重吨
length_width_height	：船舶长宽高
buildYearMonth	：船舶建成年月
draught_speed	：船舶吃水和航速
ship_type	：船舶类型
ship_nameCn	：船舶中文名
ship_nameEn	：船舶英文名

'''


def get_shipInfo_by_code(ship_mmsi):
    # url
    url = f"{URL_PREFIX}/sdc/v1/vessels/{ship_mmsi}/detail"
    print(url)
    # 请求头：没有【User-Agent】会返回405
    headers = {
        "User-Agent": "PostmanRuntime/7.29.2",
        "Authorization": HEADER_AUTHORIZATION
    }
    # 发送请求
    res = requests.get(url=url, headers=headers)
    if res.status_code != 200:
        print(res)
        return None

    res_dict = res.json()["data"]

    my_dict = {
        "mmsi": res_dict["mmsi"],  # 船舶mmsi
        "载重吨": res_dict["dwt"],  # 船舶载重吨
        "length_width_height": str(res_dict["length"]) + "m*" + str(res_dict["width"]) + "m*" + str(
            res_dict["height"]) + "m",  # 船舶长宽高
        "buildYearMonth": res_dict["buildYearMonth"][:4] + "-" + res_dict["buildYearMonth"][-2:],
        "draught_speed": str(format(res_dict["draught"], '.1f')) + 'm/' + str(res_dict["speed"]) + "kn",
        "ship_type": res_dict["vesselSub2TypeNameCn"],
        "ship_nameCn": res_dict["nameCn"],
        "ship_nameEn": res_dict["nameEn"],
    }
    return my_dict


'''
API 	: sdc/v1/vessels/status/current/{ship_mmsi}
请求方式	: GET
说明 	: 获取船舶信息
返回
"mmsi"	:   船舶mmsi
"statusTime"	: 查询时间
"startPostime"	: 开始航行时间
"lon"	：此时船舶经度
"lat"	：此时船舶维度
"legStartPortCode"	：起始点港口代码
"legStartPortNameCn"	：起始点港口中文名称
"legStartPortCtryCode"	：起始点国家代码
"legEndTime"	：航行结束时间
"legEndPortCode"	：终点港口代码
"legEndPortNameCn"	：终点港口中文名
"legEndPortCtryCode"：终点港口国家代码
"isFullLoad"	：满载比例
legDurationPredict	: 预测航行总时间
legDurationAvg	: 平均航行时间
delayDurationAvg	: 平均停泊时间
pastDuration	: 已航行时间
restDuration	：剩余航行时间
legDistance	：总里程
pastDistance	：已航行里程
restDistance	：剩余里程
sailPct	：航行比例
currentSpeed	：对地速度
averageSpeed	：平均速度
startBerthCargoTypeName	: 货物类型
dailyFuelTotal	：燃料使用量

'''


def get_shipStatus_by_code(ship_mmsi):
    # url
    url = f"{URL_PREFIX}/sdc/v1/vessels/status/current/{ship_mmsi}"
    # 请求头：没有【User-Agent】会返回405
    headers = {
        "User-Agent": "PostmanRuntime/7.29.2",
        "Authorization": HEADER_AUTHORIZATION
    }
    # 发送请求
    res = requests.get(url=url, headers=headers)
    if res.status_code != 200:
        print(res)
        return None

    res_dict = res.json()["data"]

    my_dict = {
        "mmsi": res_dict["mmsi"],  # 船舶mmsi
        "statusTime": res_dict["statusTime"],
        "startPostime": res_dict["startPostime"],
        "lon": res_dict["lon"],
        "lat": res_dict["lat"],
        "legStartPortCode": res_dict["legStartPortCode"],
        "legStartPortNameCn": res_dict["legStartPortNameCn"],
        "legStartPortCtryCode": res_dict["legStartPortCtryCode"],
        "legEndTime": res_dict["legEndTime"],
        "legEndPortCode": res_dict["legEndPortCode"],
        "legEndPortNameCn": res_dict["legEndPortNameCn"],
        "legEndPortCtryCode": res_dict["legEndPortCtryCode"],
        "isFullLoad": res_dict["isFullLoad"],
        "legDurationPredict": str(int(res_dict["legDurationPredict"] / 24)) + 'd' + str(
            int(res_dict["legDurationPredict"] % 24)) + 'h',
        "legDurationAvg": str(int(res_dict["legDurationAvg"] / 24)) + 'd' + str(
            int(res_dict["legDurationAvg"] % 24)) + 'h',
        "delayDurationAvg": str(int(res_dict["delayDurationAvg"] / 24)) + 'd' + str(
            int(res_dict["delayDurationAvg"] % 24)) + 'h',
        "pastDuration": str(int(res_dict["pastDuration"] / 24)) + 'd' + str(int(res_dict["pastDuration"] % 24)) + 'h',
        "restDuration": str(int(res_dict["restDuration"] / 24)) + 'd' + str(int(res_dict["restDuration"] % 24)) + 'h',
        "legDistance": str(res_dict["legDistance"]) + "nm",
        "pastDistance": str(res_dict["pastDistance"]) + "nm",
        "restDistance": str(res_dict["restDistance"]) + "nm",
        "sailPct": str(format(res_dict["sailPct"] * 100, '.1f')) + "%",
        "currentSpeed": str(res_dict["currentSpeed"]) + "kn",
        "averageSpeed": str(res_dict["averageSpeed"]) + "kn",
        "startBerthCargoTypeName": res_dict["startBerthCargoTypeName"],
        "dailyFuelTotal": res_dict["dailyFuelTotal"],
        "dailyCo2Total": res_dict["dailyCo2Total"],
        "calculateSpeed": res_dict["calculateSpeed"],
    }
    return my_dict


'''
API 	: sdc/v1/vessels/status/track
请求方式	: POST
说明 	: 获取船舶航行轨迹经纬度（截止时间为当前）
返回
经纬度列表
'''


def get_shipTrack_by_code(data):
    # url
    url = f"{URL_PREFIX}/sdc/v1/vessels/status/track"
    # 请求头：没有【User-Agent】会返回405
    headers = {
        'Content-Type': 'application/json',
        "User-Agent": "PostmanRuntime/7.29.2",
        "Authorization": HEADER_AUTHORIZATION
    }
    # 发送请求
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        print(res)
        return None
    res_dict = res.json()["data"]
    lon_lat_list = []
    for lon_lat in res_dict:
        lon_lat_list.append(str(lon_lat["lon"]) + " " + str(lon_lat["lat"]))
    return lon_lat_list


'''
API 	: sdc/v1/routes/predict
请求方式	: POST
说明 	: 获取船舶航行预测轨迹经纬度（预测时间）
返回
经纬度列表
'''


def get_shipTrackPredict_by_code(data):
    # url
    url = f"{URL_PREFIX}/sdc/v1/routes/predict"
    # 请求头：没有【User-Agent】会返回405
    headers = {
        'Content-Type': 'application/json',
        "User-Agent": "PostmanRuntime/7.29.2",
        "Authorization": HEADER_AUTHORIZATION
    }
    # 发送请求
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        print(res)
        return None
    res_dict = res.json()["data"]["restPointsOnLine"]
    lon_lat_list = []
    for lon_lat in res_dict:
        lon_lat_list.append(str(lon_lat["lon"]) + " " + str(lon_lat["lat"]))
    return lon_lat_list
