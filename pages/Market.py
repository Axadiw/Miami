import streamlit as st

from auth_helpers import get_configuration_for_authorized_user
from ccxt_helpers import get_balance

three_commas_api_key, three_commas_api_secret, three_commas_account, bybit_api_key, bybit_api_secret = \
    get_configuration_for_authorized_user()

st.title('Market')
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

bybit_balance = get_balance(apiKey=bybit_api_key, apiSecret=bybit_api_secret)
st.write('Balance {} $'.format(bybit_balance))

config_col, config2_col, rendered_value_col, tradingview_col = st.columns([3, 1, 1, 3])

symbol_val = config_col.text_input("Symbol")
direction_val = config_col.radio("direction", ['buy', 'sell'], horizontal=True)

maxLoss = config_col.text_input("Max loss")
tp1 = config_col.text_input("TP1")
tp2 = config_col.text_input("TP2")
tp3 = config_col.text_input("TP3")
sl = config_col.text_input("SL")

maxLossType = config2_col.radio(label='', key="Max loss type", options=['%', '$'], horizontal=True)
tp1Type = config2_col.radio(label='', key="tp1type", options=['%', '$'], horizontal=True)
tp2Type = config2_col.radio(label='', key="tp2type", options=['%', '$'], horizontal=True)
tp3Type = config2_col.radio(label='', key="tp3type", options=['%', '$'], horizontal=True)
slType = config2_col.radio(label='', key="sltype", options=['%', '$'], horizontal=True)
comment = config_col.text_input("Comment")

calculated_max_loss = float(maxLoss) if maxLoss and maxLossType == '$' else float(maxLoss) * 0.01 * bybit_balance if maxLoss else None
rendered_value_col.write('{} $'.format(calculated_max_loss))

# Every form must have a submit button.
submitted = st.button("Submit")
# if submitted:
# submitted
