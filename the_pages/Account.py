import asyncio
import json

import streamlit as st

from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token

from cookies import GOOGLE_REDIRECT_URL, BYBIT_API_SECRET_KEY, BYBIT_API_KEY_KEY, TC_ACCOUNT_KEY, \
    TC_API_SECRET_KEY, TC_API_KEY_KEY, OAUTH_TOKEN_KEY, OAUTH_REFRESH_TOKEN_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET


def account(cookies):
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

    client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    auth_token = OAuth2Token(json.loads(cookies[OAUTH_TOKEN_KEY])) if cookies is not None and \
                                                                      OAUTH_TOKEN_KEY in cookies and \
                                                                      cookies[OAUTH_TOKEN_KEY] != '' else None

    query_params = st.experimental_get_query_params()

    if not auth_token:
        authorization_url = asyncio.run(
            write_authorization_url(oauthclient=client,
                                    redirect_uri=GOOGLE_REDIRECT_URL)
        )
        st.write(f'''<h3>
                <a target="_blank"
                href="{authorization_url}">Click here to login</a></h3>''',
                 unsafe_allow_html=True)

        if 'code' in query_params:
            code = query_params['code']
            token = asyncio.run(
                write_access_token(oauthclient=client,
                                   redirect_uri=GOOGLE_REDIRECT_URL,
                                   authcode=code))

            cookies[OAUTH_TOKEN_KEY] = json.dumps(token)
            cookies[OAUTH_REFRESH_TOKEN_KEY] = token['refresh_token']
            cookies.save()
            st.experimental_set_query_params()
    else:
        three_commas_api_key = st.text_input('3commas API Key',
                                          value=(cookies[TC_API_KEY_KEY] if TC_API_KEY_KEY in cookies else ''))
        three_commas_api_secret = st.text_input('3commas API Secret',
                                             value=(cookies[TC_API_SECRET_KEY] if TC_API_SECRET_KEY in cookies else ''))
        three_commas_account = st.text_input('3commas Account Id',
                                           value=(cookies[TC_ACCOUNT_KEY] if TC_ACCOUNT_KEY in cookies else ''))
        bybit_api_key = st.text_input('ByBit API Key',
                                    value=(cookies[BYBIT_API_KEY_KEY] if BYBIT_API_KEY_KEY in cookies else ''))
        bybit_api_secret = st.text_input('ByBit API Secret',
                                       value=(cookies[BYBIT_API_SECRET_KEY] if BYBIT_API_SECRET_KEY in cookies else ''))

        def save():
            cookies[TC_API_KEY_KEY] = three_commas_api_key
            cookies[TC_API_SECRET_KEY] = three_commas_api_secret
            cookies[TC_ACCOUNT_KEY] = three_commas_account
            cookies[BYBIT_API_KEY_KEY] = bybit_api_key
            cookies[BYBIT_API_SECRET_KEY] = bybit_api_secret
            cookies.save()
            st.write('Saved successfully')

        st.button('Save', on_click=save)

        def log_out():
            if OAUTH_TOKEN_KEY in cookies:
                cookies[OAUTH_TOKEN_KEY] = ''
                cookies[OAUTH_REFRESH_TOKEN_KEY] = ''
                cookies.save()

        st.button("Log out", on_click=log_out)
