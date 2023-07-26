import streamlit as st

from auth_helpers import get_configuration_for_authorized_user
from ccxt_helpers import get_balance, get_current_price, get_ohlcv_data
from lib.streamlit_lightweight_charts import renderLightweightCharts


def market(cookies):
    st.title('Market')
    three_commas_api_key, three_commas_api_secret, three_commas_account, bybit_api_key, bybit_api_secret = \
        get_configuration_for_authorized_user(cookies)

    bybit_balance = get_balance(apiKey=bybit_api_key, apiSecret=bybit_api_secret)

    balance_container = st.empty()
    config_col, tradingview_col = st.columns([1, 2])
    symbol_value_col, symbol_price_col = config_col.columns(2)
    m1_col, m5_col, m15_col, h1_col, h4_col, d1_col = tradingview_col.columns(6)

    balance_container.write('Balance {:.2f} $'.format(bybit_balance))
    symbol = symbol_value_col.text_input("Symbol")

    if not symbol:
        st.stop()

    direction = config_col.radio("direction", ['buy 🟩', 'sell 🟥'], horizontal=True)

    max_loss_value_col, max_loss_type_col, max_loss_rendered_col = config_col.columns(3)
    tp1_value_col, tp1_type_col, tp1_rendered_col = config_col.columns(3)
    tp2_value_col, tp2_type_col, tp2_rendered_col = config_col.columns(3)
    tp3_value_col, tp3_type_col, tp3_rendered_col = config_col.columns(3)
    sl_value_col, sl_type_col, sl_rendered_col = config_col.columns(3)

    def response_to_ohlc(row):
        return {
            'time': row[0] / 1000,
            'open': row[1],
            'high': row[2],
            'low': row[3],
            'close': row[4],
            # 'volume': row[5],
        }

    def response_to_volume(row):
        return {
            'time': row[0] / 1000,
            'value': row[5],
            'color': 'rgba(0, 150, 136, 0.8)' if row[4] > row[1] else "rgba(255,82,82, 0.8)",
        }

    interval = '5m'
    if m1_col.button("M1"):
        interval = '1m'
    if m5_col.button("M5"):
        interval = '5m'
    if m15_col.button("M15"):
        interval = '15m'
    if h1_col.button("H1"):
        interval = '1h'
    if h4_col.button("H4"):
        interval = '4h'
    if d1_col.button("D1"):
        interval = '1d'

    response = get_ohlcv_data(symbol=symbol, interval=interval)
    coin_ohlc_data = list(map(response_to_ohlc, response)) if symbol else []
    coin_volume_data = list(map(response_to_volume, response)) if symbol else []
    max_loss = max_loss_value_col.text_input("Max loss", value=1)
    tp1 = tp1_value_col.text_input("TP1", value=1)
    tp2 = tp2_value_col.text_input("TP2", value=2)
    tp3 = tp3_value_col.text_input("TP3", value=3)
    sl = sl_value_col.text_input("SL", value=10)

    max_loss_type = max_loss_type_col.radio(label="Max loss type", options=['%', '$'], horizontal=True,
                                            label_visibility='hidden')
    tp1_type = tp1_type_col.radio(label="tp1type", options=['%', '$'], horizontal=True, label_visibility='hidden')
    tp2_type = tp2_type_col.radio(label="tp2type", options=['%', '$'], horizontal=True, label_visibility='hidden')
    tp3_type = tp3_type_col.radio(label="tp3type", options=['%', '$'], horizontal=True, label_visibility='hidden')
    sl_type = sl_type_col.radio(label="sltype", options=['%', '$'], horizontal=True, label_visibility='hidden')
    comment = config_col.text_input("Comment")
    price_lines = []

    def get_price_line_data(price, name, color):
        return {
            'price': price,
            'color': color,
            'lineWidth': 2,
            'lineStyle': 0,
            'axisLabelVisible': True,
            'title': name
        }

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
            tp1_rendered_col.markdown(
                '{:.2f} $ :green[({:+.2f} %)]'.format(calculated_tp1,
                                                      100.0 * calculated_tp1 / symbol_current_price - 100))
            price_lines.append(get_price_line_data(calculated_tp1, "TP1", "#26a69a"))
        if tp2:
            calculated_tp2 = float(tp1) if tp2_type == '$' else symbol_current_price * (
                ((float(tp2)) / 100 + 1) if direction == 'buy 🟩' else (1 - (float(tp2)) / 100))
            tp2_rendered_col.write('')
            tp2_rendered_col.write('')
            tp2_rendered_col.write(
                '{:.2f} $ :green[({:+.2f} %)]'.format(calculated_tp2,
                                                      100.0 * calculated_tp2 / symbol_current_price - 100))
            price_lines.append(get_price_line_data(calculated_tp2, "TP2", "#26a69a"))
        if tp3:
            calculated_tp3 = float(tp3) if tp3_type == '$' else symbol_current_price * (
                ((float(tp3)) / 100 + 1) if direction == 'buy 🟩' else (1 - (float(tp3)) / 100))
            tp3_rendered_col.write('')
            tp3_rendered_col.write('')
            tp3_rendered_col.write(
                '{:.2f} $ :green[({:+.2f} %)]'.format(calculated_tp3,
                                                      100.0 * calculated_tp3 / symbol_current_price - 100))
            price_lines.append(get_price_line_data(calculated_tp3, "TP3", "#26a69a"))
        if sl:
            calculated_sl = float(sl) if sl_type == '$' else symbol_current_price * (
                (1 - (float(sl)) / 100) if direction == 'buy 🟩' else (1 + (float(sl)) / 100))
            sl_rendered_col.write('')
            sl_rendered_col.write('')
            sl_rendered_col.write(
                '{:.2f} $ :red[({:+.2f} %)]'.format(calculated_sl,
                                                    ((100.0 * calculated_sl / symbol_current_price) - 100)))
            price_lines.append(get_price_line_data(calculated_sl, "SL", "#ef5350"))

    # Every form must have a submit button.
    submitted = st.button("Submit")
    # if submitted:
    # submitted

    with tradingview_col:
        chart_options = {
            "layout": {
                "textColor": 'black',
                "background": {
                    "type": 'solid',
                    "color": 'white'
                }
            }
        }

        series_candlestick_chart = [{
            "type": 'Candlestick',
            "data": coin_ohlc_data,
            "options": {
                "upColor": '#26a69a',
                "downColor": '#ef5350',
                "borderVisible": False,
                "wickUpColor": '#26a69a',
                "wickDownColor": '#ef5350'
            },
            "priceLines": price_lines
        }, {
            "type": 'Histogram',
            "data": coin_volume_data,
            "options": {
                "color": '#26a69a',
                "priceFormat": {
                    "type": 'volume',
                },
                "priceScaleId": "",  # set as an overlay setting,
                'lastValueVisible': False
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0.7,
                    "bottom": 0,
                },
            }
        }, ]

        renderLightweightCharts([
            {
                "chart": chart_options,
                "series": series_candlestick_chart
            }
        ], 'candlestick')
