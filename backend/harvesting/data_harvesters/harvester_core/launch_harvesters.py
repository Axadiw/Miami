import asyncio
import logging
from queue import Queue
from threading import Thread
from time import sleep
from typing import Callable

from harvesting.data_harvesters.harvester_core.historical_harvester import HistoricalHarvester
from harvesting.data_harvesters.harvester_core.metadata_harvester import MetadataHarvester
from harvesting.data_harvesters.harvester_core.realtime_harverser import RealtimeHarvester


def launch_historical_harvester_wrapper(exchange_name: str, connector_generator: Callable,
                                        queue: Queue, ohlcv_timeframes: list[str]):
    asyncio.run(
        launch_historical_harvester(exchange_name=exchange_name, connector_generator=connector_generator, queue=queue,
                                    ohlcv_timeframes=ohlcv_timeframes))


def launch_realtime_harvester_wrapper(exchange_name: str, connector_generator: Callable,
                                      queue: Queue, ohlcv_timeframes: list[str]):
    asyncio.run(
        launch_realtime_harvester(exchange_name=exchange_name, connector_generator=connector_generator, queue=queue,
                                  ohlcv_timeframes=ohlcv_timeframes))


def launch_metadata_harvester_wrapper(exchange_name: str, connector_generator: Callable, historical_queue: Queue,
                                      realtime_queue: Queue):
    asyncio.run(
        launch_metadata_harvester(exchange_name=exchange_name, connector_generator=connector_generator,
                                  historical_queue=historical_queue, realtime_queue=realtime_queue))


async def launch_metadata_harvester(exchange_name: str, connector_generator: Callable, historical_queue: Queue,
                                    realtime_queue: Queue):
    while True:
        try:
            harvester = MetadataHarvester(exchange_name=exchange_name, client_generator=connector_generator,
                                          historical_queue=historical_queue, realtime_queue=realtime_queue)
            await harvester.start()
        except Exception as e:
            logging.error(f'Unhandled metadata harvester error {e}')
            sleep(30)


async def launch_historical_harvester(exchange_name: str, connector_generator: Callable, queue: Queue,
                                      ohlcv_timeframes: list[str]):
    while True:
        try:
            harvester = HistoricalHarvester(exchange_name=exchange_name, client_generator=connector_generator,
                                            queue=queue, ohlcv_timeframe_names=ohlcv_timeframes)
            await harvester.start()
        except Exception as e:
            logging.error(f'Unhandled historical harvester error {e}')
            sleep(30)


async def launch_realtime_harvester(exchange_name: str, connector_generator: Callable, queue: Queue,
                                    ohlcv_timeframes: list[str]):
    while True:
        try:
            harvester = RealtimeHarvester(exchange_name=exchange_name, client_generator=connector_generator,
                                          queue=queue, ohlcv_timeframe_names=ohlcv_timeframes)
            await harvester.start()
        except Exception as e:
            logging.error(f'Unhandled realtime harvester error {e}')
            sleep(30)


async def launch_all_harvesters_for_single_exchange(exchange_name: str, connector_generator: Callable,
                                                    ohlcv_timeframes: list[str]):
    historical_queue = Queue()
    realtime_queue = Queue()
    historical_thread = Thread(name=f'historical_{exchange_name}', target=launch_historical_harvester_wrapper,
                               args=(exchange_name, connector_generator, historical_queue, ohlcv_timeframes,))
    realtime_thread = Thread(name=f'realtime_{exchange_name}', target=launch_realtime_harvester_wrapper,
                             args=(exchange_name, connector_generator, realtime_queue, ohlcv_timeframes,))
    metadata_thread = Thread(name=f'metadata_{exchange_name}', target=launch_metadata_harvester_wrapper,
                             args=(exchange_name, connector_generator, historical_queue, realtime_queue,))

    historical_thread.start()
    # realtime_thread.start()
    metadata_thread.start()

    historical_thread.join()
    # realtime_thread.join()
    metadata_thread.join()
