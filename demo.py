from hogescraper import HogeScraper

def main():
	scraper: HogeScraper = HogeScraper('INFURA_API_KEY')
	address: str = 'ETH_ADDRESS_HOLDING_HOGE'
	
	# Eth network
	print("Symbol: %s" % scraper.network('eth').contract('hoge').symbol)
	print("Name: %s" % scraper.network('eth').contract('hoge').name)
	print("Total Supply: %.09f" % scraper.network('eth').contract('hoge').total_supply)
	print("Current Balance: %.09f" % scraper.get_total_tokens(address))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address))
	print("Profits: %.09f" % scraper.get_redistribution(address))
	print("Price in USD: %.09f" % scraper.get_price())
	print("Price in CAD: %.09f" % scraper.get_price('cad'))
	print("Price in AUD: %.09f" % scraper.get_price('aud'))
	for currency in ['usd', 'aud', 'cad', 'btc']:
		print("Total Balance in %s: %.09f" % (currency, scraper.convert_total_balance(currency=currency, address=address)))
		print("Redistribution rewards in %s: %.09f" % (currency, scraper.convert_redistribution(currency=currency, address=address)))

	print()

	# xDai network
	print("Symbol: %s" % scraper.network('xdai').contract('hoge').symbol)
	print("Name: %s" % scraper.network('xdai').contract('hoge').name)
	print("Total Supply: %.09f" % scraper.network('xdai').contract('hoge').total_supply)
	print("Current Balance: %.09f" % scraper.get_total_tokens(address, 'xdai'))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address, 'xdai'))
	print("Profits: %.09f" % scraper.get_redistribution(address, 'xdai'))

	for currency in ['usd', 'aud', 'cad', 'btc']:
		print("Total Balance in %s: %.09f" % (currency, scraper.convert_total_balance(currency=currency, address=address, network="xdai")))
		print("Redistribution rewards in %s: %.09f" % (currency, scraper.convert_redistribution(currency=currency, address=address, network="xdai")))

if __name__ == '__main__':
	main()
