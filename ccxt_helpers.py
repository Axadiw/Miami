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


def set_hedge_mode(symbol, apiKey, apiSecret):
    return ccxt.bybit({
        'apiKey': apiKey,
        'secret': apiSecret,
    }).set_position_mode(True, f'{symbol.upper()}/USDT:USDT')


def set_max_cross_levarage(symbol, apiKey, apiSecret):
    leverage = ccxt.bybit().fetch_derivatives_market_leverage_tiers(
        f'{symbol.upper()}/USDT:USDT')[0]['maxLeverage']
    ccxt.bybit({
        'apiKey': apiKey,
        'secret': apiSecret,
    }).set_margin_mode(
        marginMode='CROSS',
        symbol=f'{symbol.upper()}/USDT:USDT',
        params={
            "leverage": leverage
        })


@st.cache_data
def get_current_price(symbol):
    return ccxt.bybit().fetch_derivatives_tickers()[f'{symbol.upper()}/USDT:USDT']['last']
