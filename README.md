# MSDS692
Data Science Practicum I

# Project Overview
The volatility of the cryptomarkets has been described as a wild rollercoaster ride. The objective of this project is to explore the relationship between sentiments and that volatility.

# Project Description
This is an on-going project I chose for my Data Science Practicum I. I think this project will provide me an interesting pathway to learn more about the tools and methods commonly used in data science. 

Twitter and CoinMarketCap data were analyzed for this project. The Twitter API and CoinMarketCap API were used to obtain the data.

# Process for projects/Major tools used
The tools I used for this project include, Python, SQLite and Perl.

# Data cleaning and preparation
* Removed from Unicode/UTF-8 characters from Twitter data.
* Stored data from Twitter and CoinCapMarket in SQLite database and flat files.
* Flat files were used for monitoring and recovery in the event data was not loaded into database. This happened.

# Exploratory Data Analysis (EDA)

## Price and Sentiment Visualizations
![image caption](/home/fwilliams/GitHub/MSDS692/images/ADA.png)   ![image caption](/home/fwilliams/GitHub/MSDS692/images/BCH.png)
![image caption](/home/fwilliams/GitHub/MSDS692/images/BTC.png)   ![image caption](/home/fwilliams/GitHub/MSDS692/images/EOS.png)
![image caption](/home/fwilliams/GitHub/MSDS692/images/ETH.png)   ![image caption](/home/fwilliams/GitHub/MSDS692/images/LTC.png)
![image caption](/home/fwilliams/GitHub/MSDS692/images/MIOTA.png) ![image caption](/home/fwilliams/GitHub/MSDS692/images/TRX.png)
![image caption](/home/fwilliams/GitHub/MSDS692/images/XLM.png)   ![image caption](/home/fwilliams/GitHub/MSDS692/images/XRP.png)

## CoinMarketCap Visualizations
![image caption](/home/fwilliams/GitHub/MSDS692/images/cmc_correlation.png)

### Correlation Matrix - CoinMarketCap

```python
# Create a list of features.
ticker = [rank, circulating_supply,
          total_supply, max_supply, price, volume_24h, market_cap,
          percent_change_1h, percent_change_24h, percent_change_7d]

# Create nested list of lists.
Cryptocurrencies.append(ticker)

# Create DataFrame using nested list.
labels = ['rank', 'circulating_sply',
          'total_sply', 'max_sply', 'price', 'vol_24h', 'market_cap',
          'pct_chg_1h', 'pct_chg_24h', 'pct_chg_7d']

df_coinmarketcap = pd.DataFrame.from_records(Cryptocurrencies, columns=labels)

# Create scatter_matrix and plt.matshow
axes      = scatter_matrix(df_coinmarketcap)
corr      = df_coinmarketcap.corr().values
corr_norm = (corr-corr.min())/(corr.max()-corr.min())

# Combine scatter_matrix and plt.matshow plots
for i, ax in enumerate(axes.flatten()):
    c = plt.cm.viridis(corr_norm.flatten()[i])
    ax.set_facecolor(c)

#plt.show() # print to screen
png_file = "cmc_correlation.png"
plt.savefig(png_file) # print to disk
```

# Analysis results
The relationship between sentiment and price is inconclusive. 

# Conclusion
* For this project, additional data and data prep will be required.
* Filtering unwanted Twitter data requires combining strong keyword searches with regular expressions and natural language processing. This results in a very resource intensive application.
* The data did not a reveal a strong correlation between sentiments and prices.
* It appears performing a correlation study on CoinMarketCap dataset, alone, may also yield useful investment data.
This project will be continued.

# References:
Twitter Application Management https://apps.twitter.com/
Public API V2 Documentation https://coinmarketcap.com/api/
