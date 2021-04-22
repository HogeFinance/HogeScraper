from threading import Lock

from web3 import Web3

from .contracts import Contract, ERC20, ERC721
from .providers import Provider

class Chain(object):

	def __init__(self, provider: Provider, name: str = '') -> None:
		"""Initialize a web3 instance with the given provider for this chain"""
		self.lock: Lock = Lock()
		self.contracts: dict = {}
		self.name: str = name
		self.provider: Provider = provider
		self.set_w3()

	@property
	def lock(self) -> Lock:
		"""Return chain lock"""
		return self._lock

	@lock.setter
	def lock(self, lock: Lock) -> None:
		"""Set chain lock"""
		self._lock: Lock = lock

	@property
	def name(self) -> str:
		"""Return the name of the network"""
		return self._name

	@name.setter
	def name(self, name: str) -> None:
		"""Set the network name"""
		with self.lock:
			self._name: str = name

	@property
	def provider(self) -> Provider:
		"""Return currently set provider"""
		return self._provider

	@provider.setter
	def provider(self, network: Provider) -> None:
		"""Set the network provider to use"""
		with self.lock:
			self._provider: Provider = network

	@property
	def w3(self) -> Web3:
		"""Get w3 Object"""
		return self._w3

	@w3.setter
	def w3(self, w3: Web3) -> None:
		"""Set a new web3 object"""
		self._w3: Web3 = w3

	def set_w3(self) -> None:
		"""Instantiate w3 object with the designated provider"""
		with self.lock:
			self.w3: Web3 = Web3(Web3.HTTPProvider(self.provider.provider(), request_kwargs={'timeout': 120}))

	def add_contract(self, name: str, contract: Contract) -> None:
		"""Add a new contract from this network"""
		with self.lock:
			self._contracts[name]: Contract = contract

	def add_erc20(self, name: str, contract: ERC20) -> None:
		"""Add an ERC20 Contract"""
		self.add_contract(name, contract)

	def add_erc721(self, name:str, contract: ERC721) -> None:
		"""Add an ERC721 Contract"""
		self.add_contract(name, contract)

	def remove_contract(self, name: str) -> bool:
		"""Remove a contract from the networks list of contracts"""
		if name in self._contracts.keys():
			with self._lock:
				del self._contracts[name]
			return True
		return False

	def contract(self, name: str) -> Contract:
		"""Return a given contract for this network"""
		if name in self._contracts.keys():
			return self._contracts[name]
		raise Exception("Contract not found")

	@property
	def contracts(self) -> dict:
		"""Return all contracts associated with this network"""
		return self._contracts

	@contracts.setter
	def contracts(self, contracts: dict) -> None:
		"""Set a dictionary of contracts for the chain"""
		self._contracts = contracts

	@property
	def eth(self) -> 'web3.eth.Eth':
		"""Return web3 eth object"""
		return self.w3.eth

	@property
	def api_key(self) -> str:
		"""Return this network providers API key"""
		return self._api_key

	@api_key.setter
	def api_key(self, api_key: str) -> None:
		self._api_key = api_key