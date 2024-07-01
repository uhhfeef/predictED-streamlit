import sqlite3
import pandas as pd
## creating a connection
database = 'chinook.db'


conn = sqlite3.connect(database)

## importing tables 
tables = pd.read_sql("""SELECT name, type
                        FROM sqlite_master
                        WHERE type IN ("table", "view");""", conn)

print(tables)
album_primary_keys= pd.read_sql("""PRAGMA table_info(genres);""",conn)

print(album_primary_keys)

pd.read_sql("""
SELECT c.country AS Country, SUM(i.total) AS Sales
FROM customers c
JOIN invoices i ON c.CustomerId = i.CustomerId
GROUP BY Country
ORDER BY Sales DESC
LIMIT 5;

""", conn)

import matplotlib.pyplot as plt

# Define the SQL query
sql = """
SELECT g.Name AS Genre, COUNT(t.trackid) AS Tracks
FROM genres g
JOIN tracks t ON g.GenreId = t.GenreId
GROUP BY Genre
ORDER BY Tracks DESC;
"""

# Read the data into a dataframe
data = pd.read_sql(sql, conn)

# Plot the data as a bar chart
plt.bar(data.Genre, data.Tracks)
plt.title("Number of Tracks by Genre")
plt.xlabel("Genre")
plt.ylabel("Tracks")
plt.xticks(rotation=90)
plt.show()
