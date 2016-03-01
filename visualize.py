import sqlite3
import seaborn
import datetime
import numpy
import matplotlib.pyplot as plt

conn = sqlite3.connect('example_net_data.db')
data = conn.execute("SELECT * FROM entries;").fetchall()

entry_datetime = [datetime.datetime.strptime(d[1],'%Y-%m-%d %H:%M:%S.%f') for d in data]
download = [entry[3] for entry in data]

plt.plot(entry_datetime, download)

plt.show()
