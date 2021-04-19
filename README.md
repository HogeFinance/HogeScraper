# HogeScraper:
Python Module for scraping Hoge data

HogeScraper is an all-in-one utility to let you track your purchased hoge, current hoge balance(with redistribution rewards), isolate exactly how many redistribution rewards you currently hold, and get the current price in a number of currencies such as: USD, CAD, AUD, BTC, etc...

It currently leverages several sources to get its data. Primarily it reads from the ethereum and xDai blockchains, and as such an [Infura API Key](https://infura.io/) is required. This allows HogeScraper to filter transfer events sent to your address(your Hoge purchases) as well as query the contract for your current balance. Additionally price data is fed in from coingeckos API.

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
	address = 'ETH_ADDRESS_HOLDING_HOGE'
	
	# Eth network
	print("Symbol: %s" % scraper.network('eth').contract('hoge').symbol())
	print("Name: %s" % scraper.network('eth').contract('hoge').name())
	print("Total Supply: %.09f" % scraper.network('eth').contract('hoge').total_supply())
	print("Current Balance: %.09f" % scraper.get_total_tokens(address))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address))
	print("Profits: %.09f" % scraper.get_redistribution(address))
	
	for currency in ['usd', 'aud', 'cad', 'btc']:
		print("Total Balance in %s: %.09f" % (currency, scraper.convert_total_balance(currency=currency, address=address)))
		print("Redistribution rewards in %s: %.09f" % (currency, scraper.convert_redistribution(currency=currency, address=address)))

	print()

	# xDai network
	print("Symbol: %s" % scraper.network('xdai').contract('hoge').symbol())
	print("Name: %s" % scraper.network('xdai').contract('hoge').name())
	print("Total Supply: %.09f" % scraper.network('xdai').contract('hoge').total_supply())
	print("Current Balance: %.09f" % scraper.get_total_tokens(address, 'xdai'))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address, 'xdai'))
	print("Profits: %.09f" % scraper.get_redistribution(address, 'xdai'))

	for currency in ['usd', 'aud', 'cad', 'btc']:
		print("Total Balance in %s: %.09f" % (currency, scraper.convert_total_balance(currency=currency, address=address, network="xdai")))
		print("Redistribution rewards in %s: %.09f" % (currency, scraper.convert_redistribution(currency=currency, address=address, network="xdai")))

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
	address = 'YOUR_ETH_ADDRESS_HOLDING_ERC20'
	contract_name = "CONTRACT_NAME"
	scraper.network('eth').add_contract(name=contract_name, abi=abi, address=contract_address)
	
	# Token info
	print("Symbol: %s" % scraper.network('eth').contract(contract_name).symbol())
	print("Current Balance: %.09f" % scraper.get_total_tokens(address=address, network='eth', contract=contract_name))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address=address, network='eth', contract=contract_name))
		
if __name__ == '__main__':
	main()
```

# Other Networks:
HogeScraper comes pre-configured to connect to the ethereum and xDai chains, it can programatically add additional chains as long as you specify a provider
```python
from hogescraper import HogeScraper

def main():
	name = 'custom chain'
	provider = 'http://localhost:8545'
	api_key = 'API_KEY'

	abi = open('CONTRACT_ABI.json').read()
	contract_address = 'CUSTOM_ERC20_CONTRACT_ADDRESS'
	address = 'YOUR_ETH_ADDRESS_HOLDING_ERC20'
	contract_name = "CONTRACT_NAME"

	scraper = HogeScraper()
	scraper.add_network(name=name, provider=provider, api_key=api_key)
	scraper.network(name).add_contract(name=contract_name, abi=abi, address=contract_address)

if __name__ == '__main__':
	main()
```

## Donations:
To help support development of this and any other tools I write that you may enjoy, please consider sending a donation to one of the following addresses:

    ETH: 0x1cc56853360Dcf5978FcbFf95E6a64FfB9844A6b
    HOGE: 0x1cc56853360Dcf5978FcbFf95E6a64FfB9844A6b
    BTC: bc1q36ktet78lhhn9ac2nghmqt9ce4h42vfcverc35
    DOGE: DRUjcPML6UhSKumgJwpexe4DWz5H91dwM7  