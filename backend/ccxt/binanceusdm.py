# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.binance import binance
from ccxt.abstract.binanceusdm import ImplicitAPI
from ccxt.base.errors import InvalidOrder


class binanceusdm(binance, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(binanceusdm, self).describe(), {
            'id': 'binanceusdm',
            'name': 'Binance USDⓈ-M',
            'urls': {
                'logo': 'https://github.com/user-attachments/assets/871cbea7-eebb-4b28-b260-c1c91df0487a',
                'doc': [
                    'https://binance-docs.github.io/apidocs/futures/en/',
                    'https://binance-docs.github.io/apidocs/spot/en',
                    'https://developers.binance.com/en',
                ],
            },
            'has': {
                'CORS': None,
                'spot': False,
                'margin': False,
                'swap': True,
                'future': True,
                'option': None,
                'createStopMarketOrder': True,
            },
            'options': {
                'fetchMarkets': ['linear'],
                'defaultSubType': 'linear',
                # https://www.binance.com/en/support/faq/360033162192
                # tier amount, maintenance margin, initial margin
                'leverageBrackets': None,
                'marginTypes': {},
                'marginModes': {},
            },
            # https://binance-docs.github.io/apidocs/futures/en/#error-codes
            # https://developers.binance.com/docs/derivatives/usds-margined-futures/error-code
            'exceptions': {
                'exact': {
                    '-5021': InvalidOrder,  # {"code":-5021,"msg":"Due to the order could not be filled immediately, the FOK order has been rejected."}
                    '-5022': InvalidOrder,  # {"code":-5022,"msg":"Due to the order could not be executed, the Post Only order will be rejected."}
                    '-5028': InvalidOrder,  # {"code":-5028,"msg":"Timestamp for self request is outside of the ME recvWindow."}
                },
            },
        })

    def transfer_in(self, code: str, amount, params={}):
        # transfer from spot wallet to usdm futures wallet
        return self.futuresTransfer(code, amount, 1, params)

    def transfer_out(self, code: str, amount, params={}):
        # transfer from usdm futures wallet to spot wallet
        return self.futuresTransfer(code, amount, 2, params)
