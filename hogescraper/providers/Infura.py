from .Provider import Provider

class Infura(Provider):

	def provider(self) -> str:
		"""Get provider address"""
		return "%s/%s" % (self.url(), self.api_key())
