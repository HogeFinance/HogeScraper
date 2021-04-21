from datetime import datetime
import json

import requests

from .Price import Price

class CoinGecko(Price):

	def __init__(self, coin_id: str = 'hoge-finance'):
		super().__init__(coin_id)
		self._base_url = 'https://api.coingecko.com/api/v3/coins'

	def price(self):
		"""Return the current price for self._coin_id"""
		today = datetime.now().strftime("%d-%m-%Y")
		return self.historical_price(today)

	def historical_price(self, date: str):
		"""Return historical price for self._coin_id"""
		endpoint = 'history'
		url = "%s/%s/%s?date=%s&localization=false" % (self.base_url(), self.coin(), endpoint, date)
		data = json.loads(requests.get(url).text)['market_data']['current_price']
		return data

	def currencies(self):
		"""Return a list of currencies self._coin_id has prices listed in"""
		return self.price().keys()