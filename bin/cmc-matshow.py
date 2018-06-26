import requests
import json
from unidecode import unidecode
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

# Get list of CoinMarketCap cryptocurrency data.
CMC_Ticker_URL      = "https://api.coinmarketcap.com/v2/ticker/"
CMC_Ticker_response = requests.get(CMC_Ticker_URL)
CMC_Ticker_json     = CMC_Ticker_response.json()
Cryptocurrencies    = []

# Parse json results.
timestamp              = CMC_Ticker_json['metadata']['timestamp']
num_cryptocurrencies   = CMC_Ticker_json['metadata']['num_cryptocurrencies']

for key in CMC_Ticker_json['data']:
    id                 = unidecode(key)
    name               = unidecode(CMC_Ticker_json['data'][key]['name'])
    symbol             = unidecode(CMC_Ticker_json['data'][key]['symbol'])
    website_slug       = unidecode(CMC_Ticker_json['data'][key]['website_slug'])
    rank               = CMC_Ticker_json['data'][key]['rank']
    circulating_supply = CMC_Ticker_json['data'][key]['circulating_supply']
    total_supply       = CMC_Ticker_json['data'][key]['total_supply']
    max_supply         = CMC_Ticker_json['data'][key]['max_supply']

    price              = CMC_Ticker_json['data'][key]['quotes']['USD']['price']
    volume_24h         = CMC_Ticker_json['data'][key]['quotes']['USD']['volume_24h']
    market_cap         = CMC_Ticker_json['data'][key]['quotes']['USD']['market_cap']
    percent_change_1h  = CMC_Ticker_json['data'][key]['quotes']['USD']['percent_change_1h']
    percent_change_24h = CMC_Ticker_json['data'][key]['quotes']['USD']['percent_change_24h']
    percent_change_7d  = CMC_Ticker_json['data'][key]['quotes']['USD']['percent_change_7d']

    last_updated       = CMC_Ticker_json['data'][key]['last_updated']

    # Create lists.
    ticker = [id, name, symbol, website_slug, rank, circulating_supply,
              total_supply, max_supply, price, volume_24h, market_cap,
              percent_change_1h, percent_change_24h, percent_change_7d,
              last_updated]

    Cryptocurrencies.append(ticker)

# Create DataFrame.
labels = ['id', 'name', 'symbol', 'website_slug', 'rank', 'circulating_supply', 
          'total_supply', 'max_supply', 'price', 'volume_24h', 'market_cap', 
          'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 
          'last_updated']

df_coinmarketcap = pd.DataFrame.from_records(Cryptocurrencies, columns=labels)
#print(df_coinmarketcap.to_string())
#scatter_matrix(df_coinmarketcap)
#plt.show()

plt.matshow(df_coinmarketcap.corr())
plt.xticks(range(len(df_coinmarketcap.columns)), df_coinmarketcap.columns)
plt.yticks(range(len(df_coinmarketcap.columns)), df_coinmarketcap.columns)
plt.colorbar()
plt.show()


