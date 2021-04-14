import json

import requests

from .Chain import Chain

class Contract(object):

	def __init__(
		self, 
		infura_api_key: str, 
		contract_address: str ='0xfad45e47083e4607302aa43c65fb3106f1cd7607', 
		abi: str = ''
	):
		self._w3 = Chain(infura_api_key)
		self.set_abi(abi)
		self.set_contract_address(contract_address)
		self.set_contract()

	def w3(self):
		"""Return w3 object"""
		return self._w3

	def set_abi(self, abi: str = None):
		"""Set contract ABI"""
		if not abi:
			abi = requests.get('https://raw.githubusercontent.com/HogeFinance/token/main/Contract%20ABI').text
		self._abi = abi

	def set_contract_address(self, address: str):
		"""Set address of Hoge contract"""
		if self.w3().is_address(address):
			self._contract_address = self.w3().to_checksum_address(address)

	def set_contract(self):
		"""Instantiate contract object"""
		self._contract = self.w3().get_w3().eth.contract(address=self.get_contract_address(), abi=self.get_abi())

	def get_abi(self) -> str:
		"""Get contract ABI"""
		return self._abi

	def get_contract_address(self) -> str:
		"""Get contract address"""
		return self._contract_address

	def get_contract(self) -> object:
		"""Return contract object"""
		return self._contract

	def balance_of(self, address) -> float:
		"""Return balance of `address`"""
		if self.w3().is_address(address):
			address = self.w3().to_checksum_address(address)
			return float(self.w3().from_wei(
				self.get_contract().functions.balanceOf(address).call(), 'nano'
			))

	def symbol(self) -> str:
		"""Return token symbol"""
		return self.get_contract().functions.symbol().call()

	def decimals(self) -> int:
		"""Return decimal points in token"""
		return int(self.get_contract().functions.decimals().call())

	def total_supply(self) -> float:
		"""Return token total supply"""
		return float(self.get_contract().functions.totalSupply().call())

	def name(self) -> str:
		"""Return token name"""
		return self.get_contract().functions.name().call()

	def allowance(self, owner, spender) -> float:
		"""Return allocated allowance from owner to spender"""
		if self.w3().is_address(owner) and self.w3().is_address(spender):
			owner = self.w3().to_checksum_address(owner)
			spender = self.w3().to_checksum_address(spender)
			return float(self.w3().from_wei(
				self.get_contract().functions.allowance(owner, spender).call(), 'nano'
			))


