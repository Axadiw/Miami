from multiprocessing import Process

import ccxt

from data_harvesters.bybit_harvester.bybit_harvester import BybitHarvester


def harvest_bybit():
    harvester = BybitHarvester(ccxt.bybit())
    harvester.start_loop()


def launch_data_harvesters():
    p = Process(target=harvest_bybit)
    p.start()
