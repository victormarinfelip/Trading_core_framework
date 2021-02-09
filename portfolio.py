"""
Victor Marin Felip
vicmf88@gmail.com
"""

from base import *
from collections import deque
from engine_errors import *
from typing import Tuple, List, Union, Optional, Dict
from datetime import datetime, timedelta
import itertools


class Pair(object):
	
	def __init__(self, exchange: Exchange, coin: Asset, quote: Asset):
		self.ex = exchange
		self.coin = coin
		self.quote = quote
		
		self.fake_mode = False
		# TODO check this doesn't interfere with things
		# This is bc binance uses USDT by default, but we can trick the engine into thinking that this pair exists
		if self.ex == "BINANCE" and "USD" in self.coin.id and "USD" in self.quote.id:
			self.fake_mode = True
		
		if coin.id == quote.id:
			raise WrongAssetError(coin, "any other one as it is repeated (coin = quote !)")
		
		self._best_rate = None
		self.updates = deque()
		
		self._last_update_time_sys = None

	@property
	def rate(self) -> Optional[float]:
		if self.fake_mode:
			return 1
		else:
			return self._best_rate
	
	@property
	def last_update_time(self) -> Optional[datetime]:
		if self.fake_mode:
			return datetime.now()
		else:
			return self._last_update_time_sys
	
	@property
	def time_since_update(self) -> Optional[timedelta]:
		if self._last_update_time_sys is not None:
			return self.time_now - self._last_update_time_sys
		else:
			# TODO RECHECK THAT THIS ACTUALLY WORKS EVERYWHERE
			return timedelta(days=9999)
	
	@property
	def time_now(self) -> datetime:
		return datetime.now()
	
	@property
	def id(self) -> str:
		return "{}_{}_{}".format(self.ex, self.coin, self.quote)

	@property
	def sliced_id(self) -> Tuple[str, str, str]:
		return (self.ex.id, self.coin.id, self.quote.id)

	def __str__(self) -> str:
		return self.id
	
	def add_update(self, update: PriceUpdate):
		"""
		Adds an update to the pair. It expects the update to be for this specific pair.
		Will throw exceptions if exchange and assets don't match
		
		:param update: The update
		"""
		if update.ex != self.ex.id:
			raise WrongExchangeError(self.ex, update.ex)
		if update.coin != self.coin.id:
			raise WrongAssetError(self.coin, update.coin)
		if update.quote != self.quote.id:
			raise WrongAssetError(self.quote, update.quote)
	
		self.updates.append(update)
		if len(self.updates) > 50:
			self.updates.popleft()
			
		self._best_rate = update.best_rate
		self._last_update_time_sys = update.systime
	
	
class Portfolio(object):
	
	def __init__(self):
		self.pairs = {}
		self.ex_asset = {}
		self._possible_loops = None
		self._updating = True
	
	def add_pair(self, pair: Union[str, Tuple[Exchange, Asset, Asset]]) -> Pair:
		"""
		Adds a pair to the portfolio.
		pairs can be a string like "KRAKEN_USD_BTC" or a list of Exchange, Asset, Asset
		
		:param pair: The pair to be added
		:return: The added pair object
		"""
		# TODO more elegant solution if we wait until checking if assets already exist before instanciating them
		if type(pair) is str:
			names = pair.split("_")
			if len(names) != 3:
				raise IndexError("A pair needs 3 items. Got: {}".format(names))
			ex = Exchange(names[0])
			coin = Asset(names[1])
			quote = Asset(names[2])
			new_pair = Pair(ex, coin, quote)
		elif type(pair) is tuple:
			if len(pair) != 3:
				raise IndexError("A symbol needs 3 items. Got: {}".format(pair))
			new_pair = Pair(*pair)
		else:
			raise UnrecognizedPairlFormat(pair)
		
		e = new_pair.ex.id
		co = new_pair.coin.id
		quo = new_pair.quote.id
		
		try:
			old_pair = self.pairs[e][co][quo]
			raise AlreadyImplementedPair(old_pair)
		except KeyError:
			pass
		if e not in self.ex_asset.keys():
			# Let's check that the assets are not already present
			ex_ass = self.get_assets()
			for ex, asslist in ex_ass.items():
				for ass in asslist.values():
					if ass == new_pair.coin:
						new_pair.coin = Asset(ass.id)
					if ass == new_pair.quote:
						new_pair.quote = Asset(ass.id)
			
			self.ex_asset[e] = {"object": new_pair.ex}
		else:
			new_pair.ex = self.ex_asset[e]["object"]
		if co not in self.ex_asset[e].keys():
			self.ex_asset[e][co] = new_pair.coin
		else:
			new_pair.coin = self.ex_asset[e][co]
		if quo not in self.ex_asset[e].keys():
			self.ex_asset[e][quo] = new_pair.quote
		else:
			new_pair.quote = self.ex_asset[e][quo]
		
		if e not in self.pairs:
			self.pairs[e] = {}
		if co not in self.pairs[e]:
			self.pairs[e][co] = {}
		if quo not in self.pairs[e][co]:
			self.pairs[e][co][quo] = new_pair

		return new_pair
	
	def get_pairs_by_exchange(self, exchange: Union[str, Exchange]) -> list:
		"""
		Returns a list of pairs instanced for an exchange
		
		:param exchange: The exchange, in string form or as an object
		:return: A list of pairs, empty if none is found
		"""
		found_pairs = []
		exchange = str(exchange)
		if exchange not in self.pairs.keys():
			return found_pairs
		
		for c, a in self.pairs[exchange].items():
			for quo, b in a.items():
				found_pairs.append(b)
				
		return found_pairs
	
	def get_pairs_by_coin(self, coin: Union[str, Asset]) -> List[Pair]:
		"""
		Returns a list of pairs instanced for a coin
		
		:param coin: The coin, in string form or as an object
		:return: A list of pairs, empty if none is found
		"""
		found_pair = []
		
		coin = str(coin)
		
		for ex in self.pairs.keys():
			if coin not in self.pairs[ex].keys():
				continue
			for quo, pair in self.pairs[ex][coin].items():
				found_pair.append(pair)

		return found_pair
	
	def get_pairs_full(self) -> dict:
		"""
		Returns a dict of dicts with pair objects per exchange. [ex][symb.id] = symb_obj
		
		:return: The dict.
		"""
		pairs_full = {}
		for ex in self.pairs.keys():
			pairs_ex = self.get_pairs_by_exchange(ex)
			pairs_full[ex] = {}
			for symb in pairs_ex:
				pairs_full[ex][symb.id] = symb
		return pairs_full
		
	def get_pairs_by_quote(self, quote: Union[str, Asset]) -> list:
		"""
		Returns a list of pairs instanced for a quote
		
		:param quote: The quote, in string form or as an object
		:return: A list of pairs, empty if none is found
		"""
		found_pairs = []
		
		quote = str(quote)
		
		for ex in self.pairs.keys():
			for co in self.pairs[ex].keys():
				if quote not in self.pairs[ex][co].keys():
					continue
				found_pairs.append(self.pairs[ex][co][quote])

		return found_pairs
	
	def get_pair_by_id(self, pair_id: Union[str, Tuple[Exchange, Asset, Asset]]) -> Optional[Pair]:
		"""
		Returns the pair object with the same pair id as specified, none if it is not found
		
		:param pair_id: The pair id in strnig format or tuple of (exchange, coin, quote) as strings
		:return:
		"""
		found_pair = None
		
		if type(pair_id) == str:
			pair_id = pair_id.split("_")
		if len(pair_id) != 3:
			raise UnrecognizedPairlFormat(pair_id)
		if self.pair_exists(pair_id):
			return self.pairs[pair_id[0]][pair_id[1]][pair_id[2]]
		
		return found_pair

	def stop_updating(self):
		self._updating = False

	def resume_updating(self):
		self._updating = True
		
	def push_update(self, update: PriceUpdate) -> Pair:
		"""
		Pushes an update to the portfolio. Automatically finds the correct pair to apply the update
		
		:param update: The update as an instance of the PriceUpdate class
		:return: The updated pair
		"""
		if not self.pair_exists(update.id):
			raise PairlNotImplemented("{}_{}_{}".format(*update.id))
		ex, co, quo = update.id
		target_pair = self.pairs[ex][co][quo]
		if self._updating:
			target_pair.add_update(update)
		return target_pair
	
	def adjust_holdings_from_assetupd(self, update: Optional[AssetUpdate]) -> Optional[dict]:
		"""
		Adjusts holdings from an AssetUpdate object. Assumes assets existign in portfolio. If None is passed, returns None.
		
		:param update: The AssetUpdate update.
		:return: A dictionary with d[exchange][asset] = Asset, as returned by get_holdings()
		"""
		
		if update is None:
			return None
		
		ex = update.ex
		asset_names = update.assetlist
		asset_holds = update.holdinglist
		
		full_assets = self.get_assets()
		
		for name, holds in zip(asset_names, asset_holds):
			try:
				full_assets[ex][name].am = holds
			except KeyError:
				pass
				# TODO handle better this circumstance
				# There are times when you have holdings of an asset that you don't want to trade/get rates of
				
				raise AssetNotFound("Tried to update holdings of an unexisting Asset! {}-{}".format(ex, name))
		
		return self.get_holdings()
		
	def pair_exists(self, pair: Union[str, list, tuple]) -> bool:
		"""
		Returns False if pair is not found within the portfolio
		
		:param pair: pair in string format or list of strings as [exchange, coin, quote]
		
		:return: bool
		"""
		if type(pair) == str:
			pair = pair.split("_")
			
		if len(pair) != 3:
			raise UnrecognizedPairlFormat(pair)
		
		for el in pair:
			if type(el) is not str:
				raise UnrecognizedPairlFormat(pair)
		
		try:
			self.pairs[pair[0]][pair[1]][pair[2]]
		except KeyError:
			return False
		return True
		
	def get_pair_list(self) -> list:
		"""
		Returns a list of all the pairs in the portfolio, empty if none.
		
		:return: List of pair objects
		"""
		
		found_pairs = []
		for d1, a in self.pairs.items():
			for d2, b in a.items():
				for d3, c in b.items():
					found_pairs.append(c)
		
		return found_pairs
	
	def get_holdings(self) -> dict:
		"""
		Returns a dictionary with the amount held by assets per exchange
		
		:return: The dictionary
		"""
		result = {}
		
		for e in self.ex_asset.keys():
			result[e] = {}
			for a, o in self.ex_asset[e].items():
				if a == "object":
					continue
				result[e][a] = o.am
		
		return result
	
	def get_usd_value(self) -> dict:
		"""
		Returns a dictionary of [Exchange.id][Asset.id] = [amount, usd_value]
		If there is no rate for ASSET->USD then usd_value = None
		"""
		
		holdings = self.get_holdings()
		result = {}
		
		for ex, data in holdings.items():
			result[ex] = {}
			for ass, am in data.items():
				if ass == "USD":
					usd_value = am
				else:
					try:
						pair = "{}_{}_USD".format(ex, ass)
						pair = self.get_pair_by_id(pair)
						if pair is None:
							rate1 = self.get_pair_by_id("{}_{}_BTC".format(ex, ass)).rate
							rate2 = self.get_pair_by_id("{}_BTC_USD".format(ex)).rate
							usd_value = am*rate1*rate2
						else:
							rate = pair.rate
							usd_value = am*rate
					except:
						usd_value = None
				result[ex][ass] = [am, usd_value]
		
		return result

	def get_usd_only(self) -> float:
		"""
		Returns the value holded in USD form within the whole protfolio
		"""

		assval = self.get_usd_value()
		usdval = 0.

		for ex, data in assval.items():
			for ass, amval in data.items():
				if ass != "USD":
					continue
				usdval += amval[1] if amval[1] is not None else 0
		return usdval
	
	def get_full_usd_value(self) -> float:
		"""
		Returns the full value of the portfolio in USD form at current rates
		"""
		
		assval = self.get_usd_value()
		fullval = 0.
		
		for ex, data in assval.items():
			for ass, amval in data.items():
				fullval += amval[1] if amval[1] is not None else 0
				
		return fullval
	
	def get_usd_per_ex(self) -> dict:
		"""
		Returns a dict with full usd value at current rates per exchange
		"""
		
		assval = self.get_usd_value()
		exval = {}
		
		for ex, data in assval.items():
			exval[ex] = 0.
			for ass, amval in data.items():
				exval[ex] += amval[1] if amval[1] is not None else 0
		
		return exval
		
	def get_assets(self) -> Dict[str, Dict[str, Asset]]:
		"""
		Returns a dictionary with asset objects per exchange
		
		:return: The dictionary
		"""
		result = {}
		
		for e in self.ex_asset.keys():
			result[e] = {}
			for a, o in self.ex_asset[e].items():
				if a == "object":
					continue
				result[e][a] = o
		
		return result

	def get_possible_loops(self, depth: int = 3) -> List[Tuple[Pair, ...]]:
		"""
		Returns all the theorethically possible and consistent
		loops within the already added pairs.
		
		:param depth: Lenght of the loop. Will only search for loops of that lenght, not less, but exactly that.
		:return: A list ot tuples of pairs, where each tuple represents a different loop. An empty list if none is found.
		"""
		if self._possible_loops is not None:
			return self._possible_loops

		all_pairs = self.get_pair_list()
		
		possible = []
		for sequence in itertools.permutations(all_pairs, depth):
			if self.check_loop_consistency(sequence):
				possible.append(tuple(sequence))
		return possible
		
	@staticmethod
	def check_loop_consistency(pair_sequence: Tuple[Pair, ...]) -> bool:
		"""
		Returns False if the loop (as a sequence of pairs):
		- Is not "closed".
		- Is not "chained".
		True otherwise.
		
		:param pair_sequence: The loop as a tuple of pairs
		:return:
		"""
		if len(pair_sequence) < 2:
			return False
		
		starting_coin = pair_sequence[0].coin.id
		starting_quote = pair_sequence[0].quote.id
		ending_quote = pair_sequence[-1].quote.id
		if starting_coin != ending_quote:
			return False
		
		for i in range(len(pair_sequence) - 1):
			if starting_quote != pair_sequence[i + 1].coin.id:
				return False
			starting_quote = pair_sequence[i + 1].quote.id

		return True

	def pairs_with_data(self, threshold: timedelta) -> List[Pair]:
		"""
		Returns the list of pairs with data more recent than now - threshold

		:return: A list of pair instances.
		"""

		out = []

		for pair in self.get_pair_list():
			if pair.time_since_update <= threshold:
				out.append(pair)

		return out

	def report(self, threshold: timedelta) -> dict:
		"""
		Returns a dictionary with a report about which pairs has recent data.
		Keys are:
		- all: true if everything has data
		- overview: number of pairs with data / total pairs
		- with: list of pair ids with data
		- withouth: list of pair ids without data
		- exchange: dict of exchange: bool, where bool = all its pairs have data

		:param threshold: the threshold that defines having recent data or not
		"""

		out = {"all": False, "overview": "", "with": [], "without": [], "exchanges": {}}

		total = [x.time_since_update < threshold for x in self.get_pair_list()]
		out["all"] = all(total)
		total = "{}/{}".format(sum(total), len(total))
		out["overview"] = total

		wi = [x.id for x in self.get_pair_list() if x.time_since_update < threshold]
		wo = [x.id for x in self.get_pair_list() if x.time_since_update > threshold]

		out["with"] = wi
		out["without"] = wo

		result = {}
		for ex, symblist in self.get_pairs_full().items():
			result[ex] = all([x.time_since_update < threshold for x in symblist.values()])

		out["exchanges"] = result

		return out

	def data_flag(self) -> bool:
		"""
		Returns TRUE if data has been added within the last second, false otherwise
		"""

		for pair in self.get_pair_list():
			if pair.time_since_update <= timedelta(seconds=3):
				return True

		return False

	def last_data_td(self) -> timedelta:
		tdelta = []
		for pair in self.get_pair_list():
			tdelta.append(pair.time_since_update)
		return min(tdelta)

	def get_virtual_rate(self, exchange: str, asset: str, quote_asset: str, vehicle_asset: str = "BTC") -> Optional[float]:
		"""
		Returns a virtual conversion rate between two assets that (may not form a pair)
		using their comparison to a third one.
		Quote asset = (Asset -> Vehicle rate) * (Vehicle -> Quote rate)

		:param exchange: Exchange in string form
		:param asset: The initial asset
		:param quote_asset: The quote
		:param vehicle_asset: The referential asset
		:return: Virtual rate if possible, None if not.
		"""

		s1 = self.get_pair_by_id("{}_{}_{}".format(exchange, asset, vehicle_asset))
		s2 = self.get_pair_by_id("{}_{}_{}".format(exchange, vehicle_asset, quote_asset))

		if s1 is None or s2 is None:
			return None

		virtual_rate = s1.rate * s2.rate
		return virtual_rate

	def predict_usd_val(self, exchange: str, asset: str, vehicle_asset: str = "BTC") -> Optional[float]:
		"""
		Predicts the USD value of an asset in a specific exchange. If no direct pair
		with USD is present then it will try to get a virtual rate to USD through a vehicle asset
		(BTC by default). Returns None if no direct or virtual rate is found.
		
		:param exchange:
		:param asset:
		:param vehicle_asset:
		:return: The predicted usd value of the specific asset in the exchange
		"""

		to_usd_str = "{}_{}_USD".format(exchange, asset)
		symb = self.get_pair_by_id(to_usd_str)
		if symb is None:
			rate = self.get_virtual_rate(exchange, asset, "USD", vehicle_asset)
			if rate is None:
				return None
		else:
			rate = symb.rate
		assobj = self.get_assets()[exchange][asset]
		return assobj.am * rate

	def add_pair_reverses(self):
		"""
		Adds a reversed pair per already added pair

		:return: None
		"""
		to_add = []
		for pair in self.get_pair_list():
			to_add.append("{}_{}_{}".format(pair.ex.id, pair.quote.id, pair.coin.id))

		for pair in to_add:
			self.add_pair(pair)

	def set_fake_holdings(self):
		"""
		Addss 100 units of every asset in every exchange

		:return:
		"""
		for pair in self.get_pair_list():
			pair.coin._hold = 100
			pair.quote._hold = 100
