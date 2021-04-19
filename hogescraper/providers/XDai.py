from .Provider import Provider

class XDai(Provider):

	def provider(self) -> str:
		"""Get provider address"""
		return self.url()