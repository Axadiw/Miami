import asyncio
import logging
import coloredlogs
import sys

from data_harvesters.exchanges.bybit.bybit_harvesters import launch_bybit
from data_harvesters.harvester_core.common_harvester import create_all_timeframes


def run_prerequisites_for_all_harvesters():
    asyncio.run(create_all_timeframes())


def run_harvesters_for_all_exchanges():
    asyncio.run(launch_bybit())


def launch_all_data_harvesters():
    logger = logging.getLogger(__name__)
    coloredlogs.install(fmt='%(asctime)s %(levelname)s %(message)s', isatty=True, level='INFO')
    run_prerequisites_for_all_harvesters()
    run_harvesters_for_all_exchanges()


if __name__ == "__main__":
    launch_all_data_harvesters()
