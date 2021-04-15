# HogeScraper:
Python Module for scraping Hoge data

HogeScraper is an all-in-one utility to let you track your purchased hoge, current hoge balance(with redistribution rewards), isolate exactly how many redistribution rewards you currently hold, and get the current price in a number of currencies such as: USD, CAD, AUD, BTC, etc...

It currently leverages several sources to get its data. Primarily it reads from the ethereum blockchain, and as such an [Infura API Key](https://infura.io/) is required. This allows HogeScraper to filter transfer events sent to your address(your Hoge purchases) as well as query the contract for your current balance. Additionally price data is fed in from coingeckos API.

# Installation:
To install HogeScraper enter the following commands(Windows, Linux, or macOS)
```bash
git clone https://github.com/Durendal/HogeScraper.git
cd HogeScraper
pip install .
```

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
		print("Total Balance in %s: %.09f" % (currency, scraper.convert_total_balance(currency)))
		print("Redistribution rewards in %s: %.09f" % (currency, scraper.convert_redistribution(currency)))
		
if __name__ == '__main__':
	main()
```

# Other ERC-20s:
Although HogeScraper will work out of the box with the HOGE smart contract, you can specify a custom ABI and smart contract address to the Contract class, in theory its wrapped methods should work with any ERC-20 however this has not been tested.
```python
from hogescraper import HogeScraper

def main():
	abi = open('CONTRACT_ABI.json').read()
	contract_address = 'CUSTOM_ERC20_CONTRACT_ADDRESS'
	scraper = HogeScraper('INFURA_API_KEY')
	scraper.set_user_address('YOUR_ETH_ADDRESS_HOLDING_ERC20')
	scraper.contract().set_abi(abi)
	scraper.contract().set_contract_address(contract_address)
	scraper.contract().set_contract()

	# Token info
	print("Symbol: %s" % scraper.contract().symbol())
	print("Current Balance: %.09f" % scraper.get_total_tokens())
	print("Current Buys: %.09f" % scraper.get_bought_tokens())
		
if __name__ == '__main__':
	main()
```

Future versions may include the ability to run off a local full node instead of infura. More documentation to come.

## Donations:
To help support development of this and any other tools I write that you may enjoy, please consider sending a donation to one of the following addresses:

    ETH: 0x1cc56853360Dcf5978FcbFf95E6a64FfB9844A6b
    HOGE: 0x1cc56853360Dcf5978FcbFf95E6a64FfB9844A6b
    BTC: bc1q36ktet78lhhn9ac2nghmqt9ce4h42vfcverc35
    DOGE: DRUjcPML6UhSKumgJwpexe4DWz5H91dwM7  