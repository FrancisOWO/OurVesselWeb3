import wutongchain as wtc

if __name__ == "__main__":
	blk_height =  wtc.get_block_height()
	print("区块高度:", blk_height)