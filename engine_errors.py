"""
Victor Marin Felip
vicmf88@gmail.com
"""


class EngineException(Exception):

	def __init__(self, *args):
		super().__init__()


class GeneralTimeoutError(EngineException):

	def __init__(self, msg):
		"""
		Raised when, after succesfully connecting to all channels
		one or more of these stop sending data for longer than a timeout
		period. A complete engine restart will follow.
		"""
		super().__init__()
		self.msg = msg

	def __str__(self):
		return "General timeout expired. {}".format(self.msg)
	

class WrongExchangeError(EngineException):

	def __init__(self, expected_ex, given_ex):
		"""
		Raised when the wrong exchange is passed to a pair and the like
		
		:param expected_ex: Expected exchange
		:param given_ex:  Given exchange
		"""
		super().__init__()
		self.exp = expected_ex
		self.giv = given_ex
		
	def __str__(self):
		return "Wrong Exchange: {0}, expected {1}".format(self.exp, self.giv)


class UnknownExchangeError(EngineException):

	def __init__(self, given_ex):
		"""
		Raised when an unknown exchange is dealt with
		
		:param given_ex: The unknown exchange
		"""
		super().__init__()
		self.giv = given_ex
		
	def __str__(self):
		return "Unknown exchange: {0}".format(self.giv)
	

class WrongAssetError(EngineException):

	def __init__(self, expected_as, given_as):
		"""
		Raised when the wrong asset id is passed to either the coin or the quote
		
		:param expected_as: Expected Asset
		:param given_as: Given Asset
		"""
		super().__init__()
		self.exp = expected_as
		self.giv = given_as
		
	def __str__(self):
		return "Wrong Asset: {0}, expected {1}".format(self.exp, self.giv)


class UnrecognizedPairlFormat(EngineException):
	
	def __init__(self, pair):
		"""
		Raised when an unrecognized pair format is passed to a pair constructor
		
		:param pair: the unrecognized item
		"""
		super().__init__()
		self.symb = pair
		
	def __str__(self):
		return "Unrecognized pair: {}".format(self.symb)


class AlreadyImplementedPair(EngineException):
	
	def __init__(self, pair):
		"""
		Raised when an duplicated pair is added to a portfolio
		
		:param pair: the duplicated item
		"""
		super().__init__()
		self.symb = pair
		
	def __str__(self):
		return "Already implemented pair: {}".format(self.symb)


class PairlNotImplemented(EngineException):
	
	def __init__(self, pair):
		"""
		Raised when an unexisting pair is added to a portfolio
		
		:param pair: the duplicated item
		"""
		super().__init__()
		self.symb = pair
		
	def __str__(self):
		return "pair doesn't exist: {}".format(self.symb)


class AssetNotFound(EngineException):
	
	def __init__(self, msg):
		"""
		Raised when an unexisting asset is added to a portfolio
		
		:param msg: Message to print
		"""
		super().__init__()
		self.msg = msg
		
	def __str__(self):
		return self.msg


class FeeModelNotFound(EngineException):
	
	def __init__(self, ex_id):
		"""
		Raised when an exchange is instanciated without a fee model coded
		
		:param ex_id: The id of the exchange
		"""
		super().__init__()
		self.ex_id = ex_id
		
	def __str__(self):
		return "Exchange doesn't have an implemented fee model: {}".format(self.ex_id)


class SimulationNotCompleted(EngineException):
	
	def __init__(self):
		"""
		Raised when a simulation report is called without the simulation having been run.
		"""
		super().__init__()
		
	def __str__(self):
		return "Simulation uncompleded, no report possible!"
