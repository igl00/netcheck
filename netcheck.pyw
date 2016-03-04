import argparse
import datetime
import re
import sqlite3
import subprocess


def create_db():
    """ Create a new database using the sqlite3 command line argument.
        Sqlite3 must be added to the users PATH for this to work.
    """
    with open('schema.sql') as schema:
        subprocess.call('sqlite3 net_data.db', stdin=schema)


def speed_test():
    """ Run the speedtest-cli tool and enter the results into the database.
        Ping is in ms.
        Download is in Mbp/s.
        Upload is in Mbp/s.
        All fields zero out if they fail.
    """
    conn = sqlite3.connect('net_data.db')

    byte_output = subprocess.check_output(['speedtest-cli', '--simple'])
    output = byte_output.decode("utf-8")

    ping = re.search(r"(?:Ping: )([0-9]+.[0-9]+)(?: ms)", output)
    if not ping:
        ping = 0.000
    else:
        ping = ping.group(1)

    download = re.search(r'(?:Download: )([0-9]+.[0-9]+)(?: Mbit/s)', output)
    if not download:
        download = 0.00
    else:
        download = download.group(1)

    upload = re.search(r"(?:Upload: )([0-9]+.[0-9]+)(?: Mbit/s)", output)
    if not upload:
        upload = 0.00
    else:
        upload = upload.group(1)

    entry = (datetime.datetime.now(), ping, download, upload)

    conn.execute("INSERT INTO entries(datetime, ping, download, upload) VALUES (?, ?, ?, ?)", entry)
    conn.commit()

    conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Logs speed tests to a database.')

    parser.add_argument('--create-db', action='store_true',
                        help='Creates a new database. If one already exists, all tables will be wiped.')

    args = parser.parse_args()

    if args.create_db:
        create_db()
    else:
        speed_test()
