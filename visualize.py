""" Functionality:
    visualize download speed, upload speed and ping for all entries or any given date.

    Using string formatting instead of the safe sqlite3 ? syntax to build the query strings as the safe
    string replacement wouldn't work in this case "SELECT ? FROM entries".
"""
import argparse
import datetime
import matplotlib
import os
import seaborn
import sqlite3


def plot(data_x, data_y, column, date=None):
    title = '{} History'.format(column.capitalize())

    if column == 'ping':
        label_y = 'Ping (ms)'
    else:
        label_y = 'Speed (Mbp/s)'

    if date:
        label_x = date
        filename = '{}_{}'.format(column, date)
    else:
        label_x = 'Time'
        start_date = data_x[0].date()
        end_date = data_x[-1].date()
        filename = '{}-range_{}-{}'.format(column, start_date, end_date)

    # Style the plot
    matplotlib.rc('xtick', labelsize=12)
    matplotlib.rc('ytick', labelsize=12)
    plt = matplotlib.pyplot
    plt.figure(figsize=(19.20, 12.80))
    plt.title(title, fontsize=22, fontweight='bold')
    plt.xlabel(label_x, fontsize=18)
    plt.ylabel(label_y, fontsize=18)

    # Make the plot
    plt.plot(data_x, data_y)

    # Output the plot
    plt.savefig(os.path.join('./graphs', '{}.png'.format(filename)), format='png')


def query_column(db, sql_query):
    entries = db.execute(sql_query).fetchall()

    entry_datetime = [datetime.datetime.strptime(entry[0],'%Y-%m-%d %H:%M:%S.%f') for entry in entries]
    entry_column = [entry[1] for entry in entries]

    return entry_datetime, entry_column


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize the stored network data created by netcheck.pyw')

    parser.add_argument('--columns', nargs='+', action='store',
                        help='Plot the data for the given columns. The choices are: download, upload, and ping.')
    parser.add_argument('--date', action='store',
                        help='Plot the data from a specific date.')
    parser.add_argument('--today', action='store_true',
                        help='Plot the data for the current date.')
    parser.add_argument('--yesterday', action='store_true',
                        help='Plot the data for yesterday.')
    parser.add_argument('--cleanup', action='store_true',
                        help='Delete all saved plots in the ./graphs folder before creating new ones.')
    parser.add_argument('--range', nargs=2, action='store',
                        help='Plot all of the data that falls within the given range. Usage: --range date1 date2')

    args = parser.parse_args()

    # Check for multiple arguments that contradict.
    if (args.date and args.today) or (args.date and args.yesterday) or (args.date and args.range) \
            or (args.today and args.yesterday) or (args.today and args.range) or (args.yesterday and args.range):
        raise ValueError('Only one date argument is allowed.')

    # Clean out saved graphs if --cleanup is passed.
    if args.cleanup:
        graphs_dir = './graphs'
        for file in os.listdir(graphs_dir):
            file_path = os.path.join(graphs_dir, file)
            try:
                if os.path.isfile(file_path) and file != '.gitignore':
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    # Establish the database connection.
    db = sqlite3.connect('net_data.db')

    # Make the requested plots. Using a try except block to make sure the database connection is closed.
    try:
        if not args.columns:
            args.columns = ['download', 'upload', 'ping']

        for column in args.columns:
            # Keep track of variables to use as a labels on the plots
            date = None
            range_start = None
            range_end = None

            # Build the queries
            if args.date:
                query = 'SELECT datetime, {} FROM entries WHERE datetime LIKE "{}%";'.format(column, args.date)
            elif args.today:
                date = datetime.datetime.now().date()
                query = 'SELECT datetime, {} FROM entries WHERE datetime LIKE "{}%";'.format(column, date)
            elif args.yesterday:
                date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
                query = 'SELECT datetime, {} FROM entries WHERE datetime LIKE "{}%";'.format(column, date)
            elif args.range:
                range_start = args.range[0]
                range_end = args.range[1]
                query = 'SELECT datetime, {} FROM entries WHERE datetime BETWEEN "{} 00:00:00.000" AND "{} 23:59:59.000";'.format(column, range_start, range_end)
            else:
                query = 'SELECT datetime, {} FROM entries;'.format(column)

            # Execute the query
            data_x, data_y = query_column(db, query)

            # Make the plot
            plot(data_x, data_y, column, date)
    except:
        raise
    finally:
        db.close()
