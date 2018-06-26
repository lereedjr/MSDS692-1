from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
from textblob import TextBlob
from unidecode import unidecode
import time
import requests

# Get list of CoinMarketCap cryptocurrency names and symbols
CMC_Ticker_URL      = " https://api.coinmarketcap.com/v2/ticker/"
CMC_Ticker_response = requests.get(CMC_Ticker_URL)
CMC_Ticker_json     = CMC_Ticker_response.json()

Cryptocurrencies = []
for key in CMC_Ticker_json['data']:
    name   = unidecode(CMC_Ticker_json['data'][key]['name'])
    symbol = unidecode(CMC_Ticker_json['data'][key]['symbol'])
    Cryptocurrencies.append(name)
    Cryptocurrencies.append(symbol)

# Create Connection object that represents the database
#db = '/home/fwilliams/Projects/MSDS692/Practicum/data/twitter.db'
db = '/home/fwilliams/Projects/MSDS692/Practicum/data4/twitter.db'
conn = sqlite3.connect(db)

# Create cursor object
c = conn.cursor()

# Create function to create table
def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        # Create indexes (optional; for performance)
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_unix ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_unix ON sentiment(sentiment)")
        # Commit changes
        conn.commit()
    except Exception as e:
        print(str(e))
# Create table
create_table()

# Authentication information
consumer_key        = ""
consumer_secret     = ""
access_token        = ""
access_token_secret = ""

# Create a simple stream listener class
class MyListener(StreamListener):

    def on_data(self, data):
        try:
            data    = json.loads(data)
            tweet   = unidecode(data['text'])
            time_ms = data['timestamp_ms']

            analysis  = TextBlob(tweet)
            sentiment = analysis.sentiment.polarity
            print(time_ms, tweet, sentiment)

            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)", (time_ms, tweet, sentiment))
            conn.commit()

        except KeyError as e:
            print(str(e))

        return(True)

    def on_error(self, status):
        print(status)

# Main
while True:

    try:
        # Create the authentication object
        auth = OAuthHandler(consumer_key, consumer_secret)

        # Set access token and secret
        auth.set_access_token(access_token, access_token_secret)

        # Pass in authentication credentials to Twitter; this allows connection
        twitterStream = Stream(auth, MyListener())

        # Start streaming and filtering tweets
        #print(Cryptocurrencies)
        #twitterStream.filter(track=Cryptocurrencies)
        # The following crypto related terms seem to capture desired tweets better
        twitterStream.filter(track=['Altcoin', 'Airdrop', 'Blockchain', 'Crypto', 'dApp', 'ERC20', 'HODL','ICO', 'Masternode', 'Satoshi','Token'])

    except Exception as e:
        print(str(e))
        time.sleep(5)

