from cryptool.exchanges.binance import Binance

env_exchange_public_key = 'x'
env_exchange_secret_key = 'y'

timeframe = {'interval': '1h', 'unit': 'hour', 'samples': 361}
product = {'symbol': 'ETHUSDT'}

binance = Binance(env_exchange_public_key, env_exchange_secret_key)

stock = binance.symbol_history_get(product, timeframe['interval'], unit=timeframe['unit'], samples=timeframe['samples'])
print(stock)