import streamlit as st

import streamlit as st
import urllib.parse
session = st.runtime.get_instance()._session_mgr.list_active_sessions()[0]
st_base_url = urllib.parse.urlunparse([session.client.request.protocol, session.client.request.host, "", "", "", ""])

COOKIES_PREFIX = 'project-miami'
COOKIES_PASSWORD = 'lk398kljsnmad0u2lknamwdasd'
GOOGLE_CLIENT_ID = '557728805244-vt0tdbqhn9qs4nccbrs940pmtl9lebt1.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URL = 'http://localhost:8501?page=account' if st_base_url == 'http://localhost:8501' else 'https://axadiw-miami.streamlit.app/?page=account'
OAUTH_TOKEN_KEY = 'oauth-token'
OAUTH_REFRESH_TOKEN_KEY = 'oauth-refresh-token'
TC_API_KEY_KEY = '3commas-api-key'
TC_API_SECRET_KEY = '3commas-secret'
TC_ACCOUNT_KEY = '3commas-account'
BYBIT_API_KEY_KEY = 'bybit-api-key'
BYBIT_API_SECRET_KEY = 'bybit-secret'


# Check if account configured
# cookies = EncryptedCookieManager(
#     prefix=COOKIES_PREFIX,
#     password=COOKIES_PASSWORD
# )

# @st.cache_resource(experimental_allow_widgets=True)
# def get_cookies():
#
#     cookies
