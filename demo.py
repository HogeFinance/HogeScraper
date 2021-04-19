from hogescraper import HogeScraper

def main():
	scraper = HogeScraper('INFURA_API_KEY')
	address = 'ETH_ADDRESS_HOLDING_HOGE'
	
	# Eth network
	print("Symbol: %s" % scraper.network('eth').contract('hoge').symbol())
	print("Name: %s" % scraper.network('eth').contract('hoge').name())
	print("Total Supply: %.09f" % scraper.network('eth').contract('hoge').total_supply())
	print("Current Balance: %.09f" % scraper.get_total_tokens(address, 'eth'))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address, 'eth'))
	print("Profits: %.09f" % scraper.get_redistribution(address, 'eth'))
	print("Total Balance in %s: %.09f" % ('usd', scraper.convert_total_balance(currency='usd', address=address, network='eth')))
	print("Redistribution rewards in %s: %.09f" % ('usd', scraper.convert_redistribution(currency='usd', address=address, network='eth')))

	# xDai network
	print("Symbol: %s" % scraper.network('xdai').contract('hoge').symbol())
	print("Name: %s" % scraper.network('xdai').contract('hoge').name())
	print("Total Supply: %.09f" % scraper.network('xdai').contract('hoge').total_supply())
	print("Current Balance: %.09f" % scraper.get_total_tokens(address, 'xdai'))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address, 'xdai'))
	print("Profits: %.09f" % scraper.get_redistribution(address, 'xdai'))
		
if __name__ == '__main__':
	main()
