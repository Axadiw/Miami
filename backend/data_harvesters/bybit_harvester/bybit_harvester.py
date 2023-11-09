from time import sleep
from pybit.unified_trading import HTTP


class BybitHarvester:
    def __init__(self, session: HTTP):
        self.symbols = []
        self.session = session

    def update_list_of_symbols(self):
        response = self.session.get_tickers(category='linear')
        self.symbols = list(map(lambda x: x['symbol'], response['result']['list']))
        print('Updated list of symbols')
