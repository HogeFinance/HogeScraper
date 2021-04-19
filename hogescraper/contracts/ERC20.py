from .Contract import Contract

class ERC20(Contract):

	def balance_of(self, address) -> float:
		"""Return balance of `address`"""
		if self.w3().isAddress(address):
			address = self.w3().toChecksumAddress(address)
			return float(self.w3().fromWei(
				self.contract().functions.balanceOf(address).call(), 'nano'
			))

	def symbol(self) -> str:
		"""Return token symbol"""
		return self.contract().functions.symbol().call()

	def decimals(self) -> int:
		"""Return decimal points in token"""
		return int(self.contract().functions.decimals().call())

	def total_supply(self) -> float:
		"""Return token total supply"""
		return float(self.w3().fromWei(self.contract().functions.totalSupply().call(), "nano"))

	def name(self) -> str:
		"""Return token name"""
		return self.contract().functions.name().call()

	def allowance(self, owner, spender) -> float:
		"""Return allocated allowance from owner to spender"""
		if self.w3().isAddress(owner) and self.w3().isAddress(spender):
			owner = self.w3().toChecksumAddress(owner)
			spender = self.w3().toChecksumAddress(spender)
			return float(self.w3().fromWei(
				self.contract().functions.allowance(owner, spender).call(), 'nano'
			))
