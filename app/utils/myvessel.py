import requests
import json

from app.utils.config import HEADER_AUTHORIZATION

# 这是直接访问【船视宝】的url，【船视宝】可以查港口信息，中远的api不能
HOST = "voc.myvessel.cn"
URL_PREFIX = f"https://{HOST}"

# 中远api
SVC_HOST = "svc.data.myvessel.cn"
SVC_URL_PREFIX = f"https://{SVC_HOST}"


def get_host():
    return HOST


def get_url_prefix():
    return URL_PREFIX


# 经纬度【小数（十进制）=>度/分/秒（60进制）】
def cvtDec2B60(dec):
    r = int(dec)
    dec = 60*(dec-r)
    m = int(dec)
    s = int(60*(dec-m))
    return f"{r}°{m}′{s}″"


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
        "lonStr": cvtDec2B60(res_dict["lon"]),  # 121°24′00″,
        "latStr": cvtDec2B60(res_dict["lat"]),  # 37°33′00″,
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
        "dwt": res_dict["dwt"],  # 船舶载重吨
        "length_width_height": str(res_dict["length"]) + "m*" + str(res_dict["width"]) + "m*" + str(
            res_dict["height"]) + "m",  # 船舶长宽高
        "buildYearMonth": res_dict["buildYearMonth"][:4] + "-" + res_dict["buildYearMonth"][-2:],
        "draught_speed": str(format(res_dict["draught"], '.1f')) + 'm/' + str(res_dict["speed"]) + "kn",
        "ship_type": res_dict["vesselSub2TypeNameCn"],
        "ship_nameCn": res_dict["nameCn"],
        "ship_nameEn": res_dict["nameEn"],

        "vesselTypeNameCn": res_dict["vesselTypeNameCn"],   # 船舶类型：干散货
        "operatorBodyCn": res_dict["operatorBodyCn"],       # 所属公司：中远海运散货运输有限公司
        "vesselTypeFullNameCn": res_dict["vesselTypeFullNameCn"],   # 船舶类型全称
        "imo": res_dict["imo"],           # imo
        "callsign": res_dict["callsign"], # 呼号
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

    ship_status = {
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
        "legDistance": res_dict["legDistance"],
        "pastDistance": res_dict["pastDistance"],
        "restDistance": res_dict["restDistance"],
        "sailPct": str(format(res_dict["sailPct"] * 100, '.1f')) + "%",
        "currentSpeed": str(res_dict["currentSpeed"]) + "kn",
        "averageSpeed": str(res_dict["averageSpeed"]) + "kn",
        "startBerthCargoTypeName": res_dict["startBerthCargoTypeName"],
        "dailyFuelTotal": res_dict["dailyFuelTotal"],
        "dailyCo2Total": res_dict["dailyCo2Total"],
        "calculateSpeed": res_dict["calculateSpeed"],
    }
    return ship_status


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


# 返回坐标列表，而不是字符串
def get_shipTrackList_by_code(data):
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
        lon_lat_list.append([lon_lat["lon"], lon_lat["lat"]])
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


# 返回坐标列表，而不是字符串
def get_shipTrackPredictList_by_code(data):
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
        lon_lat_list.append([lon_lat["lon"],lon_lat["lat"]])
    return lon_lat_list


'''
API 	: sdc/v1/bi/lcdaily/stats/his
请求方式	: POST
说明 	: 获取船舶航行碳排放等数据
返回
'''


def get_shipCarbon_by_code(data):
    # url
    url = f"{URL_PREFIX}/sdc/v1/bi/lcdaily/stats/his"
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
    if not res_dict:
        return None
    ship_carbon_output_data = {
        "date": [],
        "carbon_data": [],
        "fuel_data": [],
        "date_predict": [],
        "carbon_data_predict": [],
        "fuel_data_predict": [],
    }
    fuel_hundred_ais_total = 0
    fuel_hundred_ais_total_co2 = 0
    fuel_hundred_ais_total_co2_predict = 0
    fuel_hundred_ais_total_predict = 0
    for data in res_dict:
        if data["isPredict"]:
            ship_carbon_output_data["date_predict"].append(str(data["inputDate"][5:10]))
            ship_carbon_output_data["carbon_data_predict"].append(data["dailyFuelAisCo2"])
            ship_carbon_output_data["fuel_data_predict"].append(data["dailyFuelAis"])
            fuel_hundred_ais_total_co2_predict = data["fuelTermHundredAisTotalCo2"]
            fuel_hundred_ais_total_predict = data["fuelTermHundredAisTotal"]
        else:
            ship_carbon_output_data["date"].append(data["inputDate"][5:10])
            ship_carbon_output_data["carbon_data"].append(data["dailyFuelAisCo2"])
            ship_carbon_output_data["fuel_data"].append(data["dailyFuelAis"])
            fuel_hundred_ais_total_co2 = data["fuelTermHundredAisTotalCo2"]
            fuel_hundred_ais_total = data["fuelTermHundredAisTotal"]
    ship_carbon_output_data["carbon_change"] = format(fuel_hundred_ais_total_co2_predict - fuel_hundred_ais_total_co2, '.2f')
    ship_carbon_output_data["fuel_change"] = format(fuel_hundred_ais_total_predict - fuel_hundred_ais_total,
                                                      '.2f')
    return ship_carbon_output_data


'''
API 	: sdc/v1/bi/simulator/cii/leg
请求方式	: POST
说明 	: 获取船舶航行CII数据
返回
'''


def get_shipCII_by_code(data):
    # url
    url = f"{URL_PREFIX}/sdc/v1/bi/simulator/cii/leg"
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

    return res_dict


'''
API 	: sdc/v1/vessels/analytics/efficiency/batch
请求方式	: POST
说明 	: 获取船舶航行数据
返回
sailDistance    : 本年度航行距离
sailDuration    ：本年度航行时间
moorDurationPort    ：本年度锚泊时长
berthDuration   ：本年度靠泊时长
sailRate    ：航行时间占比
moorDurationPortRate    ：锚泊时长占比

'''


def get_shipSailData_by_code(data):
    # url
    url = f"{URL_PREFIX}/sdc/v1/vessels/analytics/efficiency/batch"
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
    my_dict = {
        "sailDistance": res_dict["sailDistance"],
        "sailDuration": str(int(res_dict["sailDuration"] / 24)) + 'd' + str(int(res_dict["sailDuration"] % 24)) + 'h',
        "moorDurationPort": str(int((res_dict["moorDurationPort"] + + res_dict["moorDurationHalfway"]) / 24)) + 'd' + str(int((res_dict["moorDurationPort"] + res_dict["moorDurationHalfway"]) % 24)) + 'h',
        "berthDuration": str(int(res_dict["berthDuration"] / 24)) + 'd' + str(int(res_dict["berthDuration"] % 24)) + 'h',
        "sailRate": format(float(res_dict["sailRate"][:-1]) / 100, '.2f'),
        "moorDurationPortRate": format((float(res_dict["moorDurationPortRate"][:-1]) + float(res_dict["moorDurationHalfwayRate"][:-1])) / 100, '.2f'),
        "berthRate": format(float(res_dict["berthRate"][:-1]) / 100, '.2f'),
        "avgSpeed": res_dict["avgSpeed"],
    }
    return my_dict



'''
API     : /ada/oauth/token
请求方式    : GET
说明  : 获取token
返回
'''


def get_access_token():
    # url
    url = f"{SVC_URL_PREFIX}/ada/oauth/token"

    # 参数
    params = {
        'grant_type': 'client_credentials',
        "client_id": "VVV_UNIVERSITY_API01",
        "client_secret": "8070a482f6ba0c5310984281df52508e"
    }
    # 发送请求
    res = requests.get(url=url, params=params)
    if res.status_code != 200:
        print(res)
        return None

    res_dict = res.json()
    # print(res_dict)

    token = f"{res_dict['token_type']} {res_dict['access_token']}"
    return token


# token 过期后需重新请求
global TEMP_TOKEN
TEMP_TOKEN = get_access_token()


'''
API     : /sdc/v1/ports/holiday/lis
请求方式    : POST
说明  : 获取某年某月的假期信息
返回
'''


def get_holiday_list(ctryCodes, year, month):
    # url
    url = f"{SVC_URL_PREFIX}/sdc/v1/ports/holiday/list"

    # 请求头
    global TEMP_TOKEN
    headers = {
        'Content-Type': 'application/json',
        "Authorization": TEMP_TOKEN
    }
    # 数据
    data = {
      "ctryCodes": ctryCodes,
      "dataSource": "Timeanddate",
      "holidayType": "",
      "month": month,
      "portCodes": [],
      "year": year,
      "pageNum": 0,
      "pageSize": 31
    }
    # 发送请求
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        print(res)
        if res.status_code == 401:
            # token 过期，重新请求
            TEMP_TOKEN = get_access_token()
            headers["Authorization"] = TEMP_TOKEN
            res = requests.post(url=url, data=json.dumps(data), headers=headers)
            print(res)
        # 第二次请求失败，不再重新请求
        if res.status_code != 200:
            return None

    if res.json()["success"] == False:
        return None

    res_dict = res.json()["data"]

    holiday_list = []
    for holidays in res_dict:
        sameTimeHolidays = []
        for holiday in holidays["sameTimeHolidays"]:
            holiday_info = {
                "holidayNameEn": holiday["holidayNameEn"],
                "holidayType": holiday["holidayType"]
            }
            print(holiday_info)
            sameTimeHolidays.append(holiday_info)
        holidays_info = {
            "dateDay": holiday["dateDay"],
            "holidays": sameTimeHolidays
        }
        holiday_list.append(holidays_info)
    
    # print(holiday_list)
    return holiday_list


'''
API     : /sdc/v1/ports/weather/batch/forecast
请求方式    : POST
说明  : 获取港口天气
返回
'''


def get_forecast(portCodes):
    # url
    url = f"{SVC_URL_PREFIX}/sdc/v1/ports/weather/batch/forecast"

    # 请求头
    global TEMP_TOKEN
    headers = {
        'Content-Type': 'application/json',
        "Authorization": TEMP_TOKEN
    }
    # 数据
    data = {
      "portCodes": portCodes,
    }
    # 发送请求
    res = requests.post(url=url, data=json.dumps(data), headers=headers)
    if res.status_code != 200:
        print(res)
        if res.status_code == 401:
            # token 过期，重新请求
            TEMP_TOKEN = get_access_token()
            headers["Authorization"] = TEMP_TOKEN
            res = requests.post(url=url, data=json.dumps(data), headers=headers)
            print(res)
        # 第二次请求失败，不再重新请求
        if res.status_code != 200:
            return None

    if res.json()["success"] == False:
        print("success: False")
        return None

    res_dict = res.json()["data"][0]

    current_dict = res_dict["current"]
    current_weather = current_dict["weathers"][0]
    ret_current_dict = {
        "description": current_weather["description"], # "阴，多云",
        "iconData":  current_weather["iconData"],
        "windSpeed": current_dict["windSpeed"], # 10.33,
        "windSpeedLevel": current_dict["windSpeedLevel"], # "5",
        "windDeg": current_dict["windDeg"],     #  15,
        "windDegCn": current_dict["windDegCn"], # "东北偏北",
        "pressure": current_dict["pressure"], # 1024,
        "humidity": current_dict["humidity"], # 89,
        "feelLike": round(current_dict["fellLike"]["feelLike"]), #  14.15,
        "temp": round(current_dict["temperature"]["temp"]), # 14.34,
    }
    print(ret_current_dict["description"])

    # 每个属性存一个列表，便于画图
    dayWeekDescCn_list = []
    description_list = []
    iconData_list = []
    tempMax_list = []
    tempMin_list = []

    for forecast_dict in res_dict["forecastDetail"]:
        forecast_weather = forecast_dict["weathers"][0]
        # ret_forecast_dict = {
        #     "dayWeekDescCn": forecast_dict["dayWeekDescCn"], # "星期日",
        #     "description": forecast_weather["description"], # "中雨",
        #     "iconData":  forecast_weather["iconData"],
        #     "tempMax": forecast_dict["temperature"]["max"], # 14.34,
        #     "tempMin": forecast_dict["temperature"]["min"], # 11.8,
        # }
        dayWeekDescCn_list.append(forecast_dict["dayWeekDescCn"])
        description_list.append(forecast_weather["description"])
        iconData_list.append(forecast_weather["iconData"])
        tempMax_list.append(round(forecast_dict["temperature"]["max"]))
        tempMin_list.append(round(forecast_dict["temperature"]["min"]))
    
    ret_dict = {
        "current": ret_current_dict,
        "forecastDetail": {
            "dayWeekDescCn": dayWeekDescCn_list,
            "description": description_list,
            "iconData":  iconData_list,
            "tempMax": tempMax_list,
            "tempMin": tempMin_list,
        }
    }

    print(ret_dict["forecastDetail"]["dayWeekDescCn"])
    print(ret_dict["forecastDetail"]["description"])
    return ret_dict
