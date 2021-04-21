from .ERC20 import ERC20

class SafeMoon(ERC20):

	def _liquidity_fee(self) -> int:
		"""Check if address is in redistribution exclusion list"""
		self.contract().functions._liquidityFee().call()
		
	def _max_tx_amount(self): -> float:
		return float(self.w3().fromWei(
				self.contract().functions._maxTxAmount().call(), 'nano'
			))

	def _tax_fee(self): -> int:
		return self.contract().functions._taxFee().call()

	def get_unlock_time(self): -> int:
		return self.contract().functions.getUnlockTime().call()

	def is_excluded_from_fee(self, address: str) -> bool:
		return self.contract().functions.isExcludedFromFee(address).call()

	def is_excluded_from_reward(self, address: str) -> bool:
		return self.contract().functions.isExcludedFromReward(address).call()

	def reflection_from_token(self, t_amount: int, deduct_transfer_fee: bool) -> 

	def owner(self) -> str:
		"""Return the owner of the contract"""
		return self.contract().functions.owner().call()

	def reflection_from_token(self, t_amount: int, deduct_transfer_fee: bool) -> float:
		"""Calculate reflection from tokens"""
		return float(self.w3().fromWei(
				self.contract().functions.reflectionFromToken(t_amount, deduct_transfer_fee).call(), 'nano'
			))

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

	def swapAndLiquifiyEnabled(self) -> bool:
		return self.contract().functions.swapAndLiquifyEnabled().call()

	def uniswap_v2_pair(self) -> str:
		return self.contract().functions.uniswapV2Pair().call()

	def uniswap_v2_router(self) -> str:
		return self.contract().functions.uniswapV2Router().call()

	def total_fees(self) -> int:
		"""Return total fees"""
		return float(self.w3().fromWei(
				self.contract().functions.totalFees().call(), 'nano'
			))