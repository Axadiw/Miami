from datetime import datetime
from math import ceil
from typing import List, Type

from ccxt.pro import bybit
from harvesting.data_harvesters.consts import MAX_CANDLES_HISTORY_TO_FETCH
from harvesting.data_harvesters.data_to_fetch import DataToFetch
from harvesting.data_harvesters.exchange_connectors.base_exchange_connector import BaseExchangeConnector
from shared.models.exchange import Exchange
from shared.models.symbol import Symbol


class BybitConnectorCCXT(BaseExchangeConnector):

    def __init__(self):
        self.connector_pro = bybit()

    async def load_markets(self):
        await self.connector_pro.load_markets(reload=True)
        
    async def fetch_tickers(self, exchange: Type[Exchange]) -> List[Symbol]:
        await self.connector_pro.load_markets(reload=True)
        response = await self.connector_pro.fetch_tickers()
        return list(map(lambda x: Symbol(name=x[1]['symbol'], exchange=exchange.id), response.items()))

    async def fetch_ohlcv(self, exchange: Type[Exchange], data: DataToFetch) -> \
            List[tuple]:
        response = await self.connector_pro.fetch_ohlcv(data.symbol.name, data.timeframe.name,
                                                        int(data.start.timestamp() * 1000),
                                                        limit=MAX_CANDLES_HISTORY_TO_FETCH,
                                                        params={"paginate": True,
                                                                "paginationCalls": int(
                                                                    ceil(MAX_CANDLES_HISTORY_TO_FETCH / 1000)),
                                                                'until': data.end.timestamp() * 1000,
                                                                'maxRetries': 10})

        max_permitted_date_ms = data.end.timestamp() * 1000.0
        timeframe_length_ms = data.timeframe.seconds * 1000.0

        return list(map(lambda x: (datetime.fromtimestamp(x[0] / 1000.0), exchange.id, data.symbol.id,
                                   data.timeframe.id, x[1], x[2], x[3], x[4], x[5]),
                        filter(lambda x: x[0] + timeframe_length_ms < max_permitted_date_ms, response)))

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
