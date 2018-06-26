import requests
import json
from unidecode import unidecode
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt

#import seaborn.apionly as sns
#import pandas as pd
#import matplotlib.pyplot as plt

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
    #ticker = [id, name, symbol, website_slug, rank, circulating_supply,
    #          total_supply, max_supply, price, volume_24h, market_cap,
    #          percent_change_1h, percent_change_24h, percent_change_7d,
    #          last_updated]

    ticker = [rank, circulating_supply,
              total_supply, max_supply, price, volume_24h, market_cap,
              percent_change_1h, percent_change_24h, percent_change_7d]

    Cryptocurrencies.append(ticker)

# Create DataFrame.
#labels = ['id', 'name', 'symbol', 'website_slug', 'rank', 'circulating_supply',
#          'total_supply', 'max_supply', 'price', 'volume_24h', 'market_cap',
#          'percent_change_1h', 'percent_change_24h', 'percent_change_7d',
#          'last_updated']

labels = ['rank', 'circulating_sply',
          'total_sply', 'max_sply', 'price', 'vol_24h', 'market_cap',
          'pct_chg_1h', 'pct_chg_24h', 'pct_chg_7d']

df_coinmarketcap = pd.DataFrame.from_records(Cryptocurrencies, columns=labels)



# Combine scatter_matrix and plt.matshow
# taking the iris from seaborn (should be same as scikit)
#df = sns.load_dataset("iris")

axes      = scatter_matrix(df_coinmarketcap)
corr      = df_coinmarketcap.corr().values
corr_norm = (corr-corr.min())/(corr.max()-corr.min())

for i, ax in enumerate(axes.flatten()):
    c = plt.cm.viridis(corr_norm.flatten()[i])
    ax.set_facecolor(c)

#plt.show() # print to screen
png_file = "cmc_correlation.png"
plt.savefig(png_file) # print to disk

