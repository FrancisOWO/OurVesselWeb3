import wutongchain as wtc


Ship = {
	"中海才华": 477464900,
	"中海海王星": 477598400,
	"远洋7007": 413798964,
}

SC = {
	'name': '73a295a5b15dd9c7ed19b0fa60fe96f10d7ba191450ec62d1012a9313c1146c8',
	'txId': '2c22228b7750ae6aa4ff5e41d824a26eeb0ae2929d09604e1083aad5d209d1db',
	"init": "init_account",  # 初始化
	"transfer": "transfer",  # 转账 参数(string from, string to, float amount)
	"getBlance": "getBlance",  # 余额查询 (string account) account为mmsi，如果查询冻结余额，则为mmsi_frozen
	"changeBlance": "changeBlance",  # 增减余额 (string account, float amount)
	"frozenBlance": "frozenBlance",  # 冻结操作 (string account, float amount)
}

if __name__ == "__main__":
	# 合约安装
	res = wtc.sc_install("carbonTransaction.wvm")
	print(res)
	# 账户初始化
	# res = wtc.sc_invoke(SC['name'], SC["init"], [])
	# print(res)
	# 合约增添
	# res = wtc.sc_invoke(SC["name"], SC["changeBlance"], [str(Ship["中海才华"]), float(-18753.5)])
	# print(res)
	# 合约转账
	# res = wtc.sc_invoke(SC['name'], SC['transfer'], [str(Ship["中海才华"]), str(Ship["中海海王星"]), float(1000)])
	# print(res)
	# 合约查询
	# res = wtc.sc_query(SC['name'], SC['getBlance'], [str(Ship["中海才华"]) + "_frozen"])
	# print(res)
	# 冻结
	# res = wtc.sc_invoke(SC['name'], SC['frozenBlance'], [str(Ship["中海才华"]), float(1000)])
	# print(res)
	# transaction = CarbonTransactionInfoMyself("中远海运", "477464900", 0, -18753.5, "b4d2f795681c906c696b880a20ac8ca210ef083d6293ac228ace8a0608bf347c")
	# db.session.add(transaction)
	# db.session.commit()
