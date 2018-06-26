import pandas as pd
from pandas.plotting import scatter_matrix
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import style
#style.use('fivethirtyeight')
style.use('ggplot')

#-------------------------------------------------------------------------------
# Open connections to database.
#-------------------------------------------------------------------------------
# Database
db = '/home/fwilliams/Projects/MSDS692/Practicum/reports/db/msds692.db'

# Create Connection object to connect to database.
conn = sqlite3.connect(db)

# Create Cursor object to executed SQL queries against database.
#cur = conn.cursor()

#-------------------------------------------------------------------------------
# For loop
#-------------------------------------------------------------------------------
# All - Very resource intensive
#cryptocurrencies_query = 'SELECT * FROM cryptocurrencies'
#df_cryptocurrencies = pd.read_sql(cryptocurrencies_query, conn)
#symbols = df_cryptocurrencies['symbol'].values.tolist()
#symbols = df_cryptocurrencies['symbol'].tolist()

# Top ten on Mon Jun 25 11:05:44 CDT 2018
symbols = [ "BTC", "ETH", "XRP", "BCH", "EOS", "LTC", "XLM", "ADA", "MIOTA", "TRX"]

# Needed later to store mean values.
col_names = ['symbol','m_price','m_sentiment']
df_means = pd.DataFrame(columns = col_names)

for query_symbol in symbols:
  #=====================================
  # Define queries.
  #=====================================
  # For prices table.
  #prices_query = 'SELECT * FROM prices WHERE symbol LIKE \'%' + query_symbol + '%\' AND timestamp BETWEEN 1529470800 AND 1529816400 ORDER BY timestamp'
  prices_query = 'SELECT * FROM prices WHERE symbol = \'' + query_symbol + '\' AND timestamp BETWEEN 1529470800 AND 1529816400 ORDER BY timestamp'
  
  # For sentiments table.
  sentiments_query = 'SELECT * FROM sentiments WHERE tweet LIKE \'%' + query_symbol + '%\' AND time_ms BETWEEN 1529470800000 AND 1529816400000 ORDER BY time_ms'

  #=====================================
  # Execute queries.
  #=====================================
  # For prices table.
  df_prices = pd.read_sql(prices_query, conn)

  if df_prices.empty:
    print(query_symbol + ": Skipping empty prices dataframe.")
    continue

  # For sentiments table.
  df_sentiments = pd.read_sql(sentiments_query, conn)

  if df_sentiments.empty:
    print(query_symbol + ": Skipping empty sentiments dataframe.")
    continue

  #=====================================
  # Plot query results.
  #=====================================
  # For prices table.
  df_prices['timestamp'] = pd.to_datetime(df_prices['timestamp'],unit='s')
  #df_prices.groupby('symbol').plot(x='timestamp', y='price', title=query_name)
  #plt.legend().remove()
  #plt.show()

  # For sentiments table.
  df_sentiments['time_ms'] = pd.to_datetime(df_sentiments['time_ms'],unit='ms')
  #df_sentiments.plot(x='time_ms', y='sentiment', title=query_name)
  #plt.legend().remove()
  #plt.show()

  #-------------------------------------------------------------------------------
  # Plot query results (using subplots).
  #-------------------------------------------------------------------------------
  # Have one subplot
  #fig, ax = plt.subplots()
  #df_prices[      df_prices['symbol'] == query_symbol].plot(x='timestamp', y='price',     ax=ax, label=query_symbol)
  #df_sentiment[ df_sentiment['tweet'] == query_symbol].plot(x='time_ms',   y='sentiment', ax=ax, label=query_symbol)

  fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

  #df_prices[df_prices['symbol'] == query_symbol].plot(x='timestamp', y='price', legend=False, ax=ax1)
  df_prices.plot(x='timestamp', y='price', legend=False, ax=ax1)
  prices_title = query_symbol + " Prices"
  ax1.set_title(prices_title)

  #df_sentiments[df_sentiments['tweet'] == query_symbol].plot(x='time_ms', y='sentiment', legend=False, ax=ax2)
  df_sentiments.plot(x='time_ms', y='sentiment', legend=False, ax=ax2)
  sentiment_title = query_symbol + " Sentiments"
  ax2.set_title(sentiment_title)

  plt.tight_layout()
  #plt.show() # print to screen
  chart_file = '/home/fwilliams/Projects/MSDS692/Practicum/reports/correlations/visualizations/' + query_symbol + '.png'
  plt.savefig(chart_file) # print to disk

  #-------------------------------------------------------------------------------
  # Correlation calculations
  #-------------------------------------------------------------------------------
  mean_price = df_prices["price"].mean()
  mean_sentiment = df_sentiments["sentiment"].mean()
  
  df_means.loc[len(df_means)] = [query_symbol, mean_price, mean_sentiment]
  df_means.info()
  print(df_means)

#df_means.corr()
#print(df_means.corr())
#pd.scatter_matrix(df_means, figsize=(6,6)) # deprecated
scatter_matrix(df_means, figsize=(6,6))
plt.show()

plt.matshow(df_means.corr())
plt.xticks(range(len(df_means.columns)), df_means.columns)
plt.yticks(range(len(df_means.columns)), df_means.columns)
plt.colorbar()
plt.show()

#-------------------------------------------------------------------------------
# Close connections to database.
#-------------------------------------------------------------------------------
# Close Cursor object.
#cur.close()

# Close Connection object.
conn.close()

