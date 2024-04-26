import json

from api.endpoints.consts import MAXIMUM_COMMENT_LENGTH, MAXIMUM_HELPER_URL_LENGTH
from api.endpoints.session.session import PARAMS_INVALID_RESPONSE
from api.exchange_wrappers.bybit_3commas_wrapper import Bybit3CommasWrapper
from api.tests.exchange_shared_test_helpers import create_exchange_account


def should_handle_properly_side(client, mocker, user1_token, common_params, wrapper_method_name, endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'Long'})
    assert response.data == b'dummy_create_response'

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'Short'})
    assert response.data == b'dummy_create_response'

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'long'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'short'})
    assert response.status_code == 400

    assert response.json == PARAMS_INVALID_RESPONSE
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'side': 'wrong'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def should_handle_properly_symbol(client, mocker, user1_token, common_params, wrapper_method_name, endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'symbol': ''})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def should_handle_properly_numeric_parameter(client, mocker, user1_token, common_params, wrapper_method_name,
                                             endpoint_query_name, parameter_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, parameter_name: '123'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, parameter_name: 0})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, parameter_name: -1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # int value
    name_ = {**common_params, parameter_name: 10}
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json=name_)
    assert response.data == b'dummy_create_response'

    # float value
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, parameter_name: 10.1})
    assert response.data == b'dummy_create_response'


def should_handle_properly_take_profits(client, mocker, user1_token, common_params, wrapper_method_name,
                                        endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': []})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': 1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': 'abc'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 2, 3]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # single tp not 100%
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 99]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [['a', 99]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[-1, 100]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[0, 100]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # single tp 100%
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 100]],
                                 'move_sl_to_breakeven_after_tp1': False})
    assert response.data == b'dummy_create_response'

    # floats
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 40.5], [2, 59.5]]})
    assert response.data == b'dummy_create_response'

    # ints
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 40], [2, 60]]})
    assert response.data == b'dummy_create_response'

    # need to sum up to 100
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 20], [2, 30]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # tp prices can't duplicate
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 50], [2, 30], [2, 20]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def should_handle_properly_stop_loss(client, mocker, user1_token, common_params, wrapper_method_name,
                                     endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': 'abc'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': 0})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': -1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # int value
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': 10})
    assert response.data == b'dummy_create_response'

    # float value
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'stop_loss': 10.1})
    assert response.data == b'dummy_create_response'


def should_handle_properly_soft_stop_loss(client, mocker, user1_token, common_params, wrapper_method_name,
                                          endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'soft_stop_loss_timeout': 'abc'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'soft_stop_loss_timeout': -1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'soft_stop_loss_timeout': 10.5})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'soft_stop_loss_timeout': 0})
    assert response.data == b'dummy_create_response'

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'soft_stop_loss_timeout': 100})
    assert response.data == b'dummy_create_response'


def should_handle_properly_comment(client, mocker, user1_token, common_params, wrapper_method_name,
                                   endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'comment': 1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # empty comment is correct
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'comment': ''})
    assert response.data == b'dummy_create_response'

    # too long comment
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'comment': "a" * (MAXIMUM_COMMENT_LENGTH + 1)})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def should_handle_properly_move_sl_to_be(client, mocker, user1_token, common_params, wrapper_method_name,
                                         endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'move_sl_to_breakeven_after_tp1': 1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'move_sl_to_breakeven_after_tp1': 'True'})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'move_sl_to_breakeven_after_tp1': True})
    assert response.data == b'dummy_create_response'

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'move_sl_to_breakeven_after_tp1': False})
    assert response.data == b'dummy_create_response'


def should_handle_properly_helper_url(client, mocker, user1_token, common_params, wrapper_method_name,
                                      endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'helper_url': 1})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE

    # empty url is correct
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'helper_url': ''})
    assert response.data == b'dummy_create_response'

    # too long url
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'helper_url': "a" * (MAXIMUM_HELPER_URL_LENGTH + 1)})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def fail_when_non_existing_account_provided(client, user1_token, common_params, wrapper_method_name,
                                            endpoint_query_name):
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'account_id': 10})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def fail_for_account_from_different_user(client, user1_token, user2_token, common_params, wrapper_method_name,
                                         endpoint_query_name):
    create_exchange_account(client, user1_token)

    response = client.post(endpoint_query_name, headers={"x-access-tokens": user2_token},
                           json=common_params)
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def should_have_at_least_2tps_when_moveto_be_set(client, mocker, user1_token, common_params, wrapper_method_name,
                                                 endpoint_query_name):
    create_exchange_account(client, user1_token)
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 100]]})
    assert response.status_code == 400
    assert response.json == PARAMS_INVALID_RESPONSE


def can_have_single_tp_when_dont_need_to_move_sl_to_be(client, mocker, user1_token, common_params, wrapper_method_name,
                                                       endpoint_query_name):
    create_exchange_account(client, user1_token)
    mocker.patch.object(Bybit3CommasWrapper, wrapper_method_name, return_value='dummy_create_response')
    response = client.post(endpoint_query_name, headers={"x-access-tokens": user1_token},
                           json={**common_params, 'take_profits': [[1, 100]],
                                 'move_sl_to_breakeven_after_tp1': False})
    assert response.data == b'dummy_create_response'
