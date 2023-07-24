import asyncio
import json

import streamlit as st

from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token

from cookies import get_cookies, GOOGLE_REDIRECT_URL, BYBIT_API_SECRET_KEY, BYBIT_API_KEY_KEY, TC_ACCOUNT_KEY, \
    TC_API_SECRET_KEY, TC_API_KEY_KEY, OAUTH_TOKEN_KEY, OAUTH_REFRESH_TOKEN_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

st.set_page_config(layout="wide")


async def write_authorization_url(oauthclient,
                                  redirect_uri):
    return await oauthclient.get_authorization_url(
        redirect_uri,
        scope=["email", 'profile'],
        extras_params={"access_type": "offline"},
    )


async def write_access_token(oauthclient,
                             redirect_uri,
                             authcode):
    return await oauthclient.get_access_token(authcode, redirect_uri)


cookies = get_cookies()
client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
auth_token = OAuth2Token(json.loads(cookies[OAUTH_TOKEN_KEY])) if cookies is not None and \
                                                                  OAUTH_TOKEN_KEY in cookies and \
                                                                  cookies[OAUTH_TOKEN_KEY] else None
queryParams = st.experimental_get_query_params()

if not auth_token:
    authorization_url = asyncio.run(
        write_authorization_url(oauthclient=client,
                                redirect_uri=GOOGLE_REDIRECT_URL)
    )
    st.write(f'''<h3>
            <a target="_self"
            href="{authorization_url}">Click here to login</a></h3>''',
             unsafe_allow_html=True)

    if 'code' in queryParams:
        code = queryParams['code']
        token = asyncio.run(
            write_access_token(oauthclient=client,
                               redirect_uri=GOOGLE_REDIRECT_URL,
                               authcode=code))

        cookies[OAUTH_TOKEN_KEY] = json.dumps(token)
        cookies[OAUTH_REFRESH_TOKEN_KEY] = token['refresh_token']
        cookies.save()
        st.experimental_set_query_params()
else:
    threeCommasAPIKey = st.text_input('3commas API Key',
                                      value=(cookies[TC_API_KEY_KEY] if TC_API_KEY_KEY in cookies else ''))
    threeCommasAPISecret = st.text_input('3commas API Secret',
                                         value=(cookies[TC_API_SECRET_KEY] if TC_API_SECRET_KEY in cookies else ''))
    threeCommasAccount = st.text_input('3commas Account Id',
                                       value=(cookies[TC_ACCOUNT_KEY] if TC_ACCOUNT_KEY in cookies else ''))
    bybitApiKey = st.text_input('ByBit API Key',
                                value=(cookies[BYBIT_API_KEY_KEY] if BYBIT_API_KEY_KEY in cookies else ''))
    bybitApiSecret = st.text_input('ByBit API Secret',
                                   value=(cookies[BYBIT_API_SECRET_KEY] if BYBIT_API_SECRET_KEY in cookies else ''))


    def save():
        cookies[TC_API_KEY_KEY] = threeCommasAPIKey
        cookies[TC_API_SECRET_KEY] = threeCommasAPISecret
        cookies[TC_ACCOUNT_KEY] = threeCommasAccount
        cookies[BYBIT_API_KEY_KEY] = bybitApiKey
        cookies[BYBIT_API_SECRET_KEY] = bybitApiSecret
        cookies.save()
        st.write('Saved successfully')


    st.button('Save', on_click=save)


    def log_out():
        if OAUTH_TOKEN_KEY in cookies:
            cookies[OAUTH_TOKEN_KEY] = ''
            cookies[OAUTH_REFRESH_TOKEN_KEY] = ''
            cookies.save()


    st.button("Log out", on_click=log_out)
