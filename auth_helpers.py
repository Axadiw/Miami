import json

import asyncio
import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token

from cookies import get_cookies, OAUTH_TOKEN_KEY, GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID, \
    BYBIT_API_SECRET_KEY, TC_ACCOUNT_KEY, BYBIT_API_KEY_KEY, TC_API_SECRET_KEY, TC_API_KEY_KEY, OAUTH_REFRESH_TOKEN_KEY
from users import is_authorized


async def get_google_email(oauthclient, token):
    return await oauthclient.get_id_email(token['access_token'])


async def get_refreshed_token(oauthclient, token):
    return await oauthclient.refresh_token(token)


def get_configuration_for_authorized_user():
    cookies = get_cookies()
    auth_token = OAuth2Token(json.loads(cookies[OAUTH_TOKEN_KEY])) if cookies is not None and \
                                                                      OAUTH_TOKEN_KEY in cookies and \
                                                                      cookies[OAUTH_TOKEN_KEY] != '' else None

    refresh_token = cookies[OAUTH_REFRESH_TOKEN_KEY] if cookies is not None and \
                                                        OAUTH_REFRESH_TOKEN_KEY in cookies and \
                                                        cookies[OAUTH_REFRESH_TOKEN_KEY] != '' else None

    if not auth_token or not refresh_token:
        st.write('Not logged in')
        st.markdown("<a href='Account' target='_self'>Log in here</a>", unsafe_allow_html=True)
        st.stop()

    client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    if auth_token.is_expired():
        new_token = asyncio.run(get_refreshed_token(oauthclient=client, token=refresh_token))
        cookies[OAUTH_TOKEN_KEY] = json.dumps(new_token)
        cookies.save()
        auth_token = new_token

    email = asyncio.run(get_google_email(oauthclient=client, token=auth_token))[1]

    if not is_authorized(email):
        st.write('User not authorized')
        st.stop()

    if TC_API_KEY_KEY not in cookies or TC_API_SECRET_KEY not in cookies or TC_ACCOUNT_KEY not in cookies or BYBIT_API_KEY_KEY not in cookies or BYBIT_API_SECRET_KEY not in cookies:
        st.write('Configuration not completed')
        st.stop()

    three_commas_api_key = cookies[TC_API_KEY_KEY]
    three_commas_api_secret = cookies[TC_API_SECRET_KEY]
    three_commas_account = cookies[TC_ACCOUNT_KEY]
    bybit_api_key = cookies[BYBIT_API_KEY_KEY]
    bybit_api_secret = cookies[BYBIT_API_SECRET_KEY]

    return three_commas_api_key, three_commas_api_secret, three_commas_account, bybit_api_key, bybit_api_secret
