import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import os
import pandas as pd
import pandas_datareader.data as web
import sys

style.use('ggplot')

### tickers list ###



stocks = ['AAPL', 'GOOGL', 'YHOO', 'AXP', 'XOM', 'KO', 'NOK', 'MS', 'IBM', 'FDX']


###   Historical Price   ###

def get_data_from_yahoo():
    if not os.path.exists('stock_sp'):
        os.makedirs('stock_sp')

    start = dt.datetime(2005, 1, 1)
    end = dt.datetime(2015, 12, 31)

    for ticker in stocks:
        print(ticker)
        try:
            if not os.path.exists('stock_sp/{}.csv'.format(ticker)):
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv('stock_sp/{}.csv'.format(ticker))
            else:
                print('Already have {}'.format(ticker))
        except Exception:
            pass


get_data_from_yahoo()


###  compile data ###


def compile_data():
    main_df = pd.DataFrame()

    for count, ticker in enumerate(stocks):
        print(count)
        try:
            df = pd.read_csv('stock_sp/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)

            df.rename(columns={'High': ticker}, inplace=True)
            df.drop(['Open', 'Adj Close', 'Low', 'Close', 'Volume'], 1, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')

        except Exception:
            pass

    print(main_df.head())
    main_df.to_csv('spstocks_joined_high.csv')


compile_data()


###   visualisation   ###
##This function is to plot the data frame
def visualize_data():
    df = pd.read_csv('spstocks_joined_high.csv', index_col='Date')
    df[stocks].plot()
    plt.show()


visualize_data()


###   Return on investment   ###
## THE DATE MUST BE OF THIS FORMAT : YYYY-MM-DD !!!

def ROI(amount, stock_name, volume, start_date, end_date):
    # parsing dates
    main_df = pd.read_csv('spstocks_joined_high.csv', index_col='Date', parse_dates=True)

    # converting dates as datetime object
    try:
        start = dt.datetime.strptime(start_date, "%Y-%m-%d")
        end = dt.datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print('Error: Date format must be YYYY-MM-DD !')

    # checking that end is greater than start
    if start > end:
        print("Error: Start date is greater than end date")
        sys.exit()

    # if budget is lower than volume times price then exit
    if amount < volume * main_df.loc[start, stock_name]:
        print("Error: You don't have enough money")
        sys.exit()

    # taking the closest business day before. if saturday or sunday then take friday.
    if start.weekday() == 5:
        print('Start date not a business day')
        start += dt.timedelta(days=-1)
    elif start.weekday() == 6:
        print('Start date not a business day')
        start += dt.timedelta(days=-2)

    if end.weekday() == 5:
        print('End date not a business day')
        end += dt.timedelta(days=-1)
    elif end.weekday() == 6:
        print('End date not a business day')
        end += dt.timedelta(days=-2)

    money_invested = volume * main_df.loc[start, stock_name]

    returns = (main_df.loc[end, stock_name] - main_df.loc[start, stock_name]) / main_df.loc[start, stock_name]

    print (
    'Your return on investment is ', returns * 100, '%', '. Your balance is now : ', amount - money_invested, '€')


# Example
ROI(amount=1000, stock_name='AAPL', volume=15, start_date='2005-01-12', end_date='2005-01-19')

