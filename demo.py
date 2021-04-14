from hogescraper import HogeScraper

def main():
	scraper = HogeScraper('INFURA_API_KEY')
	scraper.set_user_address('YOUR_ETH_ADDRESS_HOLDING_HOGE')

	# Token info
	print("Symbol: %s" % scraper.contract().symbol())
	print("Current Balance: %.09f" % scraper.get_total_tokens())
	print("Current Buys: %.09f" % scraper.get_bought_tokens())
	print("Profits: %.09f" % scraper.get_redistribution())

	# Print Prices
	print("Price in USD: %.09f" % scraper.get_price())
	print("Price in CAD: %.09f" % scraper.get_price('cad'))
	
	# Print Balances and Rewards
	for currency in ['usd', 'cad', 'aud', 'btc']:
		print("Total Balance in %s: %.09f" % (currency, (scraper.get_price(currency) * scraper.get_total_tokens())))
		print("Redistribution rewards in %s: %.09f" % (currency, (scraper.get_price(currency) * scraper.get_redistribution())))
		
if __name__ == '__main__':
	main()
