import unittest
import os
import sys
from datetime import timedelta, datetime
from portfolio_base import AssetUpdate, PriceUpdate
from portfolio_symbol import Portfolio, Symbol
from algotools import Loop, LoopManager
import time

sys.path.append(os.path.abspath('../'))

class LoopTests(unittest.TestCase):

	def setUp(self):
		self.symbol_ids = ["KRAKEN_USD_BTC", "KRAKEN_BTC_ETH", "KRAKEN_ETH_USD", "COINBASE_ETH_USD"]
		self.port = Portfolio()
		self.updates = []
		
		for symbol in self.symbol_ids:
			self.port.add_symbol(symbol)
			
		for symbol in self.port.get_symbol_list():
			symbup = {
				"coin": symbol.coin.id,
				"quote": symbol.quote.id,
				"exchange": symbol.ex.id,
				"rate":  2,
				"datetime": datetime.now()
			}
			self.updates.append(symbup)
		
		self.assupdates = []
		ass_ex = self.port.get_assets()
		for ex, asslist in ass_ex.items():
			assup = {
				"exchange": ex,
				"datetime": datetime.now(),
				"assets": []
			}
			for ass in asslist.keys():
				assup["assets"].append([ass, 10])
			self.assupdates.append(assup)
			
		symbl = self.port.get_symbol_list()
		
		self.sampleloop = Loop(tuple([s for s in symbl if "COINBASE" not in s.id]))
		
	def test_symbol_returns_list_of_symbols(self):
		for symbol in self.sampleloop.symbols:
			self.assertIsInstance(symbol, Symbol)
		
	def test_id(self):
		expected_id = "".join(map(str, self.symbol_ids[:-1]))
		self.assertEqual(expected_id, self.sampleloop.id)
		
	def test_check_holds_on_asset(self):
		self.assertFalse(self.sampleloop._check_holds_on_assets())
		asupd = [x for x in self.assupdates if x["exchange"] == "KRAKEN"][0]
		assup = AssetUpdate(asupd)
		self.port.adjust_holdings_from_assetupd(assup)
		self.assertTrue(self.sampleloop._check_holds_on_assets())
		
	def test_check_all_symbols_rate(self):
		self.assertFalse(self.sampleloop._check_all_symbols_rate())
		updates_l = []
		for up in self.updates:
			if up["exchange"] != "KRAKEN":
				continue
			updates_l.append(PriceUpdate(up))
		
		for up in updates_l:
			self.port.push_update(up)
			
		self.assertTrue(self.sampleloop._check_all_symbols_rate())
	
	def test_check_time_condition(self):
		thr = timedelta(seconds = 0.05)
		thr2 = timedelta(seconds = 0.2)
		
		for up in self.updates:
			up = PriceUpdate(up)
			self.port.push_update(up)
		
		self.assertTrue(self.sampleloop._check_time_condition(thr))
		time.sleep(0.1)
		self.assertFalse(self.sampleloop._check_time_condition(thr))
		self.assertTrue(self.sampleloop._check_time_condition(thr2))
		
	def test_max_initial_amount(self):
		pass
	
	def test_loop_efficiency(self):
		pass
	
	def test_backwards_convert(self):
		pass
	
	def test_convert(self):
		pass
	
	def test_abs_fees(self):
		pass
	
	def test_simulate(self):
		pass
	
	def test_sym_report(self):
		pass
	
	def test_profitability(self):
		pass
	
	