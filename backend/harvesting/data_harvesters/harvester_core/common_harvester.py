import logging
from typing import Type

from sqlalchemy import select

from harvesting.data_harvesters.database import get_session
from shared.models.exchange import Exchange
from shared.models.symbol import Symbol
from shared.models.timeframe import Timeframe


async def fetch_exchange_entry(exchange_name) -> Type[Exchange]:
    async with get_session(app_name='fetch_exchange_entry') as db_session:
        existing_entry = (await db_session.execute(select(Exchange).filter_by(name=exchange_name))).scalar()

        if existing_entry is not None:
            return existing_entry
        else:
            raise Exception(f'No {exchange_name} exchange object found')


async def fetch_list_of_symbols(exchange: Type[Exchange]) -> list[Type[Symbol]]:
    logging.info(f'[Historical Harvester] Starting updating list of symbols')
    async with get_session(app_name='fetch_list_of_symbols') as db_session:
        return list(
            (await db_session.execute(
                select(Symbol).filter_by(exchange=exchange.id)
            )).scalars())


async def create_all_timeframes():
    async with get_session(app_name='create_all_timeframes') as db_session:
        supported_timeframes = [
            {'name': '1m', 'seconds': 60},
            {'name': '5m', 'seconds': 60 * 5},
            {'name': '15m', 'seconds': 60 * 15},
            {'name': '30m', 'seconds': 60 * 30},
            {'name': '1h', 'seconds': 60 * 60},
            {'name': '4h', 'seconds': 60 * 60 * 4},
            {'name': '1d', 'seconds': 60 * 60 * 24},
            {'name': '1w', 'seconds': 60 * 60 * 24 * 7},
        ]

        new_timeframes = []
        for timeframe in supported_timeframes:
            existing_timeframe = (
                await db_session.execute(select(Timeframe).filter_by(name=timeframe['name']))).scalar()
            if existing_timeframe is None:
                new_timeframes.append(Timeframe(name=timeframe['name'], seconds=timeframe['seconds']))
        if len(new_timeframes) > 0:
            db_session.add_all(new_timeframes)
            await db_session.commit()
        logging.info(
            f'Updated list of timeframes ({len(new_timeframes)} new timeframes added)')


async def get_subset_of_timeframes(timeframe_names) -> list[Type[Timeframe]]:
    async with get_session(app_name='get_subset_of_timeframes') as db_session:
        all_timeframes = list((await db_session.execute(select(Timeframe))).scalars())
        return list(
            filter(lambda timeframe: timeframe.name in timeframe_names, all_timeframes))
