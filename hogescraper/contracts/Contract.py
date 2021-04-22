from threading import Lock

from web3 import Web3

class Contract(object):

	def __init__(
		self,
		w3: Web3,
		address: str,
		abi: str = ''
	) -> None:
		"""Instantiate contract on network defined by the passed in Web3 instance"""
		self.lock: Lock = Lock()
		self.w3: Web3 = w3
		self.abi: str = abi
		self.contract_address: str = address
		self.set_contract()

	@property
	def lock(self) -> Lock:
		"""Return the Contract lock"""
		return self._lock

	@lock.setter
	def lock(self, lock: Lock) -> None:
		"""Set the Contract lock"""
		self._lock = lock

	@property
	def abi(self) -> str:
		"""Get contract ABI"""
		return self._abi

	@abi.setter
	def abi(self, abi: str = None) -> None:
		"""Set contract ABI"""
		with self.lock:
			self._abi = abi

	@property
	def contract_address(self) -> str:
		"""Get contract address"""
		return self._contract_address

	@contract_address.setter
	def contract_address(self, address: str) -> None:
		"""Set address of Hoge contract"""
		with self.lock:
			if self.w3.isAddress(address):
				self._contract_address = self.w3.toChecksumAddress(address)

	@property
	def contract(self) -> 'web3._utils.datatypes.Contract':
		"""Return contract object"""
		return self._contract

	
	def set_contract(self) -> None:
		"""Instantiate contract object"""
		with self.lock:
			self._contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

	@property
	def w3(self) -> Web3:
		"""Return the contracts Web3 instance"""
		return self._w3

	@w3.setter
	def w3(self, w3: Web3) -> None:
		"""Set the contracts Web3 instance"""
		with self.lock:
			self._w3 = w3

	@property
	def events(self) -> 'web3.contract.ContractEvents':
		"""Return contract event object"""
		return self.contract.events



