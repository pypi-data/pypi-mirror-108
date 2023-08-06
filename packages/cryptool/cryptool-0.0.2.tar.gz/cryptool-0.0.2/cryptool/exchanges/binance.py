import datetime
import inspect
import json
import urllib3

from binance.client import Client
import pandas as pd

urllib3.disable_warnings()

class Binance:
    def __init__(self, public_key, secret_key):
        self.client = Client(public_key, secret_key)

        # cert_reqs='CERT_REQUIRED' is default and highly recommend to leave it on
        # see https://urllib3.readthedocs.io/en/latest/user-guide.html#certificate-verification
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_NONE',
            retries=urllib3.Retry(3, redirect=2),
            timeout=10.0
        )

        self.prefix_url = 'https://api.binance.com/api/v3'
        self.bases_unstable = set()
        self.coins = {
            'fiat': {'AUD', 'BRL', 'EUR', 'GBP', 'NGN', 'RUB', 'TRY', 'UAH', 'ZAR'},
            'stable': {'BIDR', 'BUSD', 'BVND', 'DAI', 'IDRT', 'PAX', 'TUSD', 'USDC', 'USDT', 'VAI'}
        }
        self.quotes_unstable = set()
        self.spot_assets = set()
        self.symbols_crypto = []


    def symbol_history_get(self, signal, interval, unit='day', samples=101): #, date_start, date_end):
        date_start = (datetime.datetime.now() - datetime.timedelta(samples + 1)).strftime('%d %b, %Y')
        date_end = (datetime.datetime.now() - datetime.timedelta(1)).strftime('%d %b, %Y')

        # bars = self.client.get_historical_klines(signal['symbol'], '1d', date_start, date_end) # , limit=100)
        # self.client.KLINE_INTERVAL_1HOUR
        # bars = self.client.get_historical_klines(signal['symbol'], '1d', '{} day ago UTC'.format(samples))

        bars = self.client.get_historical_klines(signal['symbol'], interval, '{} {} ago UTC'.format(samples, unit))
        # bars = self.client.get_historical_klines(signal['symbol'], interval, date_start, date_end)

        binance_candle_columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'ct', 'qav', 'not', 'tbbav', 'tbqav', 'i']
        btc_df = pd.DataFrame(bars, columns=binance_candle_columns)

        btc_df['time'] = pd.to_datetime(btc_df['date'], unit='ms').tolist()

        return pd.DataFrame({
            'time': btc_df['time'].tolist(),
            'high': btc_df['high'].astype(float).tolist(),
            'low': btc_df['close'].astype(float).tolist(),
            'close': btc_df['close'].astype(float).tolist(),
            'volume': pd.to_numeric(btc_df['volume'], errors='coerce').astype(int).tolist()
        })


    def symbols_get(self): #, cmc_top100_symbols_names):
        function_name = inspect.currentframe().f_code.co_name
        symbols = []

        try:
            response = self.http.request('GET', '{}/exchangeInfo'.format(self.prefix_url))

            if response.status == 200:
                data_response = json.loads(response.data.decode('utf-8'))

                for product in data_response['symbols']:
                    symbol = {
                        'baseAsset': product['baseAsset'], # BTC
                        'quoteAsset': product['quoteAsset'], # USDT
                        'symbol': product['symbol'], # BTCUSDT
                        'sdema': False,
                        'suggested': False,
                        'indicator_summary': ''
                    }
                    if (
                        (product['status'] == 'TRADING') and
                        ('SPOT' in product['permissions']) and
                        ('LEVERAGED' not in product['permissions'])
                    ):
                        if (
                            (product['baseAsset'] not in self.coins['fiat']) and
                            (product['quoteAsset'] not in self.coins['fiat'])
                        ):
                            self.symbols_crypto.append(symbol)

                        if (
                            (product['baseAsset'] not in self.coins['fiat']) and
                            (product['baseAsset'] not in self.coins['stable'])
                        ):
                            self.bases_unstable.add(product['baseAsset'])

                        if (
                            (product['quoteAsset'] not in self.coins['fiat']) and
                            (product['quoteAsset'] not in self.coins['stable'])
                        ):
                            self.quotes_unstable.add(product['quoteAsset'])

                        if (
                            (product['baseAsset'] not in self.coins['fiat']) and
                            (product['baseAsset'] not in self.coins['stable']) and
                            (product['quoteAsset'] not in self.coins['fiat']) and
                            (product['quoteAsset'] in self.coins['stable'])
                        ):
                            symbols.append(symbol)
                            self.spot_assets.add(product['baseAsset'])
                return symbols
            else:
                raise Exception('{} internal_1 Exception HTTP != 200'.format(function_name))
        except Exception as err:
            raise Exception('{} main Exception'.format(function_name)).with_traceback(err.__traceback__)


    def symbols_get_quote_given(self, quote_symbol): #, cmc_top100_symbols_names):
        function_name = inspect.currentframe().f_code.co_name
        symbols = set()

        try:
            response = self.http.request('GET', '{}/exchangeInfo'.format(self.prefix_url))

            if response.status == 200:
                data_response = json.loads(response.data.decode('utf-8'))

                for product in data_response['symbols']:
                    if (
                        (product['status'] == 'TRADING') and
                        ('SPOT' in product['permissions']) and
                        ('LEVERAGED' not in product['permissions'])
                    ):
                        if (product['quoteAsset'] == quote_symbol):
                            symbols.add(product['baseAsset'])
                return symbols
            else:
                raise Exception('{} internal_1 Exception HTTP != 200'.format(function_name))
        except Exception as err:
            raise Exception('{} main Exception'.format(function_name)).with_traceback(err.__traceback__)