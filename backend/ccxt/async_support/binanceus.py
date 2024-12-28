# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.binance import binance
from ccxt.abstract.binanceus import ImplicitAPI


class binanceus(binance, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(binanceus, self).describe(), {
            'id': 'binanceus',
            'name': 'Binance US',
            'countries': ['US'],  # US
            'hostname': 'binance.us',
            'rateLimit': 50,  # 1200 req per min
            'certified': False,
            'pro': True,
            'urls': {
                'logo': 'https://github.com/user-attachments/assets/a9667919-b632-4d52-a832-df89f8a35e8c',
                'api': {
                    'web': 'https://www.binance.us',
                    'public': 'https://api.binance.us/api/v3',
                    'private': 'https://api.binance.us/api/v3',
                    'sapi': 'https://api.binance.us/sapi/v1',
                    'sapiV2': 'https://api.binance.us/sapi/v2',
                    'sapiV3': 'https://api.binance.us/sapi/v3',
                },
                'www': 'https://www.binance.us',
                'referral': 'https://www.binance.us/?ref=35005074',
                'doc': 'https://github.com/binance-us/binance-official-api-docs',
                'fees': 'https://www.binance.us/en/fee/schedule',
            },
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': self.parse_number('0.001'),  # 0.1% trading fee, zero fees for all trading pairs before November 1.
                    'maker': self.parse_number('0.001'),  # 0.1% trading fee, zero fees for all trading pairs before November 1.
                },
            },
            'options': {
                'fetchMarkets': ['spot'],
                'defaultType': 'spot',
                'fetchMargins': False,
                'quoteOrderQty': False,
            },
            'has': {
                'CORS': None,
                'spot': True,
                'margin': False,
                'swap': False,
                'future': None,
                'option': False,
                'addMargin': False,
                'closeAllPositions': False,
                'closePosition': False,
                'createReduceOnlyOrder': False,
                'fetchBorrowInterest': False,
                'fetchBorrowRate': False,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchBorrowRates': False,
                'fetchBorrowRatesPerSymbol': False,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchIsolatedPositions': False,
                'fetchLeverage': False,
                'fetchLeverageTiers': False,
                'fetchMarketLeverageTiers': False,
                'fetchMarkOHLCV': False,
                'fetchOpenInterestHistory': False,
                'fetchPosition': False,
                'fetchPositions': False,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'reduceMargin': False,
                'setLeverage': False,
                'setMargin': False,
                'setMarginMode': False,
                'setPositionMode': False,
            },
            'api': {
                'public': {
                    'get': {
                        'ping': 1,
                        'time': 1,
                        'exchangeInfo': 10,
                        'trades': 1,
                        'historicalTrades': 5,
                        'aggTrades': 1,
                        'depth': {'cost': 1, 'byLimit': [[100, 1], [500, 5], [1000, 10], [5000, 50]]},
                        'klines': 1,
                        'ticker/price': {'cost': 1, 'noSymbol': 2},
                        'avgPrice': 1,
                        'ticker/bookTicker': {'cost': 1, 'noSymbol': 2},
                        'ticker/24hr': {'cost': 1, 'noSymbol': 40},
                        'ticker': {'cost': 2, 'noSymbol': 100},
                    },
                },
                'private': {
                    'get': {
                        'account': 10,
                        'rateLimit/order': 20,
                        'order': 2,
                        'openOrders': {'cost': 3, 'noSymbol': 40},
                        'myTrades': 10,
                        'myPreventedMatches': 10,  # with ID it has weight 1, but we don't have that complex handling yet
                        'allOrders': 10,
                        'orderList': 2,
                        'allOrderList': 10,
                        'openOrderList': 3,
                    },
                    'post': {
                        'order': 1,
                        'order/test': 1,
                        'order/cancelReplace': 1,
                        'order/oco': 1,
                    },
                    'delete': {
                        'order': 1,
                        'openOrders': 1,
                        'orderList': 1,
                    },
                },
                'sapi': {
                    'get': {
                        'system/status': 1,
                        'asset/assetDistributionHistory': 1,
                        'asset/query/trading-fee': 1,
                        'asset/query/trading-volume': 1,
                        'sub-account/spotSummary': 1,
                        'sub-account/status': 1,
                        'otc/coinPairs': 1,
                        'otc/orders/{orderId}': 1,
                        'otc/orders': 1,
                        'ocbs/orders': 1,
                        'capital/config/getall': 1,
                        'capital/withdraw/history': 1,
                        'fiatpayment/query/withdraw/history': 1,
                        'capital/deposit/address': 1,
                        'capital/deposit/hisrec': 1,
                        'fiatpayment/query/deposit/history': 1,
                        'capital/sub-account/deposit/address': 1,
                        'capital/sub-account/deposit/history': 1,
                        'asset/query/dust-logs': 1,
                        'asset/query/dust-assets': 1,
                        'marketing/referral/reward/history': 1,
                        'staking/asset': 1,
                        'staking/stakingBalance': 1,
                        'staking/history': 1,
                        'staking/stakingRewardsHistory': 1,
                        'custodian/balance': 1,
                        'custodian/supportedAssetList': 1,
                        'custodian/walletTransferHistory': 1,
                        'custodian/custodianTransferHistory': 1,
                        'custodian/openOrders': 1,
                        'custodian/order': 1,
                        'custodian/orderHistory': 1,
                        'custodian/tradeHistory': 1,
                        'custodian/settlementSetting': 1,
                        'custodian/settlementHistory': 1,
                        'cl/transferHistory': 1,
                        'apipartner/checkEligibility': 1,
                        'apipartner/rebateHistory': 1,
                    },
                    'post': {
                        'otc/quotes': 1,
                        'otc/orders': 1,
                        'fiatpayment/withdraw/apply': 1,
                        'capital/withdraw/apply': 1,
                        'asset/dust': 10,
                        'staking/stake': 1,
                        'staking/unstake': 1,
                        'custodian/walletTransfer': 1,
                        'custodian/custodianTransfer': 1,
                        'custodian/undoTransfer': 1,
                        'custodian/order': 1,
                        'custodian/ocoOrder': 1,
                        'cl/transfer': 1,
                    },
                    'delete': {
                        'custodian/cancelOrder': 1,
                        'custodian/cancelOrdersBySymbol': 1,
                        'custodian/cancelOcoOrder': 1,
                    },
                },
                'sapiV2': {
                    'get': {
                        'cl/account': 10,
                        'cl/alertHistory': 1,
                    },
                },
                'sapiV3': {
                    'get': {
                        'accountStatus': 1,
                        'apiTradingStatus': 1,
                        'sub-account/list': 1,
                        'sub-account/transfer/history': 1,
                        'sub-account/assets': 1,
                    },
                    'post': {
                        'sub-account/transfer': 1,
                    },
                },
            },
        })
