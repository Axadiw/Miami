import asyncio

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token
from streamlit_js_eval import streamlit_js_eval

from cookies import GOOGLE_REDIRECT_URL, BYBIT_API_SECRET_KEY, BYBIT_API_KEY_KEY, TC_ACCOUNT_KEY, \
    TC_API_SECRET_KEY, TC_API_KEY_KEY, OAUTH_TOKEN_KEY, OAUTH_REFRESH_TOKEN_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET


def account(localstorage_manager):
    async def write_authorization_url(oauthclient,
                                      redirect_uri):
        return await oauthclient.get_authorization_url(
            redirect_uri,
            scope=["email", 'profile'],
            extras_params={"access_type": "offline", 'prompt': 'consent'}
        )

    async def write_access_token(oauthclient,
                                 redirect_uri,
                                 authcode):
        return await oauthclient.get_access_token(authcode, redirect_uri)

    # ret =
    client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    raw_auth_token = localstorage_manager.get_localstorage(OAUTH_TOKEN_KEY)
    auth_token = OAuth2Token(raw_auth_token) if raw_auth_token else None

    query_params = st.experimental_get_query_params()

    if not auth_token:
        authorization_url = asyncio.run(
            write_authorization_url(oauthclient=client,
                                    redirect_uri=GOOGLE_REDIRECT_URL)
        )
        st.write(f'''<h3>
                <a target="_self"
                href="{authorization_url}">Click here to login</a></h3>''',
                 unsafe_allow_html=True)

        if 'code' in query_params:
            code = query_params['code']
            token = asyncio.run(
                write_access_token(oauthclient=client,
                                   redirect_uri=GOOGLE_REDIRECT_URL,
                                   authcode=code))
            print('dupa')
            localstorage_manager.set_localstorage(OAUTH_TOKEN_KEY, token)
            localstorage_manager.set_localstorage(OAUTH_REFRESH_TOKEN_KEY, token['refresh_token'])
            if localstorage_manager.save():
                streamlit_js_eval(js_expressions="window.location.reload()")
    else:
        three_commas_api_key = st.text_input('3commas API Key',
                                             value=(localstorage_manager.get_localstorage(TC_API_KEY_KEY) or ''))
        three_commas_api_secret = st.text_input('3commas API Secret',
                                                value=(localstorage_manager.get_localstorage(TC_API_SECRET_KEY) or ''))
        three_commas_account = st.text_input('3commas Account Id',
                                             value=(localstorage_manager.get_localstorage(TC_ACCOUNT_KEY) or ''))
        bybit_api_key = st.text_input('ByBit API Key',
                                      value=(localstorage_manager.get_localstorage(BYBIT_API_KEY_KEY) or ''))
        bybit_api_secret = st.text_input('ByBit API Secret',
                                         value=(localstorage_manager.get_localstorage(BYBIT_API_SECRET_KEY) or ''))

        def save():
            localstorage_manager.set_localstorage(TC_API_KEY_KEY, three_commas_api_key)
            localstorage_manager.set_localstorage(TC_API_SECRET_KEY, three_commas_api_secret)
            localstorage_manager.set_localstorage(TC_ACCOUNT_KEY, three_commas_account)
            localstorage_manager.set_localstorage(BYBIT_API_KEY_KEY, bybit_api_key)
            localstorage_manager.set_localstorage(BYBIT_API_SECRET_KEY, bybit_api_secret)
            if localstorage_manager.save():
                st.write('Saved successfully')

        st.button('Save', on_click=save)

        def log_out():
            if localstorage_manager.get_localstorage(OAUTH_TOKEN_KEY):
                localstorage_manager.delete_localstorage(OAUTH_TOKEN_KEY)
                localstorage_manager.delete_localstorage(OAUTH_REFRESH_TOKEN_KEY)
                if localstorage_manager.save():
                    streamlit_js_eval(js_expressions="window.location.reload()")

        st.button("Log out", on_click=log_out)
