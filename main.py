import streamlit as st

from cookies import COOKIES_PREFIX
from lib.streamlit_cookies_manager import CookieManager
from the_pages.Account import account
from the_pages.Market import market

st.set_page_config(page_title='Project Miami', page_icon='💵', layout='wide')

cookies = CookieManager(
    # prefix=COOKIES_PREFIX,
)
if not cookies.ready():
    st.stop()

page_names_to_funcs = {
    "account": account,
    "market": market,
}


def account_page():
    st.experimental_set_query_params(page='account')


def market_page():
    st.experimental_set_query_params(page='market')


st.sidebar.button("Account", on_click=account_page)
st.sidebar.button("Market", on_click=market_page)

query_params = st.experimental_get_query_params()

if 'page' not in query_params:
    page_names_to_funcs['account'](cookies)
else:
    page = query_params['page'][0] if len(query_params['page']) == 1 else ''

    if page not in page_names_to_funcs:
        st.write('Page not found')

    page_names_to_funcs[page](cookies)
