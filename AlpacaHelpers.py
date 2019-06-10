import alpaca_trade_api as tradeapi

# HELPFUL ALPACA FUNCTIONS written in Python by Micah Yong (June 10, 2019)
# Included in this script are helpful print statements and examples (commented out)

api = tradeapi.REST(
    key_id = 'PK9W7HAA9WD0N6AUWA9O', # REPLACE WITH YOUR OWN KEY ID
    secret_key = 'SDFNaiIy3KlLfjzCxTDdJ5xt/gk5gcKpj8ded8b1', # REPLACE WITH YOUR OWN SECRET KEY
    base_url = 'https://paper-api.alpaca.markets' # REPLACE WITH YOUR OWN BASE URL
)

# USER SPECIFIC FUNCTIONS AND SUBMISSIONS
def accountIsBlocked():
    """
    :return: True if account is blocked; false otherwise
    """
    # Get our account information.
    account = api.get_account()

    # Check if our account is restricted from trading.
    if account.trading_blocked:
        print('Account is currently restricted from trading.')
    else:
        print('Account is valid for trading.')
    return account.trading_blocked

print(accountIsBlocked())

def getBuyingPower():
    """
    :return: account buying power
    """
    # Get our account information.
    account = api.get_account()
    # Check how much money we can use to open new positions.
    print('${} is available as buying power.'.format(account.buying_power))
    return account.buying_power

print(getBuyingPower())


def buyOrder(ticker, quantity):
    """
    Standard order submission to buy in market
    :param ticker: company ticker as a string (i.e. 'AAPL')
    :param quantity: amount of shares as an integer (i.e. 5)
    """
    try:
        api.submit_order(
            symbol=ticker,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print("Success! You purchased {} shares of {}".format(quantity, ticker))
    except:
        print("Error purchasing {} shares of {}".format(quantity, ticker))

# buyOrder('AAPL', 4)


def sellOrder(ticker, quantity):
    """
    Standard order submission to buy in market
    :param ticker: company ticker as a string (i.e. 'AAPL')
    :param quantity: amount of shares as an integer (i.e. 5)
    """
    try:
        api.submit_order(
            symbol=ticker,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        print("Success! You sold {} shares of {}".format(quantity, ticker))
    except:
        print("Error selling {} shares of {}".format(quantity, ticker))

# sellOrder('AAPL', 1)


def buyOrderWithClientID(ticker, quantity, clientID):
    """
    Standard order submission to buy in market
    :param ticker: company ticker as a string (i.e. 'AAPL')
    :param quantity: amount of shares as an integer (i.e. 5)
    :param clientID: client id as a string (i.e. 'my_first_order')
    :return: order number under client ID
    """
    try:
        api.submit_order(
            symbol=ticker,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='gtc',
            client_order_id=clientID
        )
        print("Success! You purchased {} shares of {}".format(quantity, ticker))
        # Get our order using its Client Order ID.
        my_order = api.get_order_by_client_order_id(clientID)
        print('Got order #{}'.format(my_order.id))
        return my_order.id
    except:
        print("Error purchasing {} shares of {}".format(quantity, ticker))
        return ""

# print(buyOrderWithClientID('AAPL', 5, 'my_first_order'))


def getPosition(ticker):
    """
    :param ticker: company ticker as a string (i.e. 'AAPL')
    :return: if position exists, return list with the following
        [0] = quantity of stocks
        [1] = ticker
        [2] = percent change (coming soon)
        otherwise, return False
    """
    try:
        # Get our position in company.
        position = api.get_position(ticker)
        print("{} shares of {}".format(position.qty, position.symbol))
        return [position.qty, position.symbol]
    except:
        print("Error finding " + ticker + " position.")
        return False

# getPosition('AAPL')


def listAllPositions():
    """
    :return: prints and returns all positions in portfolio
    """
    # Get a list of all of our positions.
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))

    return portfolio

# listAllPositions()


def listLastNOrders(N):
    """
    :param N: limit for amount of orders returned
    :return: last N (or less) closed orders
    """
    # Get the last 100 of our closed orders
    closed_orders = api.list_orders(
        status='closed',
        limit=N
    )
    return closed_orders

# listLastNOrders(5)


def listLastNOrdersForCompany(N, ticker):
    """
    :param N: limit for amount of orders returned
    :param ticker: company ticker as a string (i.e. 'AAPL')
    :return: last N (or less) closed orders for particular stock
    """
    closed_orders = api.list_orders(
        status='closed',
        limit=N
    )
    # Get only the closed orders for a particular stock
    closed_comp_orders = [o for o in closed_orders if o.symbol == ticker]
    print(closed_comp_orders)
    return closed_comp_orders

# listLastNOrdersForCompany(5, 'AAPL')


# GENERAL FUNCTIONS AND QUERIES

def percentChange(ticker, timeUnit, numUnits):
    '''
    :param ticker: company ticker as a string (i.e. 'AAPL')
    :param timeUnit: unit of time as a string (i.e. 'day')
    :param numUnits: number of units of time as int (i.e. 5)
    :return: percent change specified time to present
    '''
    barset = api.get_barset(ticker, timeUnit, limit=numUnits)
    comp_bars = barset[ticker]

    # See how much company moved in a specific timeframe
    period_open = comp_bars[0].o
    period_close = comp_bars[-1].c
    percent_change = round((period_close - period_open) / period_open, 4)
    print(ticker + " moved " + str(percent_change) + "% over the last " + str(numUnits) + " " + timeUnit + "s.")
    return percent_change

# percentChange('MSFT', 'day', 5)

def getNASDAQ():
    '''
    :return: JSON for NASDAQ assets
    '''
    active_assets = api.list_assets(status='active')

    # Fileter assets to the ones only on NASDAQ
    nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
    for asset in nasdaq_assets:
        print(asset)
    return nasdaq_assets

def marketIsOpenNow():
    '''
    :return: true if market is open; false otherwise
    '''
    # Check if the market is open now.
    clock = api.get_clock()
    print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
    return clock.is_open

# marketOpen = marketIsOpenNow()
# print(marketOpen)

def marketTimes(t):
    '''
    :param t: date represented as string (i.e. '2019-06-10')
    :return: list with the following
        [0] = market open time
        [1] = market close time
    '''
    # Check when the market was open on date, t
    date = t
    calendar = api.get_calendar(start=date, end=date)[0]
    print('The market opened at {} and closed at {} on {}.'.format(
        calendar.open,
        calendar.close,
        date
    ))
    return [calendar.open, calendar.close]

# todayMarketTimes = marketTimes('2019-06-10')
# print(todayMarketTimes)

def isTradable(ticker):
    '''
    :param ticker: company ticker as a string (i.e. 'AAPL')
    :return: true if company is tradable; false otherwise
    '''
    asset = ticker
    try:
        comp_asset = api.get_asset(asset)
        if comp_asset.tradable:
            print("We can trade " + str(asset))
            return True
        else:
            print("We cannot trade " + str(asset))
            return False
    except:
        print("Error finding " + str(asset))
        return False

# print(isTradable('AAPL'))
# print(isTradable('gbdfv'))



