import json

from api.endpoints.consts import MAXIMUM_COMMENT_LENGTH, MAXIMUM_HELPER_URL_LENGTH
from api.endpoints.session.session import PARAMS_INVALID_RESPONSE
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper


def create_exchange_account(client, token):
    client.post('/add_new_exchange_account', headers={"x-access-tokens": token},
                json={'type': 'bybit_3commas',
                      'name': 'account 1',
                      'details': (json.dumps({'accountId': '12345', 'apiKey': 'abcdef', 'apiSecret': 'secret2'}))})
