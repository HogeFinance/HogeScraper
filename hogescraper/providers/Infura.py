from .Provider import Provider

class Infura(Provider):
	def __init__(self, api_key: str, url: str = 'https://mainnet.infura.io/v3'):
		super().__init__(url=url, name='eth', api_key=api_key)

	def provider(self) -> str:
		"""Get provider address"""
		return "%s/%s" % (self.url(), self.api_key())
