import sqlite3
import seaborn
import datetime
import numpy
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rc('xtick', labelsize=12)
matplotlib.rc('ytick', labelsize=12)

conn = sqlite3.connect('net_data.db')
data = conn.execute("SELECT * FROM entries;").fetchall()

entry_datetime = [datetime.datetime.strptime(d[1],'%Y-%m-%d %H:%M:%S.%f') for d in data]
download = [entry[3] for entry in data]

plt.figure(figsize=(19.20, 12.80))
plt.title('Download Speed', fontsize=22, fontweight='bold')
plt.xlabel('DateTime', fontsize=18)
plt.ylabel('Speed (Mbp/s)', fontsize=18)
plt.plot(entry_datetime, download)

plt.savefig('.\\graphs\\test.jpg', format='jpg')
