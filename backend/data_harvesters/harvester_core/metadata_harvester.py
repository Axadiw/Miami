import asyncio
import logging
from queue import Queue
from typing import Type, Callable

from sqlalchemy import select

from data_harvesters.consts import GLOBAL_QUEUE_START_COMMAND, GLOBAL_QUEUE_REFRESH_COMMAND
from data_harvesters.database import get_session
from models.exchange import Exchange
from models.symbol import Symbol


class MetadataHarvester:
    exchange: Type[Exchange]

    def __init__(self, exchange_name: str, client_generator: Callable, historical_queue: Queue, realtime_queue: Queue):
        logging.info('[Metadata Harvester] Initializing ')

        self.exchange_name = exchange_name
        self.exchange_connector_generator = client_generator
        self.historical_queue = historical_queue
        self.realtime_queue = realtime_queue

    async def create_exchange_entry(self) -> Type[Exchange]:
        async with get_session() as db_session:
            existing_entry = (await db_session.execute(select(Exchange).filter_by(name=self.exchange_name))).scalar()

            if existing_entry is not None:
                return existing_entry
            else:
                new_entry = Exchange(name=self.exchange_name)
                await db_session.add(new_entry)
                await db_session.commit()
                return (await db_session.execute(select(Exchange).filter_by(name=self.exchange_name))).scalar()

    async def update_list_of_symbols(self) -> list[Type[Symbol]]:
        exchange_connector = self.exchange_connector_generator()
        logging.info(f'[Metadata Harvester] Starting updating list of symbols')
        async with get_session() as db_session:
            while True:  # should finish after first round because of return at the end
                try:
                    existing_symbols = list(
                        (await db_session.execute(select(Symbol).filter_by(exchange=self.exchange.id))).scalars())
                    fetched_symbols = await exchange_connector.fetch_tickers(self.exchange)
                    fetched_symbols_names = list(map(lambda x: x.name, fetched_symbols))
                    existing_symbols_names = list(map(lambda x: x.name, existing_symbols))

                    for symbol in existing_symbols:
                        if symbol.name not in fetched_symbols_names:
                            await db_session.delete(symbol)

                    new_symbols_to_add = []
                    for symbol in fetched_symbols:
                        if symbol.name not in existing_symbols_names:
                            new_symbols_to_add.append(symbol)
                    db_session.add_all(new_symbols_to_add)
                    await db_session.commit()

                    new_symbols_count = len(new_symbols_to_add)

                    logging.info(f'[Metadata Harvester] Updated list of symbols ({new_symbols_count} new added)')
                    await exchange_connector.close()
                    return list(
                        (await db_session.execute(select(Symbol).filter_by(exchange=self.exchange.id))).scalars())
                except Exception as e:
                    logging.error(f'[Metadata Harvester] Fetch list of symbols error {e}')
                    await asyncio.sleep(1)

    async def start(self):
        self.exchange = await self.create_exchange_entry()
        await self.update_list_of_symbols()
        self.historical_queue.put(GLOBAL_QUEUE_START_COMMAND)
        self.realtime_queue.put(GLOBAL_QUEUE_START_COMMAND)
        while True:
            await self.update_list_of_symbols()
            self.historical_queue.put(GLOBAL_QUEUE_REFRESH_COMMAND)
            self.realtime_queue.put(GLOBAL_QUEUE_REFRESH_COMMAND)
            await asyncio.sleep(5 * 60)
