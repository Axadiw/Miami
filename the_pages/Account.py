import asyncio
import json

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token

from cookies import GOOGLE_REDIRECT_URL, BYBIT_API_SECRET_KEY, BYBIT_API_KEY_KEY, TC_ACCOUNT_KEY, \
    TC_API_SECRET_KEY, TC_API_KEY_KEY, OAUTH_TOKEN_KEY, OAUTH_REFRESH_TOKEN_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET


def account(localstorage):
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
    raw_auth_token = localstorage.getLocalStorageVal(key=OAUTH_TOKEN_KEY)
    auth_token = OAuth2Token(json.loads(raw_auth_token)) if raw_auth_token != '' else None

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

            localstorage.setLocalStorageVal(key=OAUTH_TOKEN_KEY, val=json.dumps(token))
            localstorage.setLocalStorageVal(key=OAUTH_REFRESH_TOKEN_KEY, val=token['refresh_token'])
            st.experimental_set_query_params()
            st.experimental_rerun()
    else:
        three_commas_api_key = st.text_input('3commas API Key',
                                             value=(localstorage.getLocalStorageVal(key=TC_API_KEY_KEY)))
        three_commas_api_secret = st.text_input('3commas API Secret',
                                                value=(localstorage.getLocalStorageVal(key=TC_API_SECRET_KEY)))
        three_commas_account = st.text_input('3commas Account Id',
                                             value=(localstorage.getLocalStorageVal(key=TC_ACCOUNT_KEY)))
        bybit_api_key = st.text_input('ByBit API Key', value=(localstorage.getLocalStorageVal(key=BYBIT_API_KEY_KEY)))
        bybit_api_secret = st.text_input('ByBit API Secret',
                                         value=(localstorage.getLocalStorageVal(key=BYBIT_API_SECRET_KEY)))

        def save():
            localstorage.setLocalStorageVal(key=TC_API_KEY_KEY, val=three_commas_api_key)
            localstorage.setLocalStorageVal(key=TC_API_SECRET_KEY, val=three_commas_api_secret)
            localstorage.setLocalStorageVal(key=TC_ACCOUNT_KEY, val=three_commas_account)
            localstorage.setLocalStorageVal(key=BYBIT_API_KEY_KEY, val=bybit_api_key)
            localstorage.setLocalStorageVal(key=BYBIT_API_SECRET_KEY, val=bybit_api_secret)
            st.write('Saved successfully')

        st.button('Save', on_click=save)

        def log_out():
            if localstorage.getLocalStorageVal(key=OAUTH_TOKEN_KEY) != '':
                localstorage.setLocalStorageVal(key=OAUTH_TOKEN_KEY, val='')
                localstorage.setLocalStorageVal(key=OAUTH_REFRESH_TOKEN_KEY, val='')

        st.button("Log out", on_click=log_out)
