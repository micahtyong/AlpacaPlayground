import alpaca_trade_api as tradeapi
import AlpacaHelpers as alpaca

from datetime import datetime
import calendar

# ALPACA challenge written in Python by Micah Yong (June 10, 2019)

api = tradeapi.REST(
    key_id = 'PK9W7HAA9WD0N6AUWA9O', # REPLACE WITH YOUR OWN KEY ID
    secret_key = 'SDFNaiIy3KlLfjzCxTDdJ5xt/gk5gcKpj8ded8b1', # REPLACE WITH YOUR OWN SECRET KEY
    base_url = 'https://paper-api.alpaca.markets'
)

def isPrime(value):
    """
    method runs in O(N) time
    :param value: integer
    :return: true if value is prime; false otherwise
    """
    if value < 2: return False
    for i in range(2, value):
        if value % i == 0:
            return False
    return True

def findDay(date):
    born = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').weekday()
    return calendar.day_name[born]

def epochToDay(epoch):
    date = datetime.datetime.fromtimestamp(epoch).strftime('%c')
    return findDay(date)

startDate = '%2018-%01-%01 %00:%00:%00'
endDate = '%2019-%01-%01 %00:%00:%00'

S = api.get_barset('SPY', 'day', None, start=startDate, end=endDate, after=None, until=None)
spy_bars = S['SPY']

D = api.get_barset('DIA', 'day', None, start=startDate, end=endDate, after=None, until=None)
dia_bars = D['DIA']

length = len(spy_bars)

Xchallenge = -1

for i in range(0, length):
    S_close = int(spy_bars[i].c * (10 ** 2))
    D_close = int(dia_bars[i].c * (10 ** 2))
    day = spy_bars[i].t.dayofweek
    if isPrime(S_close) and isPrime(D_close) and day == 2:
        Xchallenge = i
        print(S_close, D_close)

print("X equals " + str(Xchallenge))
