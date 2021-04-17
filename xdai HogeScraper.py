from hogescraper import HogeScraper

def main():
	abi = open('CONTRACT_ABI.json').read()
	contract_address = '0xDfF7fcF6a86F7Dc86E7facECA502851f82a349A6'
	scraper = HogeScraper('ANKR_API_ENDPOINT')
	scraper.set_user_address('XDAI_HOGE_WALLET')
	scraper.contract().set_abi(abi)
	scraper.contract().set_contract_address(contract_address)
	scraper.contract().set_contract()

	# Token info
	print("Symbol: %s" % scraper.contract().symbol())
	print("Current Balance: %.09f" % scraper.get_total_tokens())
	#print("Current Buys: %.09f" % scraper.get_bought_tokens())
		
if __name__ == '__main__':
	main()
