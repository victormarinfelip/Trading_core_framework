"""
Victor Marin Felip
vicmf88@gmail.com
"""

from portfolio_base import *
from datetime import datetime
import copy
import unittest
import os
import sys

sys.path.append(os.path.abspath('../'))


class UpdateTests(unittest.TestCase):

	def setUp(self):
		self.now_upd = datetime.now()
		self.upd1 = {
			"exchange": "KRAKEN",
			"coin": "USD",
			"quote": "BTC",
			"rate": 0.257,
			"datetime": self.now_upd
		}
	
	def test_update_parses_ex(self):
		u = PriceUpdate(self.upd1)
		self.assertEqual(u.ex, "KRAKEN")

	def test_update_parses_coin(self):
		u = PriceUpdate(self.upd1)
		self.assertEqual(u.coin, "USD")
		
	def test_update_parses_quote(self):
		u = PriceUpdate(self.upd1)
		self.assertEqual(u.quote, "BTC")

	def test_update_parses_id(self):
		u = PriceUpdate(self.upd1)
		self.assertEqual(u.id, ("KRAKEN", "USD", "BTC"))
	
	def test_update_parses_best_rate(self):
		u = PriceUpdate(self.upd1)
		self.assertEqual(u.best_rate, 0.257)

	def test_update_parses_systime(self):
		u = PriceUpdate(self.upd1)
		self.assertEqual(u.systime, self.now_upd)
		
	def test_expected_keys(self):
		for key in self.upd1.keys():
			d = copy.copy(self.upd1)
			del d[key]
			self.assertRaises(KeyError, PriceUpdate, d)
		
		
class AssetUpdateTests(unittest.TestCase):
	
	def setUp(self):
		self.now_upd = datetime.now()
		self.upd1 = {
			"exchange": "KRAKEN",
			"datetime": self.now_upd,
			"assets": [
				["USD", 37],
				["ETH", 50],
				["DOGE", 4]
			]
		}
	
	def tests_assetupdate_parses_ex(self):
		u = AssetUpdate(self.upd1)
		self.assertEqual(u.ex, "KRAKEN")
	
	def tests_assetupdate_parses_assets(self):
		u = AssetUpdate(self.upd1)
		self.assertEqual(u.assetlist, ["USD", "ETH", "DOGE"])
	
	def tests_assetupdate_parses_holdings(self):
		u = AssetUpdate(self.upd1)
		self.assertEqual(u.holdinglist, [37, 50, 4])
	
	def tests_assetupdate_parses_datetime(self):
		u = AssetUpdate(self.upd1)
		self.assertEqual(u.systime, self.now_upd)
	
	def test_expected_keys(self):
		for key in self.upd1.keys():
			d = copy.copy(self.upd1)
			del d[key]
			self.assertRaises(KeyError, AssetUpdate, d)


class AssetTest(unittest.TestCase):
	
	def setUp(self):
		self.asset = Asset("USD")
	
	def test_id(self):
		self.assertEqual(self.asset.id, "USD")
		
	def test_amount_zero(self):
		self.assertEqual(self.asset.am, 0)
		
	def test_amount_change(self):
		self.asset.am = 3.421
		self.assertEqual(self.asset.am, 3.421)


class ExchangeTest(unittest.TestCase):
	
	def setUp(self):
		self.ex = Exchange("KRAKEN")
		
	def test_id(self):
		self.assertEqual(self.ex.id, "KRAKEN")
		
	def test_str(self):
		self.assertEqual(str(self.ex), "KRAKEN")
