import asyncio
import logging

from data_harvesters.exchanges.bybit.bybit_harvesters import launch_bybit
from data_harvesters.harvester_core.common_harvester import create_all_timeframes


def run_prerequisites_for_all_harvesters():
    asyncio.run(create_all_timeframes())


def run_harvesters_for_all_exchanges():
    asyncio.run(launch_bybit())


def launch_all_data_harvesters():
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    run_prerequisites_for_all_harvesters()
    run_harvesters_for_all_exchanges()


if __name__ == "__main__":
    launch_all_data_harvesters()
