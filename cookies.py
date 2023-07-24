import streamlit as st
from lib.streamlit_cookies_manager import CookieManager

COOKIES_PREFIX = 'project-miami'
COOKIES_PASSWORD = 'lk398kljsnmad0u2lknamwdasd'
GOOGLE_CLIENT_ID = '557728805244-p5lmcikopkrhqrbg3vhmimbk2grub3nb.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URL = 'http://localhost:8501/Account'
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

@st.cache_resource(experimental_allow_widgets=True)
def get_cookies():
    cookies = CookieManager(
        prefix=COOKIES_PREFIX,
    )
    if not cookies.ready():
        st.stop()
    cookies
