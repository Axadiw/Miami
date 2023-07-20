import asyncio
import json

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from streamlit_cookies_manager import EncryptedCookieManager

from pages.Account import COOKIES_PASSWORD, COOKIES_PREFIX, OAUTH_TOKEN_KEY, GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID, \
    BYBIT_API_SECRET_KEY, TC_ACCOUNT_KEY, BYBIT_API_KEY_KEY, TC_API_SECRET_KEY, TC_API_KEY_KEY
from users import is_authorized


async def get_google_email(oauthclient,
                           token):
    return await oauthclient.get_id_email(token['access_token'])


def get_configuration_for_authorized_user():
    # Check if account configured
    cookies = EncryptedCookieManager(
        prefix=COOKIES_PREFIX,
        password=COOKIES_PASSWORD
    )
    if not cookies.ready():
        st.stop()

    auth_token = json.loads(cookies[OAUTH_TOKEN_KEY]) if cookies is not None and \
                                                         OAUTH_TOKEN_KEY in cookies and \
                                                         cookies[OAUTH_TOKEN_KEY] != '' else None

    if not auth_token:
        st.write('Not logged in')
        st.stop()

    client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    email = asyncio.run(get_google_email(oauthclient=client, token=auth_token))[1]

    if not is_authorized(email):
        st.write('User not authorized')
        st.stop()

    three_commas_api_key = cookies[TC_API_KEY_KEY]
    three_commas_api_secret = cookies[TC_API_SECRET_KEY]
    three_commas_account = cookies[TC_ACCOUNT_KEY]
    bybit_api_key = cookies[BYBIT_API_KEY_KEY]
    bybit_api_secret = cookies[BYBIT_API_SECRET_KEY]

    if not three_commas_api_key or not three_commas_api_secret or not three_commas_account or not bybit_api_key or not bybit_api_secret:
        st.write('Configuration not completed')
        st.stop()

    return three_commas_api_key, three_commas_api_secret, three_commas_account, bybit_api_key, bybit_api_secret
