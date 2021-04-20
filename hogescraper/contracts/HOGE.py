from .ERC20 import ERC20

class HOGE(ERC20):

	def is_excluded(self, address: str) -> bool:
		"""Check if address is in redistribution exclusion list"""
		if self.w3().isAddress(address):
			return self.contract().functions.isExcluded(self.w3().toChecksumAddress(address)).call()
		return False

	def owner(self) -> str:
		"""Return the owner of the contract"""
		return self.contract().functions.owner().call()

	def reflection_from_token(self, t_amount: int, deduct_transfer_fee: bool) -> float:
		"""Calculate reflection from tokens"""
			return float(self.w3().fromWei(
				self.contract().functions.reflectionFromToken(t_amount, deduct_transfer_fee).call(), 'nano'
			))

	def token_from_reflection(self, r_amount: int) -> float:
		"""Calculate tokens from reflection"""
		return float(self.w3().fromWei(
				self.contract().functions.tokenFromReflection(r_amount).call(), 'nano'
			))

	def total_fees(self) -> int:
		"""Return total fees"""
		return float(self.w3().fromWei(
				self.contract().functions.totalFees().call(), 'nano'
			))