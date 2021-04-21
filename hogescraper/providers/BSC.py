from .Provider import Provider

class BSC(Provider):
	def __init__(self, port: int = 443):
		super().__init__(url='https://bsc-dataseed1.binance.org', name='binance', port=port)

	def provider(self) -> str:
		"""Get provider address"""
		return "%s:%d" % (self.url(), self.port())
