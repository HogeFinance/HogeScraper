# HogeScraper:
Python Module for scraping Hoge data

HogeScraper is an all-in-one utility to let you track your purchased hoge, current hoge balance(with redistribution rewards), isolate exactly how many redistribution rewards you currently hold, and get the current price in a number of currencies such as: USD, CAD, AUD, BTC, etc...

It currently leverages several sources to get its data. Primarily it reads from the ethereum and xDai blockchains, and as such an [Infura API Key](https://infura.io/), or a local node(lite or full) is required. This allows HogeScraper to filter transfer events sent to your address(your Hoge purchases) as well as query the contract for your current balance. Additionally price data is fed in from coingeckos API.

# Installation:
To install HogeScraper enter the following commands(Windows, Linux, or macOS)
```bash
git clone https://github.com/Durendal/HogeScraper.git
cd HogeScraper
pip install .
```

# Setup a local lite-node:
Make sure you have [installed geth](https://geth.ethereum.org/docs/install-and-build/installing-geth), then enter the following command in a terminal. 
```bash
geth --syncmode "light" --rpcapi eth,web3,debug,txpool,admin --rpc --rpcport=8545
```
Open [etherscan](https://www.etherscan.io) in another window and check what the latest block is. Once the latest block geth shows coincides with etherscan your node should be sync'd(this usually takes a few minutes). Once sync'd you should be able to use the 'local' network for ethereum requests(useful if you don't have a paid Infura subscription)

# Basic Use:

```python
from hogescraper import HogeScraper
from hogescraper.contracts import Contract

def main():
	scraper: HogeScraper = HogeScraper('INFURA_API_KEY')
	address: str = 'ETH_ADDRESS_HOLDING_HOGE'

	hoge_eth: Contract = scraper.network('eth').contract('hoge')
	hoge_xdai: Contract = scraper.network('xdai').contract('hoge')
	
	# Eth network
	print("Symbol: %s" % hoge_eth.symbol)
	print("Name: %s" % hoge_eth.name)
	print("Total Supply: %.09f" % hoge_eth.total_supply)
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
	print("Symbol: %s" % hoge_xdai.symbol)
	print("Name: %s" % hoge_xdai.name)
	print("Total Supply: %.09f" % hoge_xdai.total_supply)
	print("Current Balance: %.09f" % scraper.get_total_tokens(address, 'xdai'))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address, 'xdai'))
	print("Profits: %.09f" % scraper.get_redistribution(address, 'xdai'))

	for currency in ['usd', 'aud', 'cad', 'btc']:
		print("Total Balance in %s: %.09f" % (currency, scraper.convert_total_balance(currency=currency, address=address, network="xdai")))
		print("Redistribution rewards in %s: %.09f" % (currency, scraper.convert_redistribution(currency=currency, address=address, network="xdai")))

if __name__ == '__main__':
	main()
```

# Threading:
HogeScraper should be thread-safe. Each Contract and Chain object has an internal lock that controls access to all state changing methods(also see [get_addr.py](https://github.com/Durendal/HogeScraper/blob/main/get_addrs.py))
```python
from queue import Queue
from threading import Thread

from hogescraper import HogeScraper

def threaded_balance_of(address, scraper):
	while True:
		addr = address.get()
		print("%s balance: %.09f" % (addr, scraper.network('eth').contract('hoge').balance_of(addr)))
		address.task_done()

def main():

	num_threads = 10
	addresses = Queue(maxsize=0)
	scraper = HogeScraper('INFURA_API_KEY')

	# Initialize threads
	threadpool = [Thread(target=threaded_balance_of, args=(addresses, scraper)) for i in range(num_threads)]
	
	# Start threads
	for thread in threadpool:
		thread.setDaemon(True)
		thread.start()

	# Randomly sourced addresses from etherscan and feed queue
	[addresses.put(addr) for addr in [
		'0x947174ed842afe3e7246801f036709743f9ee994',
		'0xedca5d37d33a69b69dff9ccfadc4aa20dc42949d',
		'0xe79ea8f930c475c219fe882cc3a536e9861a2f6a',
		'0xa11584b769ae31c52c9e7a6c559be6c3106b73de',
		'0x4209c80442ac1da6ceb34e77da25cda9b36aaff7',
		'0x0f52dab01d18e1d3bd8876700c4613ff207939dd',
		'0xcbeef760e0be52361a79f9951f1a535238804b26',
		'0xde44f07688f43f48c8af7f18fb8883384a4157a5',
		'0x058409a0d8c12f6e949a4e0f1e6d70ee02f7e574']
	]

	addresses.join()

if __name__ == '__main__':
	main()
```

# Other ERC-20s:
Although HogeScraper will work out of the box with the HOGE smart contract, you can specify a custom ABI and smart contract address to the Contract class, in theory its wrapped methods should work with any ERC-20 however this has not been tested.
```python
from hogescraper import HogeScraper
from hogescraper.contracts import ERC20

def main():
	abi = open('CONTRACT_ABI.json').read()
	contract_address = 'CUSTOM_ERC20_CONTRACT_ADDRESS'
	scraper = HogeScraper('INFURA_API_KEY')
	address = 'YOUR_ETH_ADDRESS_HOLDING_ERC20'
	contract_name = "CONTRACT_NAME"
	scraper.network(name).add_contract(name='hoge', contract=ERC20(w3=scraper.network('eth').w3, abi=abi, address=contract_address))	
		
	# Token info
	print("Symbol: %s" % scraper.network('eth').contract(contract_name).symbol)
	print("Current Balance: %.09f" % scraper.get_total_tokens(address=address, network='eth', contract=contract_name))
	print("Current Buys: %.09f" % scraper.get_bought_tokens(address=address, network='eth', contract=contract_name))
		
if __name__ == '__main__':
	main()
```

# Other Networks:
HogeScraper comes pre-configured to connect to the ethereum and xDai chains, it can programatically add additional chains as long as you specify a provider
```python
from hogescraper import HogeScraper
from hogescraper.providers import Local
from hogescraper.contracts import ERC20

def main():
	name = 'custom chain'
	provider = Local(url='http://localhost', port=8545, name='local')

	abi = open('CONTRACT_ABI.json').read()
	contract_address = 'CUSTOM_ERC20_CONTRACT_ADDRESS'
	address = 'YOUR_ETH_ADDRESS_HOLDING_ERC20'
	contract_name = "CONTRACT_NAME"

	scraper = HogeScraper()
	scraper.add_network(name=name, provider=provider)
	scraper.network(name).add_contract(name=contract_name, contract=ERC20(w3=scraper.network(name).w3, abi=abi, address=contract_address))	

if __name__ == '__main__':
	main()
```

## Donations:
To help support development of this and any other tools I write that you may enjoy, please consider sending a donation to one of the following addresses:

    ETH: 0x1cc56853360Dcf5978FcbFf95E6a64FfB9844A6b
    HOGE: 0x1cc56853360Dcf5978FcbFf95E6a64FfB9844A6b
    BTC: bc1q36ktet78lhhn9ac2nghmqt9ce4h42vfcverc35
    DOGE: DRUjcPML6UhSKumgJwpexe4DWz5H91dwM7  