import asyncio
import json

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token

from cookies import OAUTH_TOKEN_KEY, GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID, \
    BYBIT_API_SECRET_KEY, TC_ACCOUNT_KEY, BYBIT_API_KEY_KEY, TC_API_SECRET_KEY, TC_API_KEY_KEY, OAUTH_REFRESH_TOKEN_KEY
from users import is_authorized


async def get_google_email(oauthclient, token):
    return await oauthclient.get_id_email(token['access_token'])


async def get_refreshed_token(oauthclient, token):
    return await oauthclient.refresh_token(token)


def get_configuration_for_authorized_user(localstorage):
    raw_access_token = localstorage.getLocalStorageVal(key=OAUTH_TOKEN_KEY)
    raw_refresh_token = localstorage.getLocalStorageVal(key=OAUTH_REFRESH_TOKEN_KEY)
    auth_token = OAuth2Token(json.loads(raw_access_token)) if raw_access_token != '' else None
    refresh_token = raw_refresh_token if raw_refresh_token != '' else None

    if not auth_token or not refresh_token:
        st.write('Not logged in')
        st.markdown("<a href='?page=account' target='_self'>Log in here</a>", unsafe_allow_html=True)
        st.stop()

    client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    if auth_token.is_expired():
        new_token = asyncio.run(get_refreshed_token(oauthclient=client, token=refresh_token))
        localstorage.setLocalStorageVal(key=OAUTH_TOKEN_KEY, val=json.dumps(new_token))
        auth_token = new_token

    email = asyncio.run(get_google_email(oauthclient=client, token=auth_token))[1]

    if not is_authorized(email):
        st.write('User not authorized')
        st.stop()

    three_commas_api_key = localstorage.getLocalStorageVal(key=TC_API_KEY_KEY)
    three_commas_api_secret = localstorage.getLocalStorageVal(key=TC_API_SECRET_KEY)
    three_commas_account = localstorage.getLocalStorageVal(key=TC_ACCOUNT_KEY)
    bybit_api_key = localstorage.getLocalStorageVal(key=BYBIT_API_KEY_KEY)
    bybit_api_secret = localstorage.getLocalStorageVal(key=BYBIT_API_SECRET_KEY)

    if three_commas_api_key == '' or three_commas_api_secret == '' or three_commas_account == '' or bybit_api_key == '' or bybit_api_secret == '':
        st.write('Configuration not completed')
        st.stop()

    return three_commas_api_key, three_commas_api_secret, three_commas_account, bybit_api_key, bybit_api_secret
