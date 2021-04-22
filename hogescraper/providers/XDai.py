from .Provider import Provider

class XDai(Provider):
	def __init__(self, url: str ='https://rpc.xdaichain.com/') -> None:
		"""Initiate chain to the xDai network"""
		super().__init__(url=url, name='xdai')

	def provider(self) -> str:
		"""Get provider address"""
		return self.url

