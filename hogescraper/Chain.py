from web3 import Web3

class Chain(object):

	def __init__(self, ankr_api_key: str = ''):
		self.set_w3(ankr_api_key)

	def set_w3(self, ankr_api_key: str):
		"""Instantiate w3 object with ankr API key"""
		self._w3 = Web3(Web3.HTTPProvider('https://apis.ankr.com/%s' % ankr_api_key))

	def get_w3(self) -> object:
		"""Get w3 Object"""
		return self._w3

	def is_address(self, address: str) -> bool:
		"""Check if a string is a valid address"""
		return self.get_w3().isAddress(address)

	def to_checksum_address(self, address: str) -> str:
		"""Convert an address to checksum format"""
		if self.is_address(address):
			return self.get_w3().toChecksumAddress(address)

	def is_connected(self) -> bool:
		"""Check if self._w3 is connected to the blockchain"""
		return self.get_w3().isConnected()

	def from_wei(self, val: int, decimals: str = 'nano') -> float:
		"""Convert a value from wei to another format"""
		return float(self.get_w3().fromWei(val, decimals))

	def to_wei(self, val: int, decimals: str = 'nano') -> float:
		"""Convert a value to wei from another format"""
		return float(self.get_w3().toWei(val, decimals))