import string
from datetime import datetime
from time import sleep
from typing import Type

from ccxt import bybit
from sqlalchemy import desc, create_engine
from sqlalchemy.orm import sessionmaker

from consts_secrets import db_username, db_password, db_name
from models.exchanges import Exchanges
from models.ohlcv import OHLCV
from models.symbols import Symbols

EXCHANGE_NAME = 'bybit'
MAX_TIME_BETWEEN_SYMBOLS_FETCH = 3600
MAX_TIME_BETWEEN_ALL_OHLCV_FETCH = 60


class BybitHarvester:

    @staticmethod
    def get_session():
        return sessionmaker(create_engine(url=f'postgresql://{db_username}:{db_password}@db/{db_name}'))()

    def __init__(self, client: bybit):
        self.client = client
        self.db_session = self.get_session()
        self.time_of_last_symbols_update = datetime.fromtimestamp(0)
        self.time_of_last_all_ohlcv_update = datetime.fromtimestamp(0)
        self.exchange = self.create_exchange_entry()

    def create_exchange_entry(self):
        existing_entry = self.db_session.query(Exchanges).filter_by(name=EXCHANGE_NAME).first()

        if existing_entry is not None:
            return existing_entry
        else:
            new_entry = Exchanges(name=EXCHANGE_NAME)
            self.db_session.add(new_entry)
            self.db_session.commit()
            return self.db_session.query(Exchanges).filter_by(name=EXCHANGE_NAME).first()

    def update_list_of_symbols(self):
        if (datetime.now() - self.time_of_last_symbols_update).total_seconds() < MAX_TIME_BETWEEN_SYMBOLS_FETCH:
            return

        existing_symbols = list(map(lambda x: x.name, self.db_session.query(Symbols).all()))

        response = self.client.fetch_tickers()
        fetched_symbols = list(map(lambda x: x[1]['symbol'], response.items()))
        new_symbols_to_add = []
        for symbol in fetched_symbols:
            if symbol not in existing_symbols:
                new_symbols_to_add.append(symbol)

        new_symbols_to_add_objects = list(map(lambda x: Symbols(name=x), new_symbols_to_add))
        self.db_session.bulk_save_objects(new_symbols_to_add_objects)
        self.db_session.commit()

        self.time_of_last_symbols_update = datetime.now()
        print(f'Updated list of symbols ({len(new_symbols_to_add)} new added)')

    def update_all_ohlcv(self):
        if (datetime.now() - self.time_of_last_all_ohlcv_update).total_seconds() < MAX_TIME_BETWEEN_ALL_OHLCV_FETCH:
            return

        existing_symbols = self.db_session.query(Symbols).all()
        for index, symbol in enumerate(existing_symbols):
            self.update_ohlcv(symbol)
            print(f'Finished updating OHLCV history for {symbol.name} ({index + 1} / {len(existing_symbols)})')

        self.time_of_last_all_ohlcv_update = datetime.now()

    def update_ohlcv(self, symbol: Type[Symbols]):
        since = int(datetime.timestamp(self.get_newest_ohlcv_timestamp(symbol.id)))
        response = self.client.fetch_ohlcv(symbol.name, timeframe='1m', since=since, params={"paginate": True})
        new_items = list(
            map(lambda x: OHLCV(timestamp=datetime.fromtimestamp(x[0] / 1000.0),
                                exchange=self.exchange.id,
                                symbol=symbol.id,
                                open=x[1],
                                high=x[2],
                                low=x[3],
                                close=x[4],
                                volume=x[5]), response))

        self.db_session.bulk_save_objects(new_items)
        self.db_session.commit()
        pass

    def get_newest_ohlcv_timestamp(self, symbol_id: int):
        last_item = self.db_session.query(OHLCV).filter_by(exchange=self.exchange.id, symbol=symbol_id) \
            .order_by(desc(OHLCV.timestamp)) \
            .limit(1).first()

        if last_item is None:
            return datetime.fromtimestamp(0)
        else:
            return last_item.timestamp

    def start_loop(self):
        while True:
            self.update_list_of_symbols()
            self.update_all_ohlcv()
            sleep(1)
