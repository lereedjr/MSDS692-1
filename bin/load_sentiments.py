import csv, sqlite3, sys

# Quick and dirty command line processing (not recommended)
csv_file = sys.argv[1]
db_file  = sys.argv[2]

# Create Connection object that represents the database.
conn = sqlite3.connect(db_file)

# Create cursor object.
c = conn.cursor()

# Create function to create table.
def create_table():
    try:
        # Create table with column name and datatypes.
        c.execute("CREATE TABLE IF NOT EXISTS sentiments(time_ms INTEGER, tweet TEXT, sentiment REAL)") # column names and datatypes

        # Create indexes (optional; for performance).
        c.execute("CREATE INDEX fast_time_ms ON sentiments(time_ms)")
        c.execute("CREATE INDEX fast_tweet ON sentiments(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiments(sentiment)")

        # Commit changes
        conn.commit()

    except Exception as e:
        print(str(e))

# Create table
create_table()

# Import CSV file into csv.DictReader.
with open(csv_file, 'rb') as csvfile:

  # csv.DictReader uses first line in file for column headings by default
  dr = csv.DictReader(csvfile) # comma is default delimiter

  to_db = [ ( i['time_ms'], i['tweet'], i['sentiment'] ) for i in dr ] 

# Insert csv.DictReader data into table.
c.executemany("INSERT INTO sentiments (time_ms, tweet, sentiment) VALUES (?, ?, ?)", to_db)

# Commit changes and close connection/session.
conn.commit()
conn.close()


