from abc import ABC, abstractmethod

class Provider(ABC):

	def __init__(self, url: str, name: str, api_key: str = '', port: int = 8545) -> None:
		"""Initiate chain to the network specified by url and port"""
		self._name: str = name
		self._url: str = url
		self._api_key: str = api_key
		self._port: str = port

	@property
	def url(self) -> str:
		"""Get provider URL"""
		return self._url

	@url.setter
	def url(self, url: str):
		"""Set Provider URL"""
		self._url = url

	@property
	def api_key(self) -> str:
		"""Get provider API Key"""
		return self._api_key

	@api_key.setter
	def api_key(self, api_key: str):
		"""Set provider API Key"""
		self._api_key = api_key

	@property
	def name(self) -> str:
		"""Get provider name"""
		return self._name

	@name.setter
	def name(self, name: str):
		"""Set provider name"""
		self._name = name
	
	@property
	def port(self) -> int:
			"""Get provider port"""
			return self._port

	@port.setter
	def port(self, port: int = 8545):
		"""Set provider port"""
		if 0 <= port <= 65534:
			self._port = port

	@abstractmethod
	def provider(self) -> str:
		"""Get provider address"""
		pass
