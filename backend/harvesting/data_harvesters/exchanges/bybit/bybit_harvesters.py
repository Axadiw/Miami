from harvesting.data_harvesters.exchange_connectors.bybit_exchange_connector import BybitConnectorCCXT
from harvesting.data_harvesters.harvester_core.launch_harvesters import launch_all_harvesters_for_single_exchange


def bybit_connector_generator():
    return BybitConnectorCCXT()


async def launch_bybit():
    ohlcv_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w']
    # ohlcv_timeframes = ['1m']
    await launch_all_harvesters_for_single_exchange(exchange_name='bybit',
                                                    connector_generator=bybit_connector_generator,
                                                    ohlcv_timeframes=ohlcv_timeframes)
