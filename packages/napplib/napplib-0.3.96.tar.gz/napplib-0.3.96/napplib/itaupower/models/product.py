from typing import List


class CustomAttribute:
	attribute_code: str
	value: str

	def __init__(self, attribute_code: str, value: str) -> None:
		self.attribute_code = attribute_code
		self.value = value


class BundleProductOptionExtensionAttributes:
	pass

	def __init__(self, ) -> None:
		pass


class BundleProductOptionProductLink:
	id: str
	sku: str
	option_id: int
	qty: int
	position: int
	is_default: bool
	price: int
	price_type: int
	can_change_quantity: int
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, id: str, sku: str, option_id: int, qty: int, position: int, is_default: bool, price: int, price_type: int, can_change_quantity: int, extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.id = id
		self.sku = sku
		self.option_id = option_id
		self.qty = qty
		self.position = position
		self.is_default = is_default
		self.price = price
		self.price_type = price_type
		self.can_change_quantity = can_change_quantity
		self.extension_attributes = extension_attributes


class BundleProductOption:
	option_id: int
	title: str
	required: bool
	type: str
	position: int
	sku: str
	product_links: List[BundleProductOptionProductLink]
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, option_id: int, title: str, required: bool, type: str, position: int, sku: str, product_links: List[BundleProductOptionProductLink], extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.option_id = option_id
		self.title = title
		self.required = required
		self.type = type
		self.position = position
		self.sku = sku
		self.product_links = product_links
		self.extension_attributes = extension_attributes


class CategoryLink:
	position: int
	category_id: str
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, position: int, category_id: str, extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.position = position
		self.category_id = category_id
		self.extension_attributes = extension_attributes


class ConfigurableProductOptionValue:
	value_index: int
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, value_index: int, extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.value_index = value_index
		self.extension_attributes = extension_attributes


class ConfigurableProductOption:
	id: int
	attribute_id: str
	label: str
	position: int
	is_use_default: bool
	values: List[ConfigurableProductOptionValue]
	extension_attributes: BundleProductOptionExtensionAttributes
	product_id: int

	def __init__(self, id: int, attribute_id: str, label: str, position: int, is_use_default: bool, values: List[ConfigurableProductOptionValue], extension_attributes: BundleProductOptionExtensionAttributes, product_id: int) -> None:
		self.id = id
		self.attribute_id = attribute_id
		self.label = label
		self.position = position
		self.is_use_default = is_use_default
		self.values = values
		self.extension_attributes = extension_attributes
		self.product_id = product_id


class FileContent:
	file_data: str
	name: str
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, file_data: str, name: str, extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.file_data = file_data
		self.name = name
		self.extension_attributes = extension_attributes


class DownloadableProductLink:
	id: int
	title: str
	sort_order: int
	is_shareable: int
	price: int
	number_of_downloads: int
	link_type: str
	link_file: str
	link_file_content: FileContent
	link_url: str
	sample_type: str
	sample_file: str
	sample_file_content: FileContent
	sample_url: str
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, id: int, title: str, sort_order: int, is_shareable: int, price: int, number_of_downloads: int, link_type: str, link_file: str, link_file_content: FileContent, link_url: str, sample_type: str, sample_file: str, sample_file_content: FileContent, sample_url: str, extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.id = id
		self.title = title
		self.sort_order = sort_order
		self.is_shareable = is_shareable
		self.price = price
		self.number_of_downloads = number_of_downloads
		self.link_type = link_type
		self.link_file = link_file
		self.link_file_content = link_file_content
		self.link_url = link_url
		self.sample_type = sample_type
		self.sample_file = sample_file
		self.sample_file_content = sample_file_content
		self.sample_url = sample_url
		self.extension_attributes = extension_attributes


class DownloadableProductSample:
	id: int
	title: str
	sort_order: int
	sample_type: str
	sample_file: str
	sample_file_content: FileContent
	sample_url: str
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, id: int, title: str, sort_order: int, sample_type: str, sample_file: str, sample_file_content: FileContent, sample_url: str, extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.id = id
		self.title = title
		self.sort_order = sort_order
		self.sample_type = sample_type
		self.sample_file = sample_file
		self.sample_file_content = sample_file_content
		self.sample_url = sample_url
		self.extension_attributes = extension_attributes


class GiftcardAmount:
	attribute_id: int
	website_id: int
	value: int
	website_value: int
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, attribute_id: int, website_id: int, value: int, website_value: int, extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.attribute_id = attribute_id
		self.website_id = website_id
		self.value = value
		self.website_value = website_value
		self.extension_attributes = extension_attributes


class StockItem:
	item_id: int
	product_id: int
	stock_id: int
	qty: int
	is_in_stock: bool
	is_qty_decimal: bool
	show_default_notification_message: bool
	use_config_min_qty: bool
	min_qty: int
	use_config_min_sale_qty: int
	min_sale_qty: int
	use_config_max_sale_qty: bool
	max_sale_qty: int
	use_config_backorders: bool
	backorders: int
	use_config_notify_stock_qty: bool
	notify_stock_qty: int
	use_config_qty_increments: bool
	qty_increments: int
	use_config_enable_qty_inc: bool
	enable_qty_increments: bool
	use_config_manage_stock: bool
	manage_stock: bool
	low_stock_date: str
	is_decimal_divided: bool
	stock_status_changed_auto: int
	extension_attributes: BundleProductOptionExtensionAttributes

	def __init__(self, item_id: int, product_id: int, stock_id: int, qty: int, is_in_stock: bool, is_qty_decimal: bool, show_default_notification_message: bool, use_config_min_qty: bool, min_qty: int, use_config_min_sale_qty: int, min_sale_qty: int, use_config_max_sale_qty: bool, max_sale_qty: int, use_config_backorders: bool, backorders: int, use_config_notify_stock_qty: bool, notify_stock_qty: int, use_config_qty_increments: bool, qty_increments: int, use_config_enable_qty_inc: bool, enable_qty_increments: bool, use_config_manage_stock: bool, manage_stock: bool, low_stock_date: str, is_decimal_divided: bool, stock_status_changed_auto: int, extension_attributes: BundleProductOptionExtensionAttributes) -> None:
		self.item_id = item_id
		self.product_id = product_id
		self.stock_id = stock_id
		self.qty = qty
		self.is_in_stock = is_in_stock
		self.is_qty_decimal = is_qty_decimal
		self.show_default_notification_message = show_default_notification_message
		self.use_config_min_qty = use_config_min_qty
		self.min_qty = min_qty
		self.use_config_min_sale_qty = use_config_min_sale_qty
		self.min_sale_qty = min_sale_qty
		self.use_config_max_sale_qty = use_config_max_sale_qty
		self.max_sale_qty = max_sale_qty
		self.use_config_backorders = use_config_backorders
		self.backorders = backorders
		self.use_config_notify_stock_qty = use_config_notify_stock_qty
		self.notify_stock_qty = notify_stock_qty
		self.use_config_qty_increments = use_config_qty_increments
		self.qty_increments = qty_increments
		self.use_config_enable_qty_inc = use_config_enable_qty_inc
		self.enable_qty_increments = enable_qty_increments
		self.use_config_manage_stock = use_config_manage_stock
		self.manage_stock = manage_stock
		self.low_stock_date = low_stock_date
		self.is_decimal_divided = is_decimal_divided
		self.stock_status_changed_auto = stock_status_changed_auto
		self.extension_attributes = extension_attributes


class VertexCommodityCode:
	code: str
	type: str

	def __init__(self, code: str, type: str) -> None:
		self.code = code
		self.type = type


class ProductExtensionAttributes:
	website_ids: List[int]
	category_links: List[CategoryLink]
	bundle_product_options: List[BundleProductOption]
	stock_item: StockItem
	downloadable_product_links: List[DownloadableProductLink]
	downloadable_product_samples: List[DownloadableProductSample]
	giftcard_amounts: List[GiftcardAmount]
	configurable_product_options: List[ConfigurableProductOption]
	configurable_product_links: List[int]
	vertex_commodity_code: VertexCommodityCode

	def __init__(self, website_ids: List[int] = None,
						category_links: List[CategoryLink] = None,
						bundle_product_options: List[BundleProductOption] = None,
						stock_item: StockItem = None,
						downloadable_product_links: List[DownloadableProductLink] = None,
						downloadable_product_samples: List[DownloadableProductSample] = None,
						giftcard_amounts: List[GiftcardAmount] = None,
						configurable_product_options: List[ConfigurableProductOption] = None,
						configurable_product_links: List[int] = None,
						vertex_commodity_code: VertexCommodityCode = None) -> None:
		if website_ids:
			self.website_ids = website_ids
		if category_links:
			self.category_links = category_links
		if bundle_product_options:
			self.bundle_product_options = bundle_product_options
		if stock_item:
			self.stock_item = stock_item
		if downloadable_product_links:
			self.downloadable_product_links = downloadable_product_links
		if downloadable_product_samples:
			self.downloadable_product_samples = downloadable_product_samples
		if giftcard_amounts:
			self.giftcard_amounts = giftcard_amounts
		if configurable_product_options:
			self.configurable_product_options = configurable_product_options
		if configurable_product_links:
			self.configurable_product_links = configurable_product_links
		if vertex_commodity_code:
			self.vertex_commodity_code = vertex_commodity_code


class Content:
	base64_encoded_data: str
	type: str
	name: str

	def __init__(self, base64_encoded_data: str, type: str, name: str) -> None:
		self.base64_encoded_data = base64_encoded_data
		self.type = type
		self.name = name


class VideoContent:
	media_type: str
	video_provider: str
	video_url: str
	video_title: str
	video_description: str
	video_metadata: str

	def __init__(self, media_type: str, video_provider: str, video_url: str, video_title: str, video_description: str, video_metadata: str) -> None:
		self.media_type = media_type
		self.video_provider = video_provider
		self.video_url = video_url
		self.video_title = video_title
		self.video_description = video_description
		self.video_metadata = video_metadata


class MediaGalleryEntryExtensionAttributes:
	video_content: VideoContent

	def __init__(self, video_content: VideoContent) -> None:
		self.video_content = video_content


class MediaGalleryEntry:
	id: int
	media_type: str
	label: str
	position: int
	disabled: bool
	types: List[str]
	file: str
	content: Content
	extension_attributes: MediaGalleryEntryExtensionAttributes

	def __init__(self, id: int, media_type: str, label: str, position: int, disabled: bool, types: List[str], file: str, content: Content, extension_attributes: MediaGalleryEntryExtensionAttributes) -> None:
		self.id = id
		self.media_type = media_type
		self.label = label
		self.position = position
		self.disabled = disabled
		self.types = types
		self.file = file
		self.content = content
		self.extension_attributes = extension_attributes


class OptionExtensionAttributes:
	vertex_flex_field: str

	def __init__(self, vertex_flex_field: str) -> None:
		self.vertex_flex_field = vertex_flex_field


class OptionValue:
	title: str
	sort_order: int
	price: int
	price_type: str
	sku: str
	option_type_id: int

	def __init__(self, title: str, sort_order: int, price: int, price_type: str, sku: str, option_type_id: int) -> None:
		self.title = title
		self.sort_order = sort_order
		self.price = price
		self.price_type = price_type
		self.sku = sku
		self.option_type_id = option_type_id


class Option:
	product_sku: str
	option_id: int
	title: str
	type: str
	sort_order: int
	is_require: bool
	price: int
	price_type: str
	sku: str
	file_extension: str
	max_characters: int
	image_size_x: int
	image_size_y: int
	values: List[OptionValue]
	extension_attributes: OptionExtensionAttributes

	def __init__(self, product_sku: str,
						option_id: int,
						title: str,
						type: str,
						sort_order: int,
						is_require: bool,
						price: int,
						price_type: str,
						sku: str,
						file_extension: str,
						max_characters: int,
						image_size_x: int,
						image_size_y: int,
						values: List[OptionValue],
						extension_attributes: OptionExtensionAttributes) -> None:
		self.product_sku = product_sku
		self.option_id = option_id
		self.title = title
		self.type = type
		self.sort_order = sort_order
		self.is_require = is_require
		self.price = price
		self.price_type = price_type
		self.sku = sku
		self.file_extension = file_extension
		self.max_characters = max_characters
		self.image_size_x = image_size_x
		self.image_size_y = image_size_y
		self.values = values
		self.extension_attributes = extension_attributes


class PurpleExtensionAttributes:
	qty: int

	def __init__(self, qty: int) -> None:
		self.qty = qty


class ProductProductLink:
	sku: str
	link_type: str
	linked_product_sku: str
	linked_product_type: str
	position: int
	extension_attributes: PurpleExtensionAttributes

	def __init__(self, sku: str,
						link_type: str,
						linked_product_sku: str,
						linked_product_type: str,
						position: int,
						extension_attributes: PurpleExtensionAttributes) -> None:
		self.sku = sku
		self.link_type = link_type
		self.linked_product_sku = linked_product_sku
		self.linked_product_type = linked_product_type
		self.position = position
		self.extension_attributes = extension_attributes


class TierPriceExtensionAttributes:
	percentage_value: int
	website_id: int

	def __init__(self, percentage_value: int, website_id: int) -> None:
		self.percentage_value = percentage_value
		self.website_id = website_id


class TierPrice:
	customer_group_id: int
	qty: int
	value: int
	extension_attributes: TierPriceExtensionAttributes

	def __init__(self, customer_group_id: int, qty: int, value: int, extension_attributes: TierPriceExtensionAttributes) -> None:
		self.customer_group_id = customer_group_id
		self.qty = qty
		self.value = value
		self.extension_attributes = extension_attributes


class Product:
	id: int
	sku: str
	name: str
	attribute_set_id: int
	price: int
	status: int
	visibility: int
	type_id: str
	created_at: str
	updated_at: str
	weight: int
	extension_attributes: ProductExtensionAttributes
	product_links: List[ProductProductLink]
	options: List[Option]
	media_gallery_entries: List[MediaGalleryEntry]
	tier_prices: List[TierPrice]
	custom_attributes: List[CustomAttribute]

	def __init__(self, sku: str,
						id: int = None,
						name: str = None,
						attribute_set_id: int = None,
						price: int = None,
						status: int = None,
						visibility: int = None,
						type_id: str = None,
						created_at: str = None,
						updated_at: str = None,
						weight: int = None,
						extension_attributes: ProductExtensionAttributes = None,
						product_links: List[ProductProductLink] = None,
						options: List[Option] = None,
						media_gallery_entries: List[MediaGalleryEntry] = None,
						tier_prices: List[TierPrice] = None,
						custom_attributes: List[CustomAttribute] = None) -> None:
		self.sku = sku
		if id:
			self.id = id
		if name:
			self.name = name
		if attribute_set_id:
			self.attribute_set_id = attribute_set_id
		if price:
			self.price = price
		if status:
			self.status = status
		if visibility:
			self.visibility = visibility
		if type_id:
			self.type_id = type_id
		if created_at:
			self.created_at = created_at
		if updated_at:
			self.updated_at = updated_at
		if weight:
			self.weight = weight
		if extension_attributes:
			self.extension_attributes = extension_attributes
		if product_links:
			self.product_links = product_links
		if options:
			self.options = options
		if media_gallery_entries:
			self.media_gallery_entries = media_gallery_entries
		if tier_prices:
			self.tier_prices = tier_prices
		if custom_attributes:
			self.custom_attributes = custom_attributes


class ItauPowerProduct:
	product: Product
	save_options: bool

	def __init__(self, product: Product, save_options: bool = None) -> None:
		self.product = product
		if save_options:
			self.save_options = save_options
