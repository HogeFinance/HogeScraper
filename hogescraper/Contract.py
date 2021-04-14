import json

import requests
from web3 import Web3

class Contract(object):

	def __init__(
		self, 
		infura_api_key: str, 
		contract_address: str ='0xfad45e47083e4607302aa43c65fb3106f1cd7607', 
		abi: str = ''
	):
		self.set_w3(infura_api_key)
		self.set_abi(abi)
		self.set_contract_address(contract_address)
		self.set_contract()

	def set_abi(self, abi=None):
		"""Set contract ABI"""
		if not abi:
			abi = requests.get('https://raw.githubusercontent.com/HogeFinance/token/main/Contract%20ABI').text
		self._abi = abi

	def set_w3(self, infura_api_key: str):
		"""Instantiate w3 object with infura API key"""
		self._w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/%s' % infura_api_key))

	def set_contract_address(self, address: str):
		"""Set address of Hoge contract"""
		if self.get_w3().isAddress(address):
			self._contract_address = self.get_w3().toChecksumAddress(address)

	def set_contract(self):
		"""Instantiate contract object"""
		self._contract = self.get_w3().eth.contract(address=self.get_contract_address(), abi=self.get_abi())

	def get_abi(self) -> str:
		"""Get contract ABI"""
		return self._abi

	def get_w3(self) -> object:
		"""Get w3 Object"""
		return self._w3

	def get_contract_address(self) -> str:
		"""Get contract address"""
		return self._contract_address

	def get_contract(self) -> object:
		"""Return contract object"""
		return self._contract

	def balance_of(self, address):
		"""Return balance of `address`"""
		if self.get_w3().isAddress(address):
			address = self.get_w3().toChecksumAddress(address)
			return self.get_w3().fromWei(
				self.get_contract().functions.balanceOf(address).call(), 'nano'
			)

	def symbol(self):
		"""Return token symbol"""
		return self.get_contract().functions.symbol().call()

	def decimals(self):
		"""Return token symbol"""
		return self.get_contract().functions.decimals().call()

	def total_supply(self):
		"""Return token symbol"""
		return self.get_contract().functions.totalSupply().call()

	def name(self):
		"""Return token symbol"""
		return self.get_contract().functions.name().call()

	def allowance(self, owner, spender):
		"""Return token symbol"""
		if self.get_w3().isAddress(owner) and self.get_w3().isAddress(spender):
			owner = self.get_w3().toChecksumAddress(owner)
			spender = self.get_w3().toChecksumAddress(spender)
			return self.get_w3().fromWei(
				self.get_contract().functions.allowance(owner, spender).call(), 'nano'
			)

	def isConnected(self) -> bool:
		"""Check if self._w3 is connected to the blockchain"""
		return self.get_w3().isConnected()

