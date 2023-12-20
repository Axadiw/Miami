import asyncio
import logging
import os

import coloredlogs

from harvesting.data_harvesters.consts import HARVESTER_TYPE_ENVIRONMENT_VARIABLE
from harvesting.data_harvesters.exchanges.bybit.bybit_harvesters import launch_bybit
from harvesting.data_harvesters.harvester_core.common_harvester import create_all_timeframes


def run_prerequisites_for_all_harvesters():
    asyncio.run(create_all_timeframes())


def bybit():
    run_prerequisites_for_all_harvesters()
    asyncio.run(launch_bybit())


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    coloredlogs.install(fmt='%(asctime)s %(levelname)s %(message)s', isatty=True, level='INFO')
    harvester = os.environ[HARVESTER_TYPE_ENVIRONMENT_VARIABLE]
    if harvester == 'bybit':
        bybit()
