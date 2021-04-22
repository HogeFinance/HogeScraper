from web3 import Web3
import requests

from .ERC20 import ERC20

class SafeMoon(ERC20):

	def __init__(self, w3: Web3) -> None:
		"""Initiate SafeMoon instance with abi and contract address"""
		abi: str = requests.get('http://api.bscscan.com/api?module=contract&action=getabi&address=0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3&format=raw').text
		address: str = '0x8076C74C5e3F5852037F31Ff0093Eeb8c8ADd8D3'
		super().__init__(abi=abi, address=address, w3=w3)

	@property
	def _liquidity_fee(self) -> int:
		"""Check if address is in redistribution exclusion list"""
		self.contract.functions._liquidityFee().call()

	@property		
	def _max_tx_amount(self) -> float:
		return float(self.w3.fromWei(
				self.contract.functions._maxTxAmount().call(), 'nano'
			))

	@property
	def _tax_fee(self) -> int:
		return self.contract.functions._taxFee().call()

	@property
	def get_unlock_time(self) -> int:
		return self.contract.functions.getUnlockTime().call()

	def is_excluded_from_fee(self, address: str) -> bool:
		return self.contract.functions.isExcludedFromFee(address).call()

	def is_excluded_from_reward(self, address: str) -> bool:
		return self.contract.functions.isExcludedFromReward(address).call()

	@property
	def owner(self) -> str:
		"""Return the owner of the contract"""
		return self.contract.functions.owner().call()

	def reflection_from_token(self, t_amount: int, deduct_transfer_fee: bool) -> float:
		"""Calculate reflection from tokens"""
		return float(self.w3.fromWei(
				self.contract.functions.reflectionFromToken(t_amount, deduct_transfer_fee).call(), 'nano'
			))

	def reflection_from_token(self, t_amount: int, deduct_transfer_fee: bool) -> float:
		"""Calculate reflection from tokens"""
		return float(self.w3.fromWei(
				self.contract.functions.reflectionFromToken(t_amount, deduct_transfer_fee).call(), 'nano'
			))

	def token_from_reflection(self, r_amount: int) -> float:
		"""Calculate tokens from reflection"""
		return float(self.w3.fromWei(
				self.contract.functions.tokenFromReflection(r_amount).call(), 'nano'
			))

	@property
	def swapAndLiquifiyEnabled(self) -> bool:
		return self.contract.functions.swapAndLiquifyEnabled().call()

	@property
	def uniswap_v2_pair(self) -> str:
		return self.contract.functions.uniswapV2Pair().call()

	@property
	def uniswap_v2_router(self) -> str:
		return self.contract.functions.uniswapV2Router().call()

	@property
	def total_fees(self) -> int:
		"""Return total fees"""
		return float(self.w3.fromWei(
				self.contract.functions.totalFees().call(), 'nano'
			))