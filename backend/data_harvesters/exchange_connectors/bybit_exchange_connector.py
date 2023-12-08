from datetime import datetime
from math import floor, ceil
from typing import List, Type

from ccxt.pro import bybit
from data_harvesters.consts import MAX_CANDLES_HISTORY_TO_FETCH
from data_harvesters.data_to_fetch import DataToFetch
from data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from models.exchange import Exchange
from models.ohlcv import OHLCV
from models.symbol import Symbol


class BybitConnectorCCXT(BaseExchangeConnector):

    def __init__(self):
        self.connector_pro = bybit()

    async def fetch_tickers(self, exchange: Type[Exchange]) -> List[Symbol]:
        response = await self.connector_pro.fetch_tickers()
        return list(map(lambda x: Symbol(name=x[1]['symbol'], exchange=exchange.id), response.items()))

    async def fetch_ohlcv(self, exchange: Type[Exchange], data: DataToFetch) -> \
            List[OHLCV]:
        response = await self.connector_pro.fetch_ohlcv(data.symbol.name, data.timeframe.name,
                                                        int(data.start.timestamp() * 1000),
                                                        limit=(MAX_CANDLES_HISTORY_TO_FETCH),
                                                        params={"paginate": True,
                                                                "paginationCalls": int(
                                                                    ceil(MAX_CANDLES_HISTORY_TO_FETCH / 1000)),
                                                                'until': data.end.timestamp() * 1000,
                                                                'maxRetries': 10})
        new_items = list(
            filter(lambda x: data.start <= x.timestamp <= data.end,
                   map(lambda x: OHLCV(timestamp=datetime.fromtimestamp(x[0] / 1000.0),
                                       exchange=exchange.id,
                                       symbol=data.symbol.id,
                                       timeframe=data.timeframe.id,
                                       open=x[1],
                                       high=x[2],
                                       low=x[3],
                                       close=x[4],
                                       volume=x[5]), response)))

        if len(new_items) == 0:
            pass

        # if data.is_last_to_fetch and len(new_items) > 0:
        #     new_items.pop()  # Remove last, not finished candle

        return new_items

    async def watch_ohlcv(self, symbols_and_time_frames: List[List[str]]):
        return await self.connector_pro.watch_ohlcv_for_symbols(symbols_and_time_frames)

    async def watch_tickers(self, symbols: List[str]):
        return await self.connector_pro.watch_tickers(symbols, {})

    async def fetch_start_dates(self):
        return {i[0]: datetime.fromtimestamp(int(i[1]) / 1000) for i in
                list(map(lambda x: [x['symbol'], x['info']['launchTime']],
                         await self.connector_pro.fetch_future_markets(
                             {'category': 'linear'})))}

    async def get_server_time(self) -> datetime:
        return datetime.fromtimestamp(await self.connector_pro.fetch_time() / 1000)

    async def close(self):
        await self.connector_pro.close()
