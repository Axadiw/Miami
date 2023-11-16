import asyncio
import logging
from multiprocessing import Process

import ccxt

from data_harvesters.bybit_harvester.bybit_harvester import BybitHarvester
from data_harvesters.exchange_connectors.bybit_exchange_connector import BybitConnectorCCXT
from asyncio import get_event_loop


async def harvest_bybit():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    harvester = BybitHarvester(BybitConnectorCCXT())
    await harvester.start_loop()


def wrapper():
    asyncio.run(harvest_bybit())


def launch_data_harvesters():
    p = Process(target=wrapper)
    p.start()


if __name__ == "__main__":
    asyncio.run(harvest_bybit())
