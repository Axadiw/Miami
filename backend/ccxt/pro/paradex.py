# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache
from ccxt.base.types import Int, OrderBook, Strings, Ticker, Tickers, Trade
from ccxt.async_support.base.ws.client import Client
from typing import List


class paradex(ccxt.async_support.paradex):

    def describe(self):
        return self.deep_extend(super(paradex, self).describe(), {
            'has': {
                'ws': True,
                'watchTicker': True,
                'watchTickers': True,
                'watchOrderBook': True,
                'watchOrders': False,
                'watchTrades': True,
                'watchTradesForSymbols': False,
                'watchBalance': False,
                'watchOHLCV': False,
            },
            'urls': {
                'logo': 'https://x.com/tradeparadex/photo',
                'api': {
                    'ws': 'wss://ws.api.prod.paradex.trade/v1',
                },
                'test': {
                    'ws': 'wss://ws.api.testnet.paradex.trade/v1',
                },
                'www': 'https://www.paradex.trade/',
                'doc': 'https://docs.api.testnet.paradex.trade/',
                'fees': 'https://docs.paradex.trade/getting-started/trading-fees',
                'referral': '',
            },
            'options': {},
            'streaming': {},
        })

    async def watch_trades(self, symbol: str, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        get the list of most recent trades for a particular symbol

        https://docs.api.testnet.paradex.trade/#sub-trades-market_symbol-operation

        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of `trade structures <https://docs.ccxt.com/#/?id=public-trades>`
        """
        await self.load_markets()
        messageHash = 'trades.'
        if symbol is not None:
            market = self.market(symbol)
            messageHash += market['id']
        else:
            messageHash += 'ALL'
        url = self.urls['api']['ws']
        request: dict = {
            'jsonrpc': '2.0',
            'method': 'subscribe',
            'params': {
                'channel': messageHash,
            },
        }
        trades = await self.watch(url, messageHash, self.deep_extend(request, params), messageHash)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trade(self, client: Client, message):
        #
        #     {
        #         "jsonrpc": "2.0",
        #         "method": "subscription",
        #         "params": {
        #             "channel": "trades.ALL",
        #             "data": {
        #                 "id": "1718179273230201709233240002",
        #                 "market": "kBONK-USD-PERP",
        #                 "side": "BUY",
        #                 "size": "34028",
        #                 "price": "0.028776",
        #                 "created_at": 1718179273230,
        #                 "trade_type": "FILL"
        #             }
        #         }
        #     }
        #
        params = self.safe_dict(message, 'params', {})
        data = self.safe_dict(params, 'data', {})
        parsedTrade = self.parse_trade(data)
        symbol = parsedTrade['symbol']
        messageHash = self.safe_string(params, 'channel')
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            stored = ArrayCache(self.safe_integer(self.options, 'tradesLimit', 1000))
            self.trades[symbol] = stored
        stored.append(parsedTrade)
        client.resolve(stored, messageHash)
        return message

    async def watch_order_book(self, symbol: str, limit: Int = None, params={}) -> OrderBook:
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data

        https://docs.api.testnet.paradex.trade/#sub-order_book-market_symbol-snapshot-15-refresh_rate-operation

        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        messageHash = 'order_book.' + market['id'] + '.snapshot@15@100ms'
        url = self.urls['api']['ws']
        request: dict = {
            'jsonrpc': '2.0',
            'method': 'subscribe',
            'params': {
                'channel': messageHash,
            },
        }
        orderbook = await self.watch(url, messageHash, self.deep_extend(request, params), messageHash)
        return orderbook.limit()

    def handle_order_book(self, client: Client, message):
        #
        #     {
        #         "jsonrpc": "2.0",
        #         "method": "subscription",
        #         "params": {
        #             "channel": "order_book.BTC-USD-PERP.snapshot@15@50ms",
        #             "data": {
        #                 "seq_no": 14127815,
        #                 "market": "BTC-USD-PERP",
        #                 "last_updated_at": 1718267837265,
        #                 "update_type": "s",
        #                 "inserts": [
        #                     {
        #                         "side": "BUY",
        #                         "price": "67629.7",
        #                         "size": "0.992"
        #                     },
        #                     {
        #                         "side": "SELL",
        #                         "price": "69378.6",
        #                         "size": "3.137"
        #                     }
        #                 ],
        #                 "updates": [],
        #                 "deletes": []
        #             }
        #         }
        #     }
        #
        params = self.safe_dict(message, 'params', {})
        data = self.safe_dict(params, 'data', {})
        marketId = self.safe_string(data, 'market')
        market = self.safe_market(marketId)
        timestamp = self.safe_integer(data, 'last_updated_at')
        symbol = market['symbol']
        if not (symbol in self.orderbooks):
            self.orderbooks[symbol] = self.order_book()
        orderbookData = {
            'bids': [],
            'asks': [],
        }
        inserts = self.safe_list(data, 'inserts')
        for i in range(0, len(inserts)):
            insert = self.safe_dict(inserts, i)
            side = self.safe_string(insert, 'side')
            price = self.safe_string(insert, 'price')
            size = self.safe_string(insert, 'size')
            if side == 'BUY':
                orderbookData['bids'].append([price, size])
            else:
                orderbookData['asks'].append([price, size])
        orderbook = self.orderbooks[symbol]
        snapshot = self.parse_order_book(orderbookData, symbol, timestamp, 'bids', 'asks')
        snapshot['nonce'] = self.safe_number(data, 'seq_no')
        orderbook.reset(snapshot)
        messageHash = self.safe_string(params, 'channel')
        client.resolve(orderbook, messageHash)

    async def watch_ticker(self, symbol: str, params={}) -> Ticker:
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market

        https://docs.api.testnet.paradex.trade/#sub-markets_summary-operation

        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        symbol = self.symbol(symbol)
        channel = 'markets_summary'
        url = self.urls['api']['ws']
        request: dict = {
            'jsonrpc': '2.0',
            'method': 'subscribe',
            'params': {
                'channel': channel,
            },
        }
        messageHash = channel + '.' + symbol
        return await self.watch(url, messageHash, self.deep_extend(request, params), messageHash)

    async def watch_tickers(self, symbols: Strings = None, params={}) -> Tickers:
        """
        watches a price ticker, a statistical calculation with the information calculated over the past 24 hours for all markets of a specific list

        https://docs.api.testnet.paradex.trade/#sub-markets_summary-operation

        :param str[] symbols: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        symbols = self.market_symbols(symbols)
        channel = 'markets_summary'
        url = self.urls['api']['ws']
        request: dict = {
            'jsonrpc': '2.0',
            'method': 'subscribe',
            'params': {
                'channel': channel,
            },
        }
        messageHashes = []
        if isinstance(symbols, list):
            for i in range(0, len(symbols)):
                messageHash = channel + '.' + symbols[i]
                messageHashes.append(messageHash)
        else:
            messageHashes.append(channel)
        newTickers = await self.watch_multiple(url, messageHashes, self.deep_extend(request, params), messageHashes)
        if self.newUpdates:
            result: dict = {}
            result[newTickers['symbol']] = newTickers
            return result
        return self.filter_by_array(self.tickers, 'symbol', symbols)

    def handle_ticker(self, client: Client, message):
        #
        #     {
        #         "jsonrpc": "2.0",
        #         "method": "subscription",
        #         "params": {
        #             "channel": "markets_summary",
        #             "data": {
        #                 "symbol": "ORDI-USD-PERP",
        #                 "oracle_price": "49.80885481",
        #                 "mark_price": "49.80885481",
        #                 "last_traded_price": "62.038",
        #                 "bid": "49.822",
        #                 "ask": "58.167",
        #                 "volume_24h": "0",
        #                 "total_volume": "54542628.66054200416",
        #                 "created_at": 1718334307698,
        #                 "underlying_price": "47.93",
        #                 "open_interest": "6999.5",
        #                 "funding_rate": "0.03919997509811",
        #                 "price_change_rate_24h": ""
        #             }
        #         }
        #     }
        #
        params = self.safe_dict(message, 'params', {})
        data = self.safe_dict(params, 'data', {})
        marketId = self.safe_string(data, 'symbol')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        channel = self.safe_string(params, 'channel')
        messageHash = channel + '.' + symbol
        ticker = self.parse_ticker(data, market)
        self.tickers[symbol] = ticker
        client.resolve(ticker, channel)
        client.resolve(ticker, messageHash)
        return message

    def handle_error_message(self, client: Client, message):
        #
        #     {
        #         "jsonrpc": "2.0",
        #         "id": 0,
        #         "error": {
        #             "code": -32600,
        #             "message": "invalid subscribe request",
        #             "data": "invalid channel"
        #         },
        #         "usIn": 1718179125962419,
        #         "usDiff": 76,
        #         "usOut": 1718179125962495
        #     }
        #
        error = self.safe_dict(message, 'error')
        if error is None:
            return True
        else:
            errorCode = self.safe_string(error, 'code')
            if errorCode is not None:
                feedback = self.id + ' ' + self.json(error)
                self.throw_exactly_matched_exception(self.exceptions['exact'], '-32600', feedback)
                messageString = self.safe_value(error, 'message')
                if messageString is not None:
                    self.throw_broadly_matched_exception(self.exceptions['broad'], messageString, feedback)
            return False

    def handle_message(self, client: Client, message):
        if not self.handle_error_message(client, message):
            return
        #
        #     {
        #         "jsonrpc": "2.0",
        #         "method": "subscription",
        #         "params": {
        #             "channel": "trades.ALL",
        #             "data": {
        #                 "id": "1718179273230201709233240002",
        #                 "market": "kBONK-USD-PERP",
        #                 "side": "BUY",
        #                 "size": "34028",
        #                 "price": "0.028776",
        #                 "created_at": 1718179273230,
        #                 "trade_type": "FILL"
        #             }
        #         }
        #     }
        #
        data = self.safe_dict(message, 'params')
        if data is not None:
            channel = self.safe_string(data, 'channel')
            parts = channel.split('.')
            name = self.safe_string(parts, 0)
            methods: dict = {
                'trades': self.handle_trade,
                'order_book': self.handle_order_book,
                'markets_summary': self.handle_ticker,
                # ...
            }
            method = self.safe_value(methods, name)
            if method is not None:
                method(client, message)
