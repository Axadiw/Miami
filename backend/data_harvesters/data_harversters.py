import asyncio
import logging
from multiprocessing import Process
from time import sleep

from data_harvesters.bybit_harvester.bybit_harvester import BybitHarvester
from data_harvesters.exchange_connectors.bybit_exchange_connector import BybitConnectorCCXT


def bybit_connector_generator():
    return BybitConnectorCCXT()


async def harvest_bybit():
    while True:
        try:
            logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
            harvester = BybitHarvester(client_generator=bybit_connector_generator)
            await harvester.configure()
            await harvester.start_loop()
        except Exception as e:
            logging.error(f'Unhandled data harvesters error {e}')
            sleep(30)


def wrapper():
    asyncio.run(harvest_bybit())


def launch_data_harvesters():
    p = Process(target=wrapper)
    p.start()


if __name__ == "__main__":
    asyncio.run(harvest_bybit())
