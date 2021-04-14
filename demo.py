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

	# Print Balances & Rewards
	print("Total Balance in USD: %.09f" % (scraper.get_price() * scraper.get_total_tokens()))
	print("Redistribution rewards in USD: %.09f" % (scraper.get_price() * scraper.get_redistribution()))
	print("Total Balance in CAD: %.09f" % (scraper.get_price('cad') * scraper.get_total_tokens()))
	print("Redistribution rewards in CAD: %.09f" % (scraper.get_price('cad') * scraper.get_redistribution()))
	print("Total Balance in AUD: %.09f" % (scraper.get_price('aud') * scraper.get_total_tokens()))
	print("Redistribution rewards in AUD: %.09f" % (scraper.get_price('aud') * scraper.get_redistribution()))
	print("Total Balance in BTC: %.08f" % (scraper.get_price('btc') * scraper.get_total_tokens()))
	print("Redistribution rewards in BTC: %.08f" % (scraper.get_price('btc') * scraper.get_redistribution()))

if __name__ == '__main__':
	main()
