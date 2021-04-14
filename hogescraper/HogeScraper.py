import json

import requests
from web3 import Web3

class HogeScraper(object):

	def __init__(self, infura_api_key: str, user_address: str = '', hoge_address: str ='0xfad45e47083e4607302aa43c65fb3106f1cd7607'):
		self.set_w3(infura_api_key)
		self.set_abi()
		self.set_user_address(user_address)
		self.set_hoge_address(hoge_address)
		self.set_contract()
		self._contract = self._w3.eth.contract(address=self._hoge_address, abi=self._abi)

	def set_abi(self):
		"""Set contract ABI"""
		self._abi = requests.get('https://raw.githubusercontent.com/HogeFinance/token/main/Contract%20ABI').text

	def set_w3(self, infura_api_key: str):
		"""Instantiate w3 object with infura API key"""
		self._w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/%s' % infura_api_key))

	def set_user_address(self, address: str):
		"""Set address of user to scrape"""
		if self.get_w3().isAddress(address):
			self._user = self.get_w3().toChecksumAddress(address)

	def set_hoge_address(self, address: str):
		"""Set address of Hoge contract"""
		if self.get_w3().isAddress(address):
			self._hoge_address = self.get_w3().toChecksumAddress(address)

	def set_contract(self):
		"""Instantiate contract object"""
		self._contract = self.get_w3().eth.contract(address=self.get_hoge_address(), abi=self.get_abi())

	def get_abi(self) -> str:
		"""Get contract ABI"""
		return self._abi

	def get_w3(self) -> object:
		"""Get w3 Object"""
		return self._w3

	def get_user_address(self) -> str:
		"""Get user address"""
		return self._user

	def get_hoge_address(self) -> str:
		"""Get contract address"""
		return self._hoge_address

	def get_contract(self) -> object:
		"""Return contract object"""
		return self._contract

	def get_buys(self) -> list:
		"""Retrieve list of Transfer events for each purchase"""
		t_filter = self.get_contract().events.Transfer.createFilter(
			fromBlock=0,
			toBlock='latest', 
			argument_filters={
				'to': self.get_user_address()
			}
		)
		return t_filter.get_all_entries()

	def get_bought_tokens(self) -> float:
		"""Get sum of purchased tokens"""
		transfers = self.get_buys()
		buys = [transfer['args']['value'] for transfer in transfers]
		return sum([self.get_w3().fromWei(buy, 'nano') for buy in buys])

	def get_total_tokens(self) -> float:
		"""Get total Hoge balance"""
		return self.get_w3().fromWei(
			self.get_contract().functions.balanceOf(self.get_user_address()).call(), 'nano'
		)

	def get_redistribution(self) -> float:
		"""Calculate redistribution earnings"""
		return self.get_total_tokens() - self.get_bought_tokens()

	def get_price(self, currency: str ='usd') -> float:
		"""Get hoge price in numerous currencies"""
		data = json.loads(
			requests.get(
				'https://api.coingecko.com/api/v3/coins/ethereum/contract/%s' % self.get_hoge_address()
			).text
		)
		return float(data['market_data']['current_price'][currency.lower()])

	def isConnected(self) -> bool:
		"""Check if self._w3 is connected to the blockchain"""
		return self.get_w3().isConnected()