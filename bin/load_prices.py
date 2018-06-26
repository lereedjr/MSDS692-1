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
        c.execute("CREATE TABLE IF NOT EXISTS prices(id INTEGER, timestamp INTEGER, name TEXT, symbol TEXT, price REAL)") # column names and datatypes

        # Create indexes (optional; for performance).
        c.execute("CREATE INDEX fast_id ON prices(id)")
        c.execute("CREATE INDEX fast_timestamp ON prices(timestamp)")
        c.execute("CREATE INDEX fast_name ON prices(name)")
        c.execute("CREATE INDEX fast_symbol ON prices(symbol)")
        c.execute("CREATE INDEX fast_price ON prices(price)")

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

  to_db = [ ( i['id'], i['timestamp'], i['name'], i['symbol'], i['price'] ) for i in dr ] 

# Insert csv.DictReader data into table.
c.executemany("INSERT INTO prices (id, timestamp, name, symbol, price) VALUES (?, ?, ?, ?, ?)", to_db)

# Commit changes and close connection/session.
conn.commit()
conn.close()


