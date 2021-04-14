# HogeScraper:
Python Module for scraping Hoge data

HogeScraper is an all-in-one utility to let you track your purchased hoge, current hoge balance(with redistribution rewards), isolate exactly how many redistribution rewards you currently hold, and get the current price in a number of currencies such as: USD, CAD, AUD, BTC, etc...

It currently leverages several sources to get its data. Primarily it reads from the ethereum blockchain, and as such an [Infura API Key](https://infura.io/) is required. This allows HogeScraper to filter transfer events sent to your address(your Hoge purchases) as well as query the contract for your current balance. Additionally price data is fed in from coingeckos API.

# Basic Use:

```python
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
```

Future versions may include the ability to run off a local full node instead of infura. More documentation to come.