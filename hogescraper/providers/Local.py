from .Provider import Provider

class Local(Provider):
	def __init__(self, url: str = 'http://localhost', port: int = 8545):
		super().__init__(url=url, name='local', port=port)

	def provider(self) -> str:
		"""Get provider address"""
		return "%s:%d" % (self.url(), self.port())