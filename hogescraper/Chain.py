from threading import Lock

from web3 import Web3

from .contracts import Contract, ERC20, ERC721
from .providers import Provider

class Chain(object):

	def __init__(self, provider: Provider, name: str = ''):
		self._lock = Lock()
		self._contracts = {}
		self.set_name(name)
		self.set_provider(provider)
		self.set_w3()

	def set_name(self, name: str):
		"""Set the network name"""
		with self._lock:
			self._name = name

	def set_provider(self, network: Provider):
		"""Set the network provider to use"""
		with self._lock:
			self._provider = network

	def set_w3(self):
		"""Instantiate w3 object with the designated provider"""
		with self._lock:
			self._w3 = Web3(Web3.HTTPProvider(self.provider().provider()))

	def add_contract(self, name: str, contract: Contract):
		"""Add a new contract from this network"""
		with self._lock:
			self._contracts[name] = contract

	def add_erc20(self, name: str, contract: ERC20):
		"""Add an ERC20 Contract"""
		self.add_contract(name, contract)

	def add_erc721(self, name:str, contract: ERC721):
		"""Add an ERC721 Contract"""
		self.add_contract(name, contract)

	def remove_contract(self, name) -> bool:
		"""Remove a contract from the networks list of contracts"""
		if name in self._contracts.keys():
			with self._lock:
				del self._contracts[name]
			return True
		return False

	def contract(self, name: str) -> object:
		"""Return a given contract for this network"""
		if name in self._contracts.keys():
			return self._contracts[name]
		raise Exception("Contract not found")

	def contracts(self) -> object:
		"""Return all contracts associated with this network"""
		return self._contracts

	def name(self) -> str:
		"""Return the name of the network"""
		return self._name

	def api_key(self) -> str:
		"""Return this network providers API key"""
		return self._api_key

	def provider(self) -> Provider:
		"""Return currently set provider"""
		return self._provider

	def w3(self) -> Web3:
		"""Get w3 Object"""
		return self._w3
