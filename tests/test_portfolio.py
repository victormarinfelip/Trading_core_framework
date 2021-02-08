from portfolio_symbol import *
from engine_errors import *
from datetime import datetime, timedelta
import time
import unittest
import os
import sys

sys.path.append(os.path.abspath('../'))


class SymbolTests(unittest.TestCase):
	
	def setUp(self):
		self.ex = Exchange("KRAKEN")
		self.ex2 = Exchange("COINBASE")
		
		self.asset = Asset("USD")
		self.asset2 = Asset("ETH")
		self.asset3 = Asset("BTC")
		
		self.now_upd = datetime.now()
		self.upd = {
			"exchange": "KRAKEN",
			"coin": "USD",
			"quote": "BTC",
			"rate": 0.257,
			"datetime": self.now_upd
		}
		
		self.update = PriceUpdate(self.upd)
		
	def test_ex(self):
		s = Symbol(self.ex, self.asset, self. asset2)
		self.assertEqual(s.ex, self.ex)

	def test_coin(self):
		s = Symbol(self.ex, self.asset, self. asset2)
		self.assertEqual(s.coin, self.asset)

	def test_quote(self):
		s = Symbol(self.ex, self.asset, self. asset2)
		self.assertEqual(s.quote, self.asset2)
		
	def test_id(self):
		s = Symbol(self.ex, self.asset, self. asset2)
		self.assertEqual("KRAKEN_USD_ETH", s.id)

	def test_update_wrong_exchange(self):
		s = Symbol(self.ex, self.asset, self. asset2)

		self.upd["exchange"] = "COINBASE"
		self.update = PriceUpdate(self.upd)
		self.assertRaises(WrongExchangeError, s.add_update, self.update)
	
	def test_update_wrong_coin(self):
		s = Symbol(self.ex, self.asset, self. asset2)

		self.upd["coin"] = "BTC"
		self.update = PriceUpdate(self.upd)
		self.assertRaises(WrongAssetError, s.add_update, self.update)

	def test_update_wrong_quote(self):
		s = Symbol(self.ex, self.asset, self. asset2)

		self.upd["quote"] = "BTC"
		self.update = PriceUpdate(self.upd)
		self.assertRaises(WrongAssetError, s.add_update, self.update)
	
	def test_rate_is_set(self):
		s = Symbol(self.ex, self.asset, self. asset3)
		s.add_update(self.update)
		
		self.assertEqual(s.rate, 0.257)
		
	def test_time_is_set(self):
		s = Symbol(self.ex, self.asset, self. asset3)
		s.add_update(self.update)
		
		self.assertEqual(s.last_update_time, self.now_upd)

	def test_time_is_measured(self):
		s = Symbol(self.ex, self.asset, self. asset3)
		s.add_update(self.update)
		time.sleep(0.1)
		self.assertGreater(s.time_since_update, timedelta(seconds=0.099))
		self.assertLess(s.time_since_update, timedelta(seconds=0.101))
		
	def test_raises_on_equal_coin_quote(self):
		ex = Exchange("KRAKEN")
		c = Asset("USD")
		q = Asset("USD")
		
		self.assertRaises(WrongAssetError, Symbol, ex, c, q)


class PortfolioTests(unittest.TestCase):
	
	def setUp(self):
		self.ex1 = Exchange("KRAKEN")
		self.ex2 = Exchange("COINBASE")
		self.ass1 = Asset("USD")
		self.ass2 = Asset("BTC")
		self.ass3 = Asset("ETH")
		
		self.symbol1 = Symbol(self.ex1, self.ass1, self.ass2)
		
	def test_add_symbol_creates_symbol_basic(self):
		p = Portfolio()
		s = p.add_symbol((self.ex1, self.ass1, self.ass2))
		self.assertEqual(s.id, "KRAKEN_USD_BTC")
		
	def test_add_symbol_reuses_asset_coin(self):
		p = Portfolio()
		coin2 = Asset("USD")
		s1 = p.add_symbol((self.ex1, self.ass1, self.ass2))
		s2 = p.add_symbol((self.ex1, coin2, self.ass3))
		self.assertEqual(s1.coin, s2.coin)
		
		p = Portfolio()
		s1 = p.add_symbol("KRAKEN_USD_BTC")
		s2 = p.add_symbol("KRAKEN_USD_ETH")
		self.assertEqual(s1.coin, s2.coin)
		
	def test_add_symbol_reuses_asset_quote(self):
		p = Portfolio()
		coin2 = Asset("BTC")
		s1 = p.add_symbol((self.ex1, self.ass1, self.ass2))
		s2 = p.add_symbol((self.ex1, self.ass3, coin2))
		self.assertEqual(s1.quote, s2.quote)
		
		p = Portfolio()
		s1 = p.add_symbol("KRAKEN_BTC_ETH")
		s2 = p.add_symbol("KRAKEN_USD_ETH")
		self.assertEqual(s1.quote, s2.quote)
		
	def test_add_symbol_reuses_exchange(self):
		p = Portfolio()
		ex2 = Exchange("KRAKEN")
		s1 = p.add_symbol((self.ex1, self.ass1, self.ass2))
		s2 = p.add_symbol((ex2, self.ass1, self.ass3))
		self.assertEqual(s1.ex, s2.ex)
		
		p = Portfolio()
		s1 = p.add_symbol("KRAKEN_BTC_ETH")
		s2 = p.add_symbol("KRAKEN_USD_ETH")
		self.assertEqual(s1.ex, s2.ex)
		
	def test_add_symbol_doesnt_reuse_on_diff_exchange(self):
		p = Portfolio()
		s1 = p.add_symbol("KRAKEN_USD_BTC")
		s2 = p.add_symbol("COINBASE_USD_BTC")
		
		self.assertNotEqual(s1.ex, s2.ex)
		self.assertNotEqual(s1.coin, s2.coin)
		self.assertNotEqual(s1.quote, s2.quote)
		
		p = Portfolio()
		s1 = p.add_symbol((self.ex1, self.ass1, self.ass2))
		s2 = p.add_symbol((self.ex2, self.ass1, self.ass2))
		
		self.assertNotEqual(s1.ex, s2.ex)
		self.assertNotEqual(s1.coin, s2.coin)
		self.assertNotEqual(s1.quote, s2.quote)
		
	def test_add_symbol_raises_index_on_bad_format(self):
		p = Portfolio()
		s1 = "KRAKEN_USD_BTC_ETH"
		s2 = (self.ex1, self.ass1, self.ass2, self.ass3)
		self.assertRaises(IndexError, p.add_symbol, s1)
		self.assertRaises(IndexError, p.add_symbol, s2)
		
	def test_add_symbol_raises_unrecognized_on_bad_format(self):
		p = Portfolio()
		s2 = [self.ex1, self.ass1, self.ass2, self.ass3]
		self.assertRaises(UnrecognizedSymbolFormat, p.add_symbol, s2)
		
	def test_add_symbol_raises_already_implemented_symbol(self):
		s1 = "KRAKEN_USD_BTC"
		s2 = (self.ex1, self.ass1, self.ass2)
		
		p = Portfolio()
		p.add_symbol(s1)
		self.assertRaises(AlreadyImplementedSymbol, p.add_symbol, s2)
		
	def test_get_symbols_by_ex_finds(self):
		s1 = "KRAKEN_ETH_BTC"
		s2 = "KRAKEN_USD_BTC"
		s3 = "COINBASE_ETH_BTC"
		s4 = "BINANCE_DOGE_BTC"
		
		p = Portfolio()
		p.add_symbol(s1)
		p.add_symbol(s2)
		p.add_symbol(s3)
		p.add_symbol(s4)
		
		kraken_symb = p.get_symbols_by_exchange("KRAKEN")
		kraken_symb2 = p.get_symbols_by_exchange(Exchange("KRAKEN"))
		
		self.assertEqual(kraken_symb, kraken_symb2)
		
		as_str = [x.id for x in kraken_symb]
		
		self.assertTrue(s1 in as_str)
		self.assertTrue(s2 in as_str)
		self.assertEqual(len(as_str), 2)
		
		coinbase_symb = p.get_symbols_by_exchange("COINBASE")
		as_str = [x.id for x in coinbase_symb]

		self.assertEqual(as_str, [s3])
		
		none_symb = p.get_symbols_by_exchange("BITMEX")
		
		self.assertEqual(none_symb, [])
		
	def test_get_symbols_by_coin_finds(self):
		s1 = "KRAKEN_ETH_BTC"
		s2 = "KRAKEN_USD_BTC"
		s3 = "COINBASE_ETH_BTC"
		s4 = "BINANCE_DOGE_BTC"
		
		p = Portfolio()
		p.add_symbol(s1)
		p.add_symbol(s2)
		p.add_symbol(s3)
		p.add_symbol(s4)
		
		coin_symb = p.get_symbols_by_coin("ETH")
		coin_symb2 = p.get_symbols_by_coin(Asset("ETH"))
		
		self.assertEqual(coin_symb, coin_symb2)
		
		as_str = [x.id for x in coin_symb]
		
		self.assertTrue(s1 in as_str)
		self.assertTrue(s3 in as_str)
		self.assertEqual(len(as_str), 2)
		
		coin_symb = p.get_symbols_by_coin("USD")
		as_str = [x.id for x in coin_symb]

		self.assertEqual(as_str, [s2])
		
		none_symb = p.get_symbols_by_coin("LITE")
		
		self.assertEqual(none_symb, [])
		
	def test_get_symbols_by_quot_finds(self):
		s1 = "KRAKEN_ETH_BTC"
		s2 = "KRAKEN_USD_ETH"
		s3 = "COINBASE_ETH_USD"
		s4 = "BINANCE_DOGE_ETH"
		
		p = Portfolio()
		p.add_symbol(s1)
		p.add_symbol(s2)
		p.add_symbol(s3)
		p.add_symbol(s4)
		
		quote_symb = p.get_symbols_by_quote("ETH")
		quote_symb2 = p.get_symbols_by_quote(Asset("ETH"))
		
		self.assertEqual(quote_symb, quote_symb2)
		
		as_str = [x.id for x in quote_symb]
		
		self.assertTrue(s2 in as_str)
		self.assertTrue(s4 in as_str)
		self.assertEqual(len(as_str), 2)
		
		quote_symb = p.get_symbols_by_quote("USD")
		as_str = [x.id for x in quote_symb]

		self.assertEqual(as_str, [s3])
		
		none_symb = p.get_symbols_by_quote("LITE")
		
		self.assertEqual(none_symb, [])
		
	def test_get_symbol_by_id(self):
		p = Portfolio()
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		dum2 = "KRAKEN_USD_ETH"
		
		p.add_symbol(symb_id)
		p.add_symbol(dum1)
		p.add_symbol(dum2)
		
		found = p.get_symbol_by_id(symb_id)
		self.assertEqual(found.id, symb_id)
		
		found = p.get_symbol_by_id("POTATO_USD_ETH")
		self.assertIsNone(found)
		
	def test_push_update(self):
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		dum2 = "KRAKEN_USD_ETH"
		
		p.add_symbol(symb_id)
		p.add_symbol(dum1)
		p.add_symbol(dum2)
		
		upd1 = {
			"exchange": "KRAKEN",
			"coin": "USD",
			"quote": "BTC",
			"rate": 0.257,
			"datetime": datetime.now()
		}
		
		u = PriceUpdate(upd1)
		updated_symb = p.push_update(u)
		
		self.assertEqual(updated_symb.rate, 0.257)
		self.assertEqual(updated_symb.coin.id, "USD")
		self.assertEqual(updated_symb.quote.id, "BTC")
		
		updated_symb = p.get_symbol_by_id(symb_id)
		
		self.assertEqual(updated_symb.rate, 0.257)
		self.assertEqual(updated_symb.coin.id, "USD")
		self.assertEqual(updated_symb.quote.id, "BTC")
		
	def test_push_update_raises_not_implemented(self):
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		dum2 = "KRAKEN_USD_ETH"
		
		p.add_symbol(symb_id)
		p.add_symbol(dum1)
		p.add_symbol(dum2)
		
		upd1 = {
			"exchange": "KRAKEN",
			"coin": "USD",
			"quote": "LITE",
			"rate": 0.257,
			"datetime": datetime.now()
		}
		
		u = PriceUpdate(upd1)
		self.assertRaises(SymbolNotImplemented, p.push_update, u)
		
		upd1 = {
			"exchange": "KRAKEN",
			"coin": "LITE",
			"quote": "BTC",
			"rate": 0.257,
			"datetime": datetime.now()
		}
		
		u = PriceUpdate(upd1)
		self.assertRaises(SymbolNotImplemented, p.push_update, u)
		
		upd1 = {
			"exchange": "POTATO",
			"coin": "USD",
			"quote": "BTC",
			"rate": 0.257,
			"datetime": datetime.now()
		}
		
		u = PriceUpdate(upd1)
		self.assertRaises(SymbolNotImplemented, p.push_update, u)
		
	def test_adjust_holdings(self):
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		dum2 = "KRAKEN_USD_ETH"
		
		p.add_symbol(symb_id)
		p.add_symbol(dum1)
		p.add_symbol(dum2)
		
		upd1 = {
			"exchange": "KRAKEN",
			"datetime": datetime.now(),
			"assets": [
				["USD", 37],
				["ETH", 50],
			]
		}
		
		u = AssetUpdate(upd1)
		holdings = p.adjust_holdings_from_assetupd(u)
		
		self.assertEqual(holdings["KRAKEN"]["USD"], 37)
		self.assertEqual(holdings["KRAKEN"]["ETH"], 50)
		self.assertEqual(holdings["KRAKEN"]["BTC"], 0)
		self.assertEqual(holdings["COINBASE"]["USD"], 0)
		self.assertEqual(holdings["COINBASE"]["BTC"], 0)
	
	def test_adjust_holdings_rasies_assetnotfound(self):
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		dum2 = "KRAKEN_USD_ETH"
		
		p.add_symbol(symb_id)
		p.add_symbol(dum1)
		p.add_symbol(dum2)
		
		upd1 = {
			"exchange": "KRAKEN",
			"datetime": datetime.now(),
			"assets": [
				["USD", 37],
				["ETH", 50],
				["DOGE", 23]
			]
		}
		
		u = AssetUpdate(upd1)
		self.assertRaises(AssetNotFound, p.adjust_holdings_from_assetupd, u)
		
		upd1 = {
			"exchange": "COINBASE",
			"datetime": datetime.now(),
			"assets": [
				["USD", 37],
				["ETH", 50]
			]
		}
		
		u = AssetUpdate(upd1)
		self.assertRaises(AssetNotFound, p.adjust_holdings_from_assetupd, u)
	
	def test_symbol_exists(self):
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		
		p.add_symbol(symb_id)

		self.assertTrue(p.symbol_exists(symb_id))
		self.assertFalse(p.symbol_exists(dum1))
	
	def test_symbol_exists_raises_unrecognized(self):
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		
		p.add_symbol(symb_id)

		self.assertRaises(UnrecognizedSymbolFormat, p.symbol_exists, "KRAKENUSD_BTC")
		self.assertRaises(UnrecognizedSymbolFormat, p.symbol_exists, ["KRAKEN", "USD"])
		self.assertRaises(UnrecognizedSymbolFormat, p.symbol_exists, [Exchange("KRAKEN"), Asset("USD"), Asset("BTC")])
		
	def test_get_symbol_list(self):
		
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		dum2 = "KRAKEN_USD_ETH"
		
		p.add_symbol(symb_id)
		p.add_symbol(dum1)
		p.add_symbol(dum2)
		
		s_list = p.get_symbol_list()
		
		result = [s.id in [symb_id, dum1, dum2] for s in s_list]
		self.assertTrue(all(result))
		
		p = Portfolio()
		self.assertEqual(p.get_symbol_list(), [])
		
	def test_get_holdings(self):
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		dum2 = "KRAKEN_USD_ETH"
		
		p.add_symbol(symb_id)
		p.add_symbol(dum1)
		p.add_symbol(dum2)
		
		upd1 = {
			"exchange": "KRAKEN",
			"datetime": datetime.now(),
			"assets": [
				["USD", 37],
				["ETH", 50],
			]
		}
		
		upd2 = {
			"exchange": "COINBASE",
			"datetime": datetime.now(),
			"assets": [
				["BTC", 3],
			]
		}
		
		u = AssetUpdate(upd1)
		p.adjust_holdings_from_assetupd(u)
		u = AssetUpdate(upd2)
		p.adjust_holdings_from_assetupd(u)
		
		holds = p.get_holdings()
		
		self.assertEqual(holds["KRAKEN"]["USD"], 37)
		self.assertEqual(holds["KRAKEN"]["ETH"], 50)
		self.assertEqual(holds["KRAKEN"]["BTC"], 0)
		self.assertEqual(holds["COINBASE"]["BTC"], 3)
		self.assertEqual(holds["COINBASE"]["USD"], 0)

		upd3 = {
			"exchange": "COINBASE",
			"datetime": datetime.now(),
			"assets": [
				["BTC", 6],
			]
		}
		
		u = AssetUpdate(upd3)
		p.adjust_holdings_from_assetupd(u)
		
		holds = p.get_holdings()

		self.assertEqual(holds["COINBASE"]["BTC"], 6)
		
	def test_get_assets(self):
		p = Portfolio()
		
		symb_id = "KRAKEN_USD_BTC"
		dum1 = "COINBASE_USD_BTC"
		dum2 = "KRAKEN_USD_ETH"
		
		p.add_symbol(symb_id)
		p.add_symbol(dum1)
		p.add_symbol(dum2)
		
		assets = p.get_assets()
		
		for ex, asslist in assets.items():
			for assid, assob in asslist.items():
				self.assertIsInstance(assob, Asset)
				self.assertTrue(assob.id in ["USD", "BTC", "ETH"])
				self.assertEqual(assid, assob.id)
				
		self.assertEqual(assets["KRAKEN"]["USD"].id, "USD")
		self.assertEqual(assets["KRAKEN"]["BTC"].id, "BTC")
		self.assertEqual(assets["KRAKEN"]["ETH"].id, "ETH")
		
		self.assertEqual(assets["COINBASE"]["USD"].id, "USD")
		self.assertEqual(assets["COINBASE"]["BTC"].id, "BTC")
		
		# Let's test that the actual asset objects are the same one, just to be sure
	
		self.assertEqual(assets["KRAKEN"]["USD"], p.get_symbol_by_id("KRAKEN_USD_ETH").coin)
		
		self.assertEqual(assets["COINBASE"]["BTC"], p.get_symbol_by_id("COINBASE_USD_BTC").quote)
