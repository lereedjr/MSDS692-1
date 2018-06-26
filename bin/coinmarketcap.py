import requests
import json
from unidecode import unidecode

# Get list of CoinMarketCap cryptocurrency data.
CMC_Ticker_URL = "https://api.coinmarketcap.com/v2/ticker/"
CMC_Ticker_response = requests.get(CMC_Ticker_URL)
CMC_Ticker_json = CMC_Ticker_response.json()

timestamp = CMC_Ticker_json['metadata']['timestamp']

Cryptocurrencies = []

for key in CMC_Ticker_json['data']:
    id     = unidecode(key)
    name   = unidecode(CMC_Ticker_json['data'][key]['name'])
    symbol = unidecode(CMC_Ticker_json['data'][key]['symbol'])
    price  = CMC_Ticker_json['data'][key]['quotes']['USD']['price']
    
    print("'%s','%s','%s','%s','%f'" % (id, timestamp, name, symbol, price))

