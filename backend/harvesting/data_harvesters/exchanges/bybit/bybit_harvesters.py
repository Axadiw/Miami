from harvesting.data_harvesters.exchange_connectors.bybit_exchange_connector import BybitConnectorCCXT
from harvesting.data_harvesters.harvester_core.launch_harvesters import launch_all_harvesters_for_single_exchange
from shared.consts import bybit_ohlcv_timeframes


def bybit_connector_generator():
    return BybitConnectorCCXT()


async def launch_bybit():
    await launch_all_harvesters_for_single_exchange(exchange_name='bybit',
                                                    connector_generator=bybit_connector_generator,
                                                    ohlcv_timeframes=bybit_ohlcv_timeframes)
