# Trading Framework (in progress)

This project, born based on previous works, aims to provide a free and versatile framework for trading algorithm development. The project is simple in its nature and very easy to learn, trying to be a good fast and lightweight prototyping tool for market replay simulations.

So far only the abstractions of portfolio, pair, asset, exchange and fee models are provided. All the code is well documented and easy to improve. It can only deal with bid/ask updates. This is a work in progress project that will grow over time based on several projects I've done in the past. Next items in the todo listm are:

  - Trading simulation
  - A master file to generate the basic simulation loop and initialize everything.
  - Market depth.
  - Slippage model.
  - Wrapper class to convert historical data to this repo's data input format.

# Usage

A portfolio instance can bre created as:

```python
from portfolio import Portfolio

port = Portfolio()

pair = port.add_pair("KRAKEN_USD_BTC") # Initializes a pair and returns it


pair.rate # Last known exchange rate from USD to BTC
pair.last_update_time # Last update time for the rate
pair.coin # USD asset object
pair.quote # BTC asset object
pair.ex # KRAKEN exchange object
pair.ex.fee_rate # Fee rate for kraken

# No trading method is yet implemented
```

Also, Portfolio has lots of methods for quality of life:

```python
pair = port.get_pair_by_id("KRAKEN_USD_BTC") # This returns a pair object that can match the string
pair.rate # = 0.1234


pair = port.get_pair_by_id("KRAKEN_USD_BTC")
port.get_pairs_by_coin(pair.coin) # Will return all the pairs with USD as coin
port.get_pairs_by_quote("BTC") # Will return all the pairs with BTC as quote
port.get_pairs_by_exchange(pair.ex) # Will return all the pairs within KRAKEN exchange

pair.coin.am # USD holdings in KRAKEN
pair.quote.am # BTC holdings in KRAKEN

port.get_assets() # Dict with Asset objects per Exchange
port.get_usd_value() # Dict of USD value per exchange (virtually converting all holdings to USD)
# And much more
```


Prices can be updated with a wrapper object:

```python
from base import PriceUpdate
from datetime import datetime

# A price update from an exchange or historical data can be expressed as
update_from_exchange = {
			"exchange": "KRAKEN",
			"coin": "USD",
			"quote": "BTC",
			"rate": 0.1234,
			"datetime": datetime.now() # Or the historical datetime
		}

# PriceUpdate will check that all required fields are present and will provide a wrapper
# api that Portfolio understands. This can easily be expanded to include market depth informacion and more
update = PriceUpdate(update_from_exchange)
port.push_update(update) # Pushing the update will automatically organize everything

pair = port.get_pair_by_id("KRAKEN_USD_BTC") # This returns a pair object that can match the string
pair.rate # = 0.1234

```

