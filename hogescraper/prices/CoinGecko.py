from datetime import datetime
import json

import requests

from .Price import Price

class CoinGecko(Price):

	def __init__(self, coin_id: str = 'hoge-finance') -> None:
		"""Initialize coingeckos base URL"""
		super().__init__(coin_id)
		self._base_url: str = 'https://api.coingecko.com/api/v3/coins'

	def price(self) -> list:
		"""Return the current price for self._coin_id"""
		today: str = datetime.now().strftime("%d-%m-%Y")
		return self.historical_price(today)

	def historical_price(self, date: str) -> list:
		"""Return historical price for self._coin_id"""
		endpoint: str = 'history'
		url: str = "%s/%s/%s?date=%s&localization=false" % (self.base_url, self.coin_id, endpoint, date)
		return json.loads(requests.get(url).text)['market_data']['current_price']

	def currencies(self) -> list:
		"""Return a list of currencies self._coin_id has prices listed in"""
		return self.price().keys()