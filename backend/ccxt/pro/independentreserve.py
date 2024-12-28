# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache
from ccxt.base.types import Int, OrderBook, Trade
from ccxt.async_support.base.ws.client import Client
from typing import List
from ccxt.base.errors import NotSupported
from ccxt.base.errors import ChecksumError


class independentreserve(ccxt.async_support.independentreserve):

    def describe(self):
        return self.deep_extend(super(independentreserve, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': False,
                'watchTicker': False,
                'watchTickers': False,
                'watchTrades': True,
                'watchTradesForSymbols': False,
                'watchMyTrades': False,
                'watchOrders': False,
                'watchOrderBook': True,
                'watchOHLCV': False,
            },
            'urls': {
                'api': {
                    'ws': 'wss://websockets.independentreserve.com',
                },
            },
            'options': {
                'watchOrderBook': {
                    'checksum': True,  # TODO: currently only working for snapshot
                },
            },
            'streaming': {
            },
            'exceptions': {
            },
        })

    async def watch_trades(self, symbol: str, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of `trade structures <https://docs.ccxt.com/#/?id=public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        url = self.urls['api']['ws'] + '?subscribe=ticker-' + market['base'] + '-' + market['quote']
        messageHash = 'trades:' + symbol
        trades = await self.watch(url, messageHash, None, messageHash)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client: Client, message):
        #
        #    {
        #        "Channel": "ticker-btc-usd",
        #        "Nonce": 130,
        #        "Data": {
        #          "TradeGuid": "7a669f2a-d564-472b-8493-6ef982eb1e96",
        #          "Pair": "btc-aud",
        #          "TradeDate": "2023-02-12T10:04:13.0804889+11:00",
        #          "Price": 31640,
        #          "Volume": 0.00079029,
        #          "BidGuid": "ba8a78b5-be69-4d33-92bb-9df0daa6314e",
        #          "OfferGuid": "27d20270-f21f-4c25-9905-152e70b2f6ec",
        #          "Side": "Buy"
        #        },
        #        "Time": 1676156653111,
        #        "Event": "Trade"
        #    }
        #
        data = self.safe_value(message, 'Data', {})
        marketId = self.safe_string(data, 'Pair')
        symbol = self.safe_symbol(marketId, None, '-')
        messageHash = 'trades:' + symbol
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        trade = self.parse_ws_trade(data)
        stored.append(trade)
        self.trades[symbol] = stored
        client.resolve(self.trades[symbol], messageHash)

    def parse_ws_trade(self, trade, market=None):
        #
        #    {
        #        "TradeGuid": "2f316718-0d0b-4e33-a30c-c2c06f3cfb34",
        #        "Pair": "xbt-aud",
        #        "TradeDate": "2023-02-12T09:22:35.4207494+11:00",
        #        "Price": 31573.8,
        #        "Volume": 0.05,
        #        "BidGuid": "adb63d74-4c02-47f9-9cc3-f287e3b48ab6",
        #        "OfferGuid": "b94d9bc4-addd-4633-a18f-69cf7e1b6f47",
        #        "Side": "Buy"
        #    }
        #
        datetime = self.safe_string(trade, 'TradeDate')
        marketId = self.safe_string(market, 'Pair')
        return self.safe_trade({
            'info': trade,
            'id': self.safe_string(trade, 'TradeGuid'),
            'order': self.safe_string(trade, 'orderNo'),
            'symbol': self.safe_symbol(marketId, market, '-'),
            'side': self.safe_string_lower(trade, 'Side'),
            'type': None,
            'takerOrMaker': None,
            'price': self.safe_string(trade, 'Price'),
            'amount': self.safe_string(trade, 'Volume'),
            'cost': None,
            'fee': None,
            'timestamp': self.parse8601(datetime),
            'datetime': datetime,
        }, market)

    async def watch_order_book(self, symbol: str, limit: Int = None, params={}) -> OrderBook:
        """
        watches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        symbol = market['symbol']
        if limit is None:
            limit = 100
        limitString = self.number_to_string(limit)
        url = self.urls['api']['ws'] + '/orderbook/' + limitString + '?subscribe=' + market['base'] + '-' + market['quote']
        messageHash = 'orderbook:' + symbol + ':' + limitString
        subscription: dict = {
            'receivedSnapshot': False,
        }
        orderbook = await self.watch(url, messageHash, None, messageHash, subscription)
        return orderbook.limit()

    def handle_order_book(self, client: Client, message):
        #
        #    {
        #        "Channel": "orderbook/1/eth/aud",
        #        "Data": {
        #          "Bids": [
        #            {
        #              "Price": 2198.09,
        #              "Volume": 0.16143952,
        #            },
        #          ],
        #          "Offers": [
        #            {
        #              "Price": 2201.25,
        #              "Volume": 15,
        #            },
        #          ],
        #          "Crc32": 1519697650,
        #        },
        #        "Time": 1676150558254,
        #        "Event": "OrderBookSnapshot",
        #    }
        #
        event = self.safe_string(message, 'Event')
        channel = self.safe_string(message, 'Channel')
        parts = channel.split('/')
        depth = self.safe_string(parts, 1)
        baseId = self.safe_string(parts, 2)
        quoteId = self.safe_string(parts, 3)
        base = self.safe_currency_code(baseId)
        quote = self.safe_currency_code(quoteId)
        symbol = base + '/' + quote
        orderBook = self.safe_dict(message, 'Data', {})
        messageHash = 'orderbook:' + symbol + ':' + depth
        subscription = self.safe_value(client.subscriptions, messageHash, {})
        receivedSnapshot = self.safe_bool(subscription, 'receivedSnapshot', False)
        timestamp = self.safe_integer(message, 'Time')
        # orderbook = self.safe_value(self.orderbooks, symbol)
        if not (symbol in self.orderbooks):
            self.orderbooks[symbol] = self.order_book({})
        orderbook = self.orderbooks[symbol]
        if event == 'OrderBookSnapshot':
            snapshot = self.parse_order_book(orderBook, symbol, timestamp, 'Bids', 'Offers', 'Price', 'Volume')
            orderbook.reset(snapshot)
            subscription['receivedSnapshot'] = True
        else:
            asks = self.safe_list(orderBook, 'Offers', [])
            bids = self.safe_list(orderBook, 'Bids', [])
            self.handle_deltas(orderbook['asks'], asks)
            self.handle_deltas(orderbook['bids'], bids)
            orderbook['timestamp'] = timestamp
            orderbook['datetime'] = self.iso8601(timestamp)
        checksum = self.handle_option('watchOrderBook', 'checksum', True)
        if checksum and receivedSnapshot:
            storedAsks = orderbook['asks']
            storedBids = orderbook['bids']
            asksLength = len(storedAsks)
            bidsLength = len(storedBids)
            payload = ''
            for i in range(0, 10):
                if i < bidsLength:
                    payload = payload + self.value_to_checksum(storedBids[i][0]) + self.value_to_checksum(storedBids[i][1])
            for i in range(0, 10):
                if i < asksLength:
                    payload = payload + self.value_to_checksum(storedAsks[i][0]) + self.value_to_checksum(storedAsks[i][1])
            calculatedChecksum = self.crc32(payload, True)
            responseChecksum = self.safe_integer(orderBook, 'Crc32')
            if calculatedChecksum != responseChecksum:
                error = ChecksumError(self.id + ' ' + self.orderbook_checksum_message(symbol))
                del client.subscriptions[messageHash]
                del self.orderbooks[symbol]
                client.reject(error, messageHash)
        if receivedSnapshot:
            client.resolve(orderbook, messageHash)

    def value_to_checksum(self, value):
        result = format(value, '.8f')
        result = result.replace('.', '')
        # remove leading zeros
        result = self.parse_number(result)
        result = self.number_to_string(result)
        return result

    def handle_delta(self, bookside, delta):
        bidAsk = self.parse_bid_ask(delta, 'Price', 'Volume')
        bookside.storeArray(bidAsk)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_heartbeat(self, client: Client, message):
        #
        #    {
        #        "Time": 1676156208182,
        #        "Event": "Heartbeat"
        #    }
        #
        return message

    def handle_subscriptions(self, client: Client, message):
        #
        #    {
        #        "Data": ["ticker-btc-sgd"],
        #        "Time": 1676157556223,
        #        "Event": "Subscriptions"
        #    }
        #
        return message

    def handle_message(self, client: Client, message):
        event = self.safe_string(message, 'Event')
        handlers: dict = {
            'Subscriptions': self.handle_subscriptions,
            'Heartbeat': self.handle_heartbeat,
            'Trade': self.handle_trades,
            'OrderBookSnapshot': self.handle_order_book,
            'OrderBookChange': self.handle_order_book,
        }
        handler = self.safe_value(handlers, event)
        if handler is not None:
            handler(client, message)
            return
        raise NotSupported(self.id + ' received an unsupported message: ' + self.json(message))
