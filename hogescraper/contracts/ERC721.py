from .Contract import Contract

class ERC721(Contract):
	
	def balance_of(self, address: str) -> int:
		"""Count all NFTs assigned to an owner"""
		if self.w3().isAddress(address):
			address = self.w3().toChecksumAddress(address)
			return self.contract().functions.balanceOf(address).call()

	def owner_of(self, token_id: int) -> str:
		"""Find the owner of an NFT"""
		return self.contract().functions.ownerOf(token_id).call()

	def get_approved(self, token_id: int) -> str:
		"""Get approved address for a single NFT"""
		return self.contract().functions.getApproved(token_id).call()

	def is_approved_for_all(self, owner_addr: str, operator_addr: str) -> bool:
		"""Query if an address is an authorized operator for another address"""
		return self.contract().functions.isApprovedForAll(owner_addr, operator_addr).call()

	def name(self) -> str:
		"""A descriptive name for a collection of NFTs in this contract"""
		return self.contract().functions.name().call()

	def symbol(self) -> str:
		"""An abbreviated name for NFTs in this contract"""
		return self.contract().functions.symbol().call()

	def token_uri(self, token_id: int) -> str:
		"""A distinct Uniform Resource Identifier (URI) for a given asset."""
		return self.contract().functions.tokenURI(token_id).call()