from abc import ABC, abstractmethod

class Price(ABC):

	def __init__(self, coin_id: str = 'hoge-finance'):
		self._coin_id = coin_id

	def coin(self):
		return self._coin_id

	def base_url(self):
		return self._base_url

	@abstractmethod
	def price(self):
		pass

	@abstractmethod
	def historical_price(self, date: str):
		pass
