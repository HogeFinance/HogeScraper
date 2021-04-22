from web3 import Web3
import requests

from .ERC20 import ERC20

class HOGE(ERC20):
	
	def __init__(self, w3: Web3, network: str = 'eth') -> None:
		"""Initiate HOGE contract, on specified network with its abi"""
		abi: str = requests.get('https://raw.githubusercontent.com/HogeFinance/token/main/Contract%20ABI').text
		addresses: dict = { 
			'eth': '0xfad45e47083e4607302aa43c65fb3106f1cd7607',
			'xdai': '0xDfF7fcF6a86F7Dc86E7facECA502851f82a349A6'
		}
		address: str = addresses[network] if network in addresses.keys() else addresses['eth']
		super().__init__(abi=abi, address=address, w3=w3)

	def is_excluded(self, address: str) -> bool:
		"""Check if address is in redistribution exclusion list"""
		if self.w3.isAddress(address):
			return self.contract.functions.isExcluded(self.w3.toChecksumAddress(address)).call()
		return False

	@property
	def owner(self) -> str:
		"""Return the owner of the contract"""
		return self.contract.functions.owner().call()

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
	def total_fees(self) -> int:
		"""Return total fees"""
		return float(self.w3.fromWei(
				self.contract.functions.totalFees().call(), 'nano'
			))