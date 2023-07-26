import streamlit as st


COOKIES_PREFIX = 'project-miami'
COOKIES_PASSWORD = 'lk398kljsnmad0u2lknamwdasd'
GOOGLE_CLIENT_ID = '557728805244-se52pupm562v4bd60av6gfha4kgoni0r.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
# GOOGLE_REDIRECT_URL = 'http://localhost:8501?page=account'
GOOGLE_REDIRECT_URL = 'https://axadiw-miami.streamlit.app/?page=account'
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
