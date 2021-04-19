from abc import ABC, abstractmethod

class Provider(ABC):

	def __init__(self, url: str, name: str, api_key: str = '', port: int = 8545):
		self.set_url(url)
		self.set_name(name)
		self.set_api_key(api_key)
		self.set_port(port)

	def set_url(self, url: str):
		"""Set Provider URL"""
		self._url = url

	def set_api_key(self, api_key: str):
		"""Set provider API Key"""
		self._api_key = api_key

	def set_name(self, name: str):
		"""Set provider name"""
		self._name = name

	def url(self) -> str:
		"""Get provider URL"""
		return self._url

	def api_key(self) -> str:
		"""Get provider API Key"""
		return self._api_key

	def name(self) -> str:
		"""Get provider name"""
		return self._name
	
	def set_port(self, port: int = 8545):
		"""Set provider port"""
		self._port = port

	def port(self) -> int:
		"""Get provider port"""
		return self._port

	@abstractmethod
	def provider(self) -> str:
		"""Get provider address"""
		pass
