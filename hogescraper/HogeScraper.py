from threading import Lock
import json
import os

import requests
from web3 import Web3

from .Chain import Chain

class HogeScraper(object):

	def __init__(self, api_key: str = '', user_address: str = ''):
		self._lock = Lock()
		abi = open('%s/HOGE_ABI.json' % os.path.dirname(os.path.realpath(__file__)), 'r').read()

		self._networks = {
			'eth': {
				'provider': 'https://mainnet.infura.io/v3/%s' % api_key,
				'hoge_addr': '0xfad45e47083e4607302aa43c65fb3106f1cd7607',
			},
			'xdai': {
				'provider': 'https://rpc.xdaichain.com/',
				'hoge_addr': '0xDfF7fcF6a86F7Dc86E7facECA502851f82a349A6'
			}
		}

		self._chains = {
			'eth': Chain(api_key=api_key, name='eth', provider=self._networks['eth']['provider']),
			'xdai': Chain(name='xdai', provider=self._networks['xdai']['provider'])
		}

		# Add Hoge Contracts for ETH and xDai networks
		for name, chain in self._chains.items():
			if self.network(name).w3().isConnected():
				self.network(name).add_contract(name='hoge', abi=abi, address=self._networks[name]['hoge_addr'])

	def add_network(self, name: str, provider: str, api_key: str = ''):
		"""Add a network"""
		with self._lock:
			self._networks[name] = {'provider': provider}
			self._chains[name] = Chain(api_key=api_key, name=name, provider=provider)

	def remove_network(self, name: str):
		"""Remove network"""
		if name in self._networks.keys() and name in self._chains.keys():
			with self._lock:
				del self._networks[name]
				del self._chains[name]

	def network(self, name: str = 'eth') -> Chain:
		"""Return the network instance for `name`"""
		if name in self._chains.keys():
			return self._chains[name]

	def w3(self, network: str = 'eth') -> Web3:
		"""Return w3 object"""
		return self.network(network).w3()

	def get_buys(self, address: str, network: str = 'eth', contract: str = 'hoge') -> list:
		"""Retrieve list of Transfer events for each purchase"""
		if self.w3(network).isAddress(address):
			try:
				t_filter = self.network(network).contract(contract).contract().events.Transfer.createFilter(
					fromBlock=0,
					toBlock='latest', 
					argument_filters={
						'to': self.w3(network).toChecksumAddress(address)
					}
				)
				return t_filter.get_all_entries()
			except ValueError as e:
				print("Error: %s" % e)
				return []

	def get_bought_tokens(self, address: str, network: str = 'eth', contract: str = 'hoge') -> float:
		"""Get sum of purchased tokens"""
		transfers = self.get_buys(address, network, contract)
		buys = [transfer['args']['value'] for transfer in transfers]
		return float(sum([self.w3(network).fromWei(buy, 'nano') for buy in buys]))

	def get_total_tokens(self, address: str, network: str = 'eth', contract: str = 'hoge') -> float:
		"""Get total Hoge balance"""
		if self.w3(network).isAddress(address):
			return float(self.w3(network).fromWei(
				self.network(network).contract(contract).contract().functions.balanceOf(self.w3(network).toChecksumAddress(address)).call(), 'nano'
			))

	def get_redistribution(self, address: str, network: str = 'eth', contract: str = 'hoge') -> float:
		"""Calculate redistribution earnings"""
		return float(self.get_total_tokens(address, network, contract) - self.get_bought_tokens(address, network, contract))

	def get_price(self, currency: str = 'usd', network: str = 'eth', contract: str = 'hoge') -> float:
		"""Get hoge price in numerous currencies"""
		data = json.loads(
			requests.get(
				'https://api.coingecko.com/api/v3/coins/ethereum/contract/%s' % self._networks['eth']['hoge_addr']
			).text
		)
		return float(data['market_data']['current_price'][currency.lower()])

	def convert_total_balance(self, address: str, network: str = 'eth', contract: str = 'hoge', currency: str = 'usd') -> float:
		"""Convert value of all held tokens to `currency`"""
		return float(self.get_price(currency) * self.get_total_tokens(address, network, contract))

	def convert_redistribution(self, address: str, network: str = 'eth', contract: str = 'hoge', currency: str = 'usd') -> float:
		"""Convert value of all held redistribution rewards to `currency`"""
		return float(self.get_price(currency) * self.get_redistribution(address, network, contract))
