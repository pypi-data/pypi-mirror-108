from typing import List


class ExtensionAttributes:
	pass

	def __init__(self, ) -> None:
		pass


class Price:
	price: int
	store_id: int
	sku: str
	extension_attributes: ExtensionAttributes

	def __init__(self, price: int, store_id: int, sku: str, extension_attributes: ExtensionAttributes = None) -> None:
		self.price = price
		self.store_id = store_id
		self.sku = sku
		if extension_attributes:
			self.extension_attributes = extension_attributes


class ItauPowerPrice:
	prices: List[Price]

	def __init__(self, prices: List[Price]) -> None:
		self.prices = prices
