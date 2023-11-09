from time import sleep
from multiprocessing import Process
from data_harvesters.bybit_harvester.bybit_harvester import BybitHarvester
from pybit.unified_trading import HTTP


def update_symbols(harvester):
    while True:
        harvester.update_list_of_symbols()
        sleep(5)


def update_kline(harvester):
    while True:
        print('will update kline')
        sleep(5)


def harvest_bybit():
    session = HTTP(testnet=False)
    harvester = BybitHarvester(session)
    p1 = Process(target=update_symbols, args=[harvester])
    p2 = Process(target=update_kline, args=[harvester])
    p1.start()
    p2.start()
