netcheck
===

Uses the speedtest-cli to check your download/upload speed and stores it in a database.
The visualize script plots the data in graphs like these:
![Download History](graphs/demo/download_2016-03-03.png)
![Upload History](graphs/demo/upload_2016-03-03.png)
![Ping History](graphs/demo/ping_2016-03-03.png)

## Getting Started
The only external package require to get netcheck.py working is speedtest-cli, the other packages are all
used by the visualize.py file to plot the data. Before anythin else, you will need to run
```python netcheck.py --create-db``` to create the database. Sqlite3.exe will need to be in your path
for this to work.

To generate a continuous log you need to add the netcheck.py script, either to cron on linux, or
task scheduler in windows.
The example images were generated using a task scheduled to run every 5 minutes.

Use netcheck.py --help and visualize.py --help to see a list of available commands.

### Known Issues
speedtest-cli.exe generates a popup window when run from a *.pyw file.