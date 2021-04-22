from abc import ABC, abstractmethod

class Price(ABC):

	def __init__(self, coin_id: str = 'hoge-finance') -> None:
		"""Initialize coin_id and base_url variables"""
		self.coin_id: str = coin_id
		self.base_url: str = ''

	@property
	def coin_id(self) -> str:
		"""Return current coin the price provider is tracking"""
		return self._coin_id

	@coin_id.setter
	def coin_id(self, coin_id: str) -> None:
		"""Set coin for price provider to track"""
		self._coin_id: str = coin_id

	@property
	def base_url(self) -> str:
		"""Return current base_url for Price Provider"""
		return self._base_url

	@base_url.setter
	def base_url(self, url: str) -> None:
		"""Set base_url for Price Provider"""
		self._base_url: str = url

	@abstractmethod
	def price(self) -> list:
		"""Return a list of prices indexed by currency"""
		pass

	@abstractmethod
	def historical_price(self, date: str) -> list:
		"""Return a list of historical prices from `date` indexed by currency"""
		pass

	@abstractmethod
	def currencies(self) -> list:
		"""Return the list of currencies this provider can convert to"""
		pass