

class FeesEmpty(object):
	
	def __init__(self):
		"""
		An empty fee model returning 0% fees
		"""
	
	@property
	def rate(self):
		return 0.


class FeesTest(object):
	def __init__(self):
		"""
		A test case for fees. Returns a flat 5% fee
		"""
	
	@property
	def rate(self):
		return 0.05


class FeesKraken(object):
	
	def __init__(self):
		"""
		Based on zero tier taker fee
		https://www.kraken.com/features/fee-schedule
		"""
		pass
	
	@property
	def rate(self):
		return 0.0026
	
	
class FeesCoinbase(object):
	
	def __init__(self):
		"""
		Based on the second tier taker fee
		https://pro.coinbase.com/fees
		"""
		pass
	
	@property
	def rate(self):
		return 0.0035
	
	
class FeesBinance(object):
	
	def __init__(self):
		"""
		Based on first tier taker fee
		https://www.binance.com/en/fee/schedule
		"""
		pass
	
	@property
	def rate(self):
		return 0.001
	
	
class FeesBitmex(object):
	
	def __init__(self):
		"""
		Single tier system
		https://www.bitmex.com/app/fees
		"""
		pass
	
	@property
	def rate(self):
		return 0.00075
	
	
class FeesBittrex(object):
	
	def __init__(self):
		"""
		Single tier system
		https://www.cryptowisser.com/exchange/bittrex/
		"""
		pass
	
	@property
	def rate(self):
		return 0.002
	

class FeesGemini(object):
	
	def __init__(self):
		"""
		A tier system similar to others
		https://gemini.com/fees/activetrader-fee-schedule#active-trader
		"""
	
	@property
	def rate(self):
		return 0.0035


class FeesBitstamp(object):
	
	def __init__(self):
		"""
		A tier system similar to others
		https://www.bitstamp.net/fee-schedule/
		"""
	
	@property
	def rate(self):
		return 0.0025


class FeesOanda(object):
	
	def __init__(self):
		"""
		Fees built in spread, computed in pips. Average of 1.2 pips of fees per trade.
		https://brokerchooser.com/broker-reviews/oanda-review/oanda-fees
		"""
		pass
	
	@property
	def rate(self):
		# 1.2*0.01*0.01 = 0.00012 --- the average fee per trade
		return 0.00012

class FeesBitfinex(object):

	def __init__(self):
		"""
		Fees based on the first tier of bitfinex fees:
		https://www.bitfinex.com/fees/
		"""
		pass

	@property
	def rate(self):
		return 0.002

class FeesPoloniex(object):

	def __init__(self):
		"""
		Fees based on https://poloniex.com/fee-schedule
		"""

	@property
	def rate(self):
		return 0.00125

