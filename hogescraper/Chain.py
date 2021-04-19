from threading import Lock

from web3 import Web3

from .Contract import Contract

class Chain(object):

	def __init__(self, api_key: str = '', name: str = '', provider: str = ''):
		self._lock = Lock()
		self._contracts = {}
		self.set_api_key(api_key)
		self.set_name(name)
		self.set_provider(provider)
		self.set_w3()

	def set_name(self, name: str):
		"""Set the network name"""
		with self._lock:
			self._name = name

	def set_api_key(self, api_key: str):
		"""Set API Key for this network provider"""
		with self._lock:
			self._api_key = api_key

	def set_provider(self, network: str):
		"""Set the network provider to use"""
		with self._lock:
			self._provider = network

	def set_w3(self):
		"""Instantiate w3 object with the designated provider"""
		with self._lock:
			self._w3 = Web3(Web3.HTTPProvider(self.provider()))

	def add_contract(self, name: str, abi: str, address: str):
		"""Add a new contract from this network"""
		with self._lock:
			self._contracts[name] = Contract(w3=self.w3(), abi=abi, address=address)

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

	def provider(self) -> str:
		"""Return currently set provider"""
		return self._provider

	def w3(self) -> Web3:
		"""Get w3 Object"""
		return self._w3
