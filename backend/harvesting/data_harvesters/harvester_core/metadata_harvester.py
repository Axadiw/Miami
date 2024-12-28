import asyncio
import logging
from queue import Queue
from typing import Type, Callable

from sqlalchemy import select, delete
from sqlalchemy.dialects import postgresql

from harvesting.data_harvesters.consts import GLOBAL_QUEUE_START_COMMAND, GLOBAL_QUEUE_REFRESH_COMMAND
from harvesting.data_harvesters.database import get_session
from shared.models.exchange import Exchange
from shared.models.funding import Funding
from shared.models.last_fetched_date import LastFetchedDate
from shared.models.ohlcv import OHLCV
from shared.models.open_interests import OpenInterest
from shared.models.symbol import Symbol


class MetadataHarvester:
    exchange: Type[Exchange]

    def __init__(self, exchange_name: str, client_generator: Callable, historical_queue: Queue, realtime_queue: Queue):
        logging.info('[Metadata Harvester] Initializing ')

        self.exchange_name = exchange_name
        self.exchange_connector_generator = client_generator
        self.historical_queue = historical_queue
        self.realtime_queue = realtime_queue

    async def create_exchange_entry(self) -> Type[Exchange]:
        async with get_session(app_name='create_exchange_entry_metadata') as db_session:
            existing_entry = (await db_session.execute(select(Exchange).filter_by(name=self.exchange_name))).scalar()

            if existing_entry is not None:
                return existing_entry
            else:
                new_entry = Exchange(name=self.exchange_name)
                db_session.add(new_entry)
                await db_session.commit()
                return (await db_session.execute(select(Exchange).filter_by(name=self.exchange_name))).scalar()

    async def update_list_of_symbols(self) -> list[Type[Symbol]]:
        exchange_connector = self.exchange_connector_generator()
        logging.debug(f'[Metadata Harvester] Starting updating list of symbols')
        async with get_session(app_name='update_list_of_symbols_metadata') as db_session:
            while True:  # should finish after first round because of return at the end
                try:
                    existing_symbols = list(
                        (await db_session.execute(select(Symbol).filter_by(exchange=self.exchange.id))).scalars())
                    fetched_symbols = await exchange_connector.fetch_tickers(self.exchange)
                    fetched_symbols_names = list(filter(lambda x: ':' in x, map(lambda x: x.name,
                                                                                # TODO: extract this to a separate block
                                                                                fetched_symbols)))  # : magic for filtering out weird symbol names like EIGENUSDT (without /USDT:USDT at the end)
                    existing_symbols_names = list(map(lambda x: x.name, existing_symbols))
                    for symbol in existing_symbols:
                        if symbol.name not in fetched_symbols_names:
                            await (db_session.execute(delete(OHLCV).where(OHLCV.symbol == symbol.id)))
                            await (db_session.execute(delete(Funding).where(Funding.symbol == symbol.id)))
                            await (db_session.execute(delete(OpenInterest).where(OpenInterest.symbol == symbol.id)))
                            await (
                                db_session.execute(delete(LastFetchedDate).where(LastFetchedDate.symbol == symbol.id)))
                            await db_session.delete(symbol)

                    new_symbols_to_add = []
                    for symbol in fetched_symbols:
                        if symbol.name not in existing_symbols_names and ':' in symbol.name:  # : magic for filtering out weird symbol names like EIGENUSDT (without /USDT:USDT at the end)
                            new_symbols_to_add.append(symbol)
                    db_session.add_all(new_symbols_to_add)
                    await db_session.commit()

                    new_symbols_count = len(new_symbols_to_add)

                    logging.debug(f'[Metadata Harvester] Updated list of symbols ({new_symbols_count} new added)')
                    await exchange_connector.close()
                    return list(
                        (await db_session.execute(select(Symbol).filter_by(exchange=self.exchange.id))).scalars())
                except Exception as e:
                    logging.error(f'[Metadata Harvester] Fetch list of symbols error {e}')
                    await asyncio.sleep(30)

    async def start(self):
        self.exchange = await self.create_exchange_entry()
        await self.update_list_of_symbols()
        self.historical_queue.put(GLOBAL_QUEUE_START_COMMAND)
        self.realtime_queue.put(GLOBAL_QUEUE_START_COMMAND)
        while True:
            await self.update_list_of_symbols()
            self.historical_queue.put(GLOBAL_QUEUE_REFRESH_COMMAND)
            self.realtime_queue.put(GLOBAL_QUEUE_REFRESH_COMMAND)
            await asyncio.sleep(30 * 60)
