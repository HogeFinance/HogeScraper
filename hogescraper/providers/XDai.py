from .Provider import Provider

class XDai(Provider):
	def __init__(self, url='https://rpc.xdaichain.com/'):
		super().__init__(url=url, name='xdai')

	def provider(self) -> str:
		"""Get provider address"""
		return self.url()

