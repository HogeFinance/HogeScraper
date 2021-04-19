from .Provider import Provider

class Local(Provider):

	def provider(self) -> str:
		"""Get provider address"""
		return "%s:%d" % (self.url(), self.port())