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
        "portCode"	: res_dict["portCode"],		# "CNYAN",
        "nameCn"	: res_dict["nameCn"], 		# "烟台",
        "nameEn"	: res_dict["nameEn"], 		# "YANTAI",
        # "ctryCode"	: res_dict["ctryCode"],		# "CN",
        "ctryNameCn": res_dict["ctryNameCn"],	# "中国",
        "ctryNameEn": res_dict["ctryNameEn"],	# "China",
        # "namePinyin": res_dict["namePinyin"],	# "YANTAI",
        "lon": res_dict["lon"], 		# 121.400000,
        "lat": res_dict["lat"], 		# 37.550000,
	}
	return my_dict
