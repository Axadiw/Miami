from multiprocessing import Process

from data_harvesters.bybit_harvester import harvest_bybit


def run_data_harvesters():
    p = Process(target=harvest_bybit)
    p.start()
