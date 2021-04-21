from threading import Lock

from web3 import Web3

class Contract(object):

	def __init__(
		self,
		w3: Web3,
		address: str,
		abi: str = ''
	):
		self._lock = Lock()
		self.set_w3(w3)
		self.set_abi(abi)
		self.set_contract_address(address)
		self.set_contract()

	def set_abi(self, abi: str = None):
		"""Set contract ABI"""
		with self._lock:
			self._abi = abi

	def set_contract_address(self, address: str):
		"""Set address of Hoge contract"""
		with self._lock:
			if self.w3().isAddress(address):
				self._contract_address = self.w3().toChecksumAddress(address)

	def set_contract(self):
		"""Instantiate contract object"""
		with self._lock:
			self._contract = self.w3().eth.contract(address=self.contract_address(), abi=self.abi())

	def set_w3(self, w3):
		"""Set the contracts Web3 instance"""
		with self._lock:
			self._w3 = w3

	def w3(self) -> Web3:
		"""Return the contracts Web3 instance"""
		return self._w3

	def abi(self) -> str:
		"""Get contract ABI"""
		return self._abi

	def contract_address(self) -> str:
		"""Get contract address"""
		return self._contract_address

	def contract(self) -> object:
		"""Return contract object"""
		return self._contract

	def events(self) -> object:
		"""Return contract event object"""
		return self.contract().events



