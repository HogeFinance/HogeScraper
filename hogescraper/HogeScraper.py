import json

import requests

from .Contract import Contract

class HogeScraper(object):

	def __init__(self, infura_api_key: str, user_address: str = ''):
		self._contract = Contract(infura_api_key)
		self.set_user_address(user_address)

	def contract(self):
		"""Return contract wrapper object"""
		return self._contract

	def w3(self):
		"""Return w3 wrapper object"""
		return self.contract().w3()

	def set_user_address(self, address: str):
		"""Set address of user to scrape"""
		if self.w3().is_address(address):
			self._user = self.w3().to_checksum_address(address)

	def get_user_address(self) -> str:
		"""Get user address"""
		return self._user

	def get_buys(self) -> list:
		"""Retrieve list of Transfer events for each purchase"""
		t_filter = self.contract().get_contract().events.Transfer.createFilter(
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
		return float(sum([self.w3().from_wei(buy, 'nano') for buy in buys]))

	def get_total_tokens(self) -> float:
		"""Get total Hoge balance"""
		return float(self.w3().from_wei(
			self.contract().get_contract().functions.balanceOf(self.get_user_address()).call(), 'nano'
		))

	def get_redistribution(self) -> float:
		"""Calculate redistribution earnings"""
		return float(self.get_total_tokens() - self.get_bought_tokens())

	def get_price(self, currency: str = 'usd') -> float:
		"""Get hoge price in numerous currencies"""
		data = json.loads(
			requests.get(
				'https://api.coingecko.com/api/v3/coins/ethereum/contract/%s' % self.contract().get_contract_address()
			).text
		)
		return float(data['market_data']['current_price'][currency.lower()])

	def convert_total_balance(self, currency: str = 'usd') -> float:
		"""Convert value of all held tokens to `currency`"""
		return float(self.get_price(currency) * self.get_total_tokens())

	def convert_redistribution(self, currency: str = 'usd') -> float:
		"""Convert value of all held redistribution rewards to `currency`"""
		return float(self.get_price(currency) * self.get_redistribution())
