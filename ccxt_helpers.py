import ccxt
import streamlit as st


@st.cache_data
def get_balance(apiKey, apiSecret):
    return ccxt.bybit({
        'apiKey': apiKey,
        'secret': apiSecret,
    }).fetch_balance()['USDT']['total']


def get_ohlcv_data(symbol, interval, reverse_order=True):
    data = ccxt.bybit().fetch_ohlcv(
        f'{symbol.upper()}/USDT:USDT', interval)
    data.sort(key=lambda x: x[0], reverse=reverse_order)
    return data
