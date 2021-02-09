"""
Victor Marin Felip
vicmf88@gmail.com
"""

from datetime import datetime
from fee_models import *
from errors import FeeModelNotFound


class PriceUpdate(object):
	
	def __init__(self, update: dict):
		self._ex = None
		self._coin = None
		self._quote = None
		self._best_rate = None
		self._extime = None
		self._systime = None
		self._orderbook = None
		
		# TODO Placeholder expected keys!
		self.expected_keys = ["coin", "quote", "exchange", "rate", "datetime"]
		self._parse_update(update)
		
	def _parse_update(self, update: dict):
		# TODO Placeholder code here!
		if not all([x in update.keys() for x in self.expected_keys]):
			raise KeyError("Missing keys in update dictionary!")
		
		self._ex = update["exchange"]
		self._coin = update["coin"]
		self._quote = update["quote"]
		self._best_rate = update["rate"]
		self._systime = update["datetime"]
		
	@property
	def ex(self) -> str:
		return self._ex
	
	@property
	def coin(self) -> str:
		return self._coin
	
	@property
	def quote(self) -> str:
		return self._quote
	
	@property
	def id(self) -> tuple:
		return self.ex, self.coin, self.quote
	
	@property
	def best_rate(self) -> float:
		return self._best_rate
	
	@property
	def extime(self) -> datetime:
		return self._extime
	
	@property
	def systime(self) -> datetime:
		return self._systime
	
	@property
	def orderbook(self) -> dict:
		return self._orderbook


class AssetUpdate(object):
	
	def __init__(self, update: dict):
		"""
		The base class for a holdings update from an exchange
		
		:param update: The exchange holdings update
		"""
		
		self._ex = None
		self._datetime = None
		self._assetlist = []
		self._holdinglist = []
		self.expected_keys = ["exchange", "assets", "datetime"]
		self._parse_update(update)
		
	def _parse_update(self, update: dict):
		# TODO Placeholder code here!
		if not all([x in update.keys() for x in self.expected_keys]):
			raise KeyError("Missing keys in update dictionary!")
		
		self._ex = update["exchange"]
		self._datetime = update["datetime"]
		for asset, holding in update["assets"]:
			self._assetlist.append(asset)
			self._holdinglist.append(float(holding))
		
	@property
	def ex(self) -> str:
		return self._ex
	
	@property
	def assetlist(self) -> list:
		return self._assetlist
	
	@property
	def holdinglist(self) -> list:
		return self._holdinglist
	
	@property
	def systime(self) -> datetime:
		return self._datetime
	
		
class Asset(object):
	
	def __init__(self, _id: str):
		self._id = _id
		self._hold = 0.
		
	@property
	def id(self) -> str:
		return self._id
	
	@property
	def am(self) -> float:
		return self._hold
	
	@am.setter
	def am(self, value):
		self._hold = value

	def __str__(self):
		return self._id
	
	
class Exchange(object):
	
	def __init__(self, _id: str):
		self._id = _id
		self.model = FeesEmpty()
		self._get_fee_model()
		
	# TODO code tests for fees
	def _get_fee_model(self):
		if self.id == "KRAKEN":
			self.model = FeesKraken()
		elif self.id == "COINBASE":
			self.model = FeesCoinbase()
		elif self.id == "BINANCE":
			self.model = FeesBinance()
		elif self.id == "BITMEX":
			self.model = FeesBitmex()
		elif self.id == "BITTREX":
			self.model = FeesBittrex()
		elif self.id == "OANDA":
			self.model = FeesOanda()
		elif self.id == "GEMINI":
			self.model = FeesGemini()
		elif self.id == "BITSTAMP":
			self.model = FeesBitstamp()
		elif self.id == "BITFINEX":
			self.model = FeesBitfinex()
		elif self.id == "POLONIEX":
			self.model = FeesPoloniex()
			
		elif self.id == "EMPTY":
			self.model = FeesEmpty()
		elif self.id == "TEST":
			self.model = FeesTest()
		else:
			raise FeeModelNotFound(self.id)
		
	@property
	def id(self) -> id:
		return self._id
	
	@property
	def fee_rate(self) -> float:
		return self.model.rate
	
	@property
	def fee_model_name(self) -> str:
		return type(self.model).__name__
	
	def __str__(self):
		return self._id
