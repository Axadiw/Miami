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

symbol_val = st.text_input("Symbol")
direction_val = st.radio("direction", ['buy', 'sell'], horizontal=True)

maxLossCol1, maxLossCol2 = st.columns(2)
tp1Col1, tp1Col2 = st.columns(2)
tp2Col1, tp2Col2 = st.columns(2)
tp3Col1, tp3Col2 = st.columns(2)
slCol1, slCol2 = st.columns(2)
maxLoss = maxLossCol1.text_input("Max loss")
tp1 = tp1Col1.text_input("TP1")
tp2 = tp2Col1.text_input("TP2")
tp3 = tp3Col1.text_input("TP3")
sl = slCol1.text_input("SL")

maxLossType = maxLossCol2.radio(label='', key="Max loss type", options=['%', '$'], horizontal=True)
tp1Type = tp1Col2.radio(label='', key="tp1type", options=['%', '$'], horizontal=True)
tp2Type = tp2Col2.radio(label='', key="tp2type", options=['%', '$'], horizontal=True)
tp3Type = tp3Col2.radio(label='', key="tp3type", options=['%', '$'], horizontal=True)
slType = slCol2.radio(label='', key="sltype", options=['%', '$'], horizontal=True)
comment = st.text_input("Comment")

# Every form must have a submit button.
submitted = st.button("Submit")
# if submitted:
# submitted
