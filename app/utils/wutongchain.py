import requests
import json


HOST = "dev-env.wutongchain.com"
PORT = 49080
LEDGER = "blkc2022"
URL_PREFIX = f"https://{HOST}:{PORT}"
BROWSER_URL = "http://dev-env.wutongchain.com:49082"


def get_host():
	return HOST

def get_port():
	return PORT

def get_ledger_name():
	return LEDGER

def get_url_prefix():
	return URL_PREFIX

def get_browser_url():
	return BROWSER_URL


'''
API 	: /v2/block/height
请求方式	: GET
说明 	: 获取区块链的最新高度
'''
def get_block_height():
	# url
	url = f"{URL_PREFIX}/v2/block/height"

	# GET 参数
	params = {
		"ledger": LEDGER
	}
	# 发送请求
	res = requests.get(url=url, params=params)
	if res.status_code != 200:
		print(res)
		return None
	'''
	res.request.headers	# 请求头
	res.headers 		# 响应头
	res.status_code 	# 状态码
	res.cookies 		# cookie值
	requests.utils.dict_from_cookiejar(res.cookies) # 以字典形式查看cookie
	'''
	res_dict = res.json()
	return res_dict["data"]

'''
API 	: /v2/block/detail/{id}
请求方式	: GET
说明 	: 根据区块ID获取区块详情
'''
def get_block_detail_by_id(blk_id):
	pass

'''
API 	: /v2/block/detail/{height}
请求方式	: GET
说明 	: 根据区块高度获取区块详情
'''
def get_block_detail_by_height(blk_height):
	pass

'''
API 	: /v2/block/height/{txId}
请求方式	: GET
说明 	: 根据交易ID获取交易所在区块高度
'''
def get_block_height_by_txid(txid):
	pass


'''
API 	: /v2/tx/store
请求方式	: POST
说明 	: 发送存证交易
'''
def tx_store():
	pass

'''
API 	: /v2/tx/store/query
请求方式	: POST
说明 	: 获取隐私存证交易内容
'''
def tx_query():
	pass

'''
API 	: /v2/tx/store/querybypubkey
请求方式	: POST
说明 	: 获取隐私存证交易内容（不传私钥）
'''
def tx_query_by_pubkey():
	pass

'''
API 	: /v2/tx/store/authorize
请求方式	: POST
说明 	: 隐私存证授权
'''
def tx_store_auth():
	pass

'''
API 	: /v2/tx/store/authorizebypubkey
请求方式	: POST
说明 	: 隐私存证授权（不传私钥）
'''
def tx_store_auth_by_pubkey():
	pass

'''
API 	: /v2/tx/detail/{txid}
请求方式	: GET
说明 	: 查询交易详情
'''
def get_tx_detail_by_txid(txid):
	pass

'''
API 	: /v2/tx/raw/{txid}
请求方式	: GET
说明 	: 获取交易原始数据（可以查询所有类型交易）
'''
def get_tx_raw_by_txid(txid):
	pass



'''
API 	: /v2/tx/sc/install
请求方式	: POST
说明 	: 安装合约
'''
def sc_install():
	pass

'''
API 	: /v2/tx/sc/invoke
请求方式	: POST
说明 	: 调用合约
'''
def sc_invoke():
	pass

'''
API 	: /v2/tx/sc/query
请求方式	: POST
说明 	: 合约查询
'''
def sc_query():
	pass

'''
API 	: /v2/tx/sc/destory
请求方式	: POST
说明 	: 销毁合约
'''
def sc_destroy():
	pass


'''
API 	: /v2/block/tx/index/{txId}
请求方式	: GET
说明 	: 根据交易ID获取交易在区块的索引
'''
def get_block_index_by_txid(txid):
	pass

'''
API 	: /v2/tx/inlocal/{txId}
请求方式	: GET
说明 	: 根据交易ID查询交易是否同步到数据库
'''
def tx_inlocal_by_txid(txid):
	pass

'''
API 	: /v2/chain/apihealth
请求方式	: GET
说明 	: 获取系统健康状态
'''
def get_chain_apihealth():
	pass

'''
API 	: /health
请求方式	: GET
说明 	: 检测应用链是否可以正常运行
'''
def isOK(txid):
	pass

'''
API 	: /v2/ledger
请求方式	: GET
说明 	: 获取应用链信息
'''
def get_ledger(txid):
	pass

'''
API 	: /v2/memberlist
请求方式	: GET
说明 	: 获取节点列表详细信息
'''
def get_memberlist(txid):
	pass



'''
API 	: /v2/tx/stoken/issue/apply
请求方式	: POST
说明 	: smart token发行申请
'''
def stoken_apply_issue():
	pass

'''
API 	: /v2/tx/stoken/issue/approve
请求方式	: POST
说明 	: smart token发行审核
'''
def stoken_approve_issue():
	pass

'''
API 	: /v2/tx/stoken/transfer/apply
请求方式	: POST
说明 	: smart token转让申请
'''
def stoken_apply_transfer():
	pass

'''
API 	: /v2/tx/stoken/exchange/apply
请求方式	: POST
说明 	: smart token转换申请
'''
def stoken_apply_exchange():
	pass

'''
API 	: /v2/tx/stoken/destroy/apply
请求方式	: POST
说明 	: smart token销毁（回收）申请
'''
def stoken_apply_destroy():
	pass


'''
API 	: /v2/tx/stoken/approve
请求方式	: POST
说明 	: smart token转让、转换、销毁审核
'''
def stoken_approve():
	pass


'''
API 	: /v2/tx/stoken/address/generate
请求方式	: POST
说明 	: 根据公钥生成多签地址
'''
def stoken_gen_address():
	pass

'''
API 	: /v2/tx/stoken/balance
请求方式	: POST
说明 	: 根据地址查询余额
'''
def get_stoken_balance():
	pass

'''
API 	: /v2/tx/stoken/tokentype/freeze
请求方式	: POST
说明 	: smart token冻结
'''
def stoken_freeze():
	pass

'''
API 	: /v2/tx/stoken/tokentype/recover 
请求方式	: POST
说明 	: smart token解冻
'''
def stoken_recover():
	pass



'''
API 	: /v2/event/msg/{height}
请求方式	: GET
说明 	: 根据区块高度查询事件信息
'''
def get_event_msg_by_height(blk_height):
	pass

'''
API 	: /v2/event/msg/tx/{txId}
请求方式	: GET
说明 	: 根据交易ID查询事件信息
'''
def get_event_msg_by_txid(txid):
	pass