import streamlit as st

from auth_helpers import get_configuration_for_authorized_user
from ccxt_helpers import get_balance, get_current_price
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data


def market(cookies):
    st.title('Market')
    three_commas_api_key, three_commas_api_secret, three_commas_account, bybit_api_key, bybit_api_secret = \
        get_configuration_for_authorized_user(cookies)

    bybit_balance = get_balance(apiKey=bybit_api_key, apiSecret=bybit_api_secret)

    balance_container = st.empty()
    config_col, tradingview_col = st.columns(2)
    symbol_value_col, symbol_price_col = config_col.columns(2)

    balance_container.write('Balance {:.2f} $'.format(bybit_balance))
    symbol = symbol_value_col.text_input("Symbol")
    direction = config_col.radio("direction", ['buy 🟩', 'sell 🟥'], horizontal=True)

    max_loss_value_col, max_loss_type_col, max_loss_rendered_col = config_col.columns(3)
    tp1_value_col, tp1_type_col, tp1_rendered_col = config_col.columns(3)
    tp2_value_col, tp2_type_col, tp2_rendered_col = config_col.columns(3)
    tp3_value_col, tp3_type_col, tp3_rendered_col = config_col.columns(3)
    sl_value_col, sl_type_col, sl_rendered_col = config_col.columns(3)

    max_loss = max_loss_value_col.text_input("Max loss", value=1)
    tp1 = tp1_value_col.text_input("TP1", value=1)
    tp2 = tp2_value_col.text_input("TP2", value=2)
    tp3 = tp3_value_col.text_input("TP3", value=3)
    sl = sl_value_col.text_input("SL", value=10)

    max_loss_type = max_loss_type_col.radio(label="Max loss type", options=['%', '$'], horizontal=True)
    tp1_type = tp1_type_col.radio(label="tp1type", options=['%', '$'], horizontal=True, label_visibility='hidden')
    tp2_type = tp2_type_col.radio(label="tp2type", options=['%', '$'], horizontal=True)
    tp3_type = tp3_type_col.radio(label="tp3type", options=['%', '$'], horizontal=True)
    sl_type = sl_type_col.radio(label="sltype", options=['%', '$'], horizontal=True)
    comment = config_col.text_input("Comment")

    if max_loss:
        calculated_max_loss = float(max_loss) if max_loss_type == '$' else float(
            max_loss) * 0.01 * bybit_balance if max_loss else None
        if calculated_max_loss:
            max_loss_rendered_col.write('')
            max_loss_rendered_col.write('')
            max_loss_rendered_col.write(
                '{:.2f} $ ({:.2f} %)'.format(calculated_max_loss, 100.0 * calculated_max_loss / bybit_balance))

    if symbol:
        symbol_current_price = get_current_price(symbol)
        symbol_price_col.write('')
        symbol_price_col.write('')
        symbol_price_col.write('Current: {} $'.format(symbol_current_price))
        if tp1:
            calculated_tp1 = float(tp1) if tp1_type == '$' else symbol_current_price * (
                ((float(tp1)) / 100 + 1) if direction == 'buy 🟩' else (1 - (float(tp1)) / 100))
            tp1_rendered_col.write('')
            tp1_rendered_col.write('')
            tp1_rendered_col.write(
                ':green[{:+.2f} $ ({:+.2f} %)]'.format(calculated_tp1, 100.0 * calculated_tp1 / symbol_current_price - 100))
        if tp2:
            calculated_tp2 = float(tp1) if tp2_type == '$' else symbol_current_price * (
                ((float(tp2)) / 100 + 1) if direction == 'buy 🟩' else (1 - (float(tp2)) / 100))
            tp2_rendered_col.write('')
            tp2_rendered_col.write('')
            tp2_rendered_col.write(
                ':green[{:+.2f} $ ({:+.2f} %)]'.format(calculated_tp2, 100.0 * calculated_tp2 / symbol_current_price - 100))
        if tp3:
            calculated_tp3 = float(tp3) if tp1_type == '$' else symbol_current_price * (
                ((float(tp3)) / 100 + 1) if direction == 'buy 🟩' else (1 - (float(tp3)) / 100))
            tp3_rendered_col.write('')
            tp3_rendered_col.write('')
            tp3_rendered_col.write(
                ':green[{:+.2f} $ ({:+.2f} %)]'.format(calculated_tp3, 100.0 * calculated_tp3 / symbol_current_price - 100))
        if sl:
            calculated_sl = float(sl) if sl_type == '$' else symbol_current_price * (
                (1 - (float(sl)) / 100) if direction == 'buy 🟩' else (1 + (float(sl)) / 100))
            sl_rendered_col.write('')
            sl_rendered_col.write('')
            sl_rendered_col.write(
                ':red[{:+.2f} $ ({:+.2f} %)]'.format(calculated_sl, ((100.0 * calculated_sl / symbol_current_price) - 100)))

    # Every form must have a submit button.
    submitted = st.button("Submit")
    # if submitted:
    # submitted
    overlaidAreaSeriesOptions = {
        "height": 400,
        "rightPriceScale": {
            "scaleMargins": {
                "top": 0.1,
                "bottom": 0.1,
            },
            "mode": 2,  # PriceScaleMode: 0-Normal, 1-Logarithmic, 2-Percentage, 3-IndexedTo100
            "borderColor": 'rgba(197, 203, 206, 0.4)',
        },
        "timeScale": {
            "borderColor": 'rgba(197, 203, 206, 0.4)',
        },
        "layout": {
            "background": {
                "type": 'solid',
                "color": '#100841'
            },
            "textColor": '#ffffff',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(197, 203, 206, 0.4)',
                "style": 1,  # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
            },
            "horzLines": {
                "color": 'rgba(197, 203, 206, 0.4)',
                "style": 1,  # LineStyle: 0-Solid, 1-Dotted, 2-Dashed, 3-LargeDashed
            }
        }
    }

    seriesOverlaidChart = [
        {
            "type": 'Area',
            "data": data.priceCandlestickMultipane,
            "options": {
                "topColor": 'rgba(255, 192, 0, 0.7)',
                "bottomColor": 'rgba(255, 192, 0, 0.3)',
                "lineColor": 'rgba(255, 192, 0, 1)',
                "lineWidth": 2,
            },
            "markers": [
                {
                    "time": '2019-04-08',
                    "position": 'aboveBar',
                    "color": 'rgba(255, 192, 0, 1)',
                    "shape": 'arrowDown',
                    "text": 'H',
                    "size": 3
                },
                {
                    "time": '2019-05-13',
                    "position": 'belowBar',
                    "color": 'rgba(255, 192, 0, 1)',
                    "shape": 'arrowUp',
                    "text": 'L',
                    "size": 3
                },
            ]
        }
    ]

    with tradingview_col:
        chartOptions = {
            "layout": {
                "textColor": 'black',
                "background": {
                    "type": 'solid',
                    "color": 'white'
                }
            }
        }

        seriesCandlestickChart = [{
            "type": 'Candlestick',
            "data": [
                {"open": 10, "high": 10.63, "low": 9.49, "close": 9.55, "time": 1642427876},
                {"open": 9.55, "high": 10.30, "low": 9.42, "close": 9.94, "time": 1642514276},
                {"open": 9.94, "high": 10.17, "low": 9.92, "close": 9.78, "time": 1642600676},
                {"open": 9.78, "high": 10.59, "low": 9.18, "close": 9.51, "time": 1642687076},
                {"open": 9.51, "high": 10.46, "low": 9.10, "close": 10.17, "time": 1642773476},
                {"open": 10.17, "high": 10.96, "low": 10.16, "close": 10.47, "time": 1642859876},
                {"open": 10.47, "high": 11.39, "low": 10.40, "close": 10.81, "time": 1642946276},
                {"open": 10.81, "high": 11.60, "low": 10.30, "close": 10.75, "time": 1643032676},
                {"open": 10.75, "high": 11.60, "low": 10.49, "close": 10.93, "time": 1643119076},
                {"open": 10.93, "high": 11.53, "low": 10.76, "close": 10.96, "time": 1643205476}
            ],
            "options": {
                "upColor": '#26a69a',
                "downColor": '#ef5350',
                "borderVisible": False,
                "wickUpColor": '#26a69a',
                "wickDownColor": '#ef5350'
            }
        }]

        renderLightweightCharts([
            {
                "chart": chartOptions,
                "series": seriesCandlestickChart
            }
        ], 'candlestick')
