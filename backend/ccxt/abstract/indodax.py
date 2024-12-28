from ccxt.base.types import Entry


class ImplicitAPI:
    public_get_api_server_time = publicGetApiServerTime = Entry('api/server_time', 'public', 'GET', {'cost': 5})
    public_get_api_pairs = publicGetApiPairs = Entry('api/pairs', 'public', 'GET', {'cost': 5})
    public_get_api_price_increments = publicGetApiPriceIncrements = Entry('api/price_increments', 'public', 'GET', {'cost': 5})
    public_get_api_summaries = publicGetApiSummaries = Entry('api/summaries', 'public', 'GET', {'cost': 5})
    public_get_api_ticker_pair = publicGetApiTickerPair = Entry('api/ticker/{pair}', 'public', 'GET', {'cost': 5})
    public_get_api_ticker_all = publicGetApiTickerAll = Entry('api/ticker_all', 'public', 'GET', {'cost': 5})
    public_get_api_trades_pair = publicGetApiTradesPair = Entry('api/trades/{pair}', 'public', 'GET', {'cost': 5})
    public_get_api_depth_pair = publicGetApiDepthPair = Entry('api/depth/{pair}', 'public', 'GET', {'cost': 5})
    public_get_tradingview_history_v2 = publicGetTradingviewHistoryV2 = Entry('tradingview/history_v2', 'public', 'GET', {'cost': 5})
    private_post_getinfo = privatePostGetInfo = Entry('getInfo', 'private', 'POST', {'cost': 4})
    private_post_transhistory = privatePostTransHistory = Entry('transHistory', 'private', 'POST', {'cost': 4})
    private_post_trade = privatePostTrade = Entry('trade', 'private', 'POST', {'cost': 1})
    private_post_tradehistory = privatePostTradeHistory = Entry('tradeHistory', 'private', 'POST', {'cost': 4})
    private_post_openorders = privatePostOpenOrders = Entry('openOrders', 'private', 'POST', {'cost': 4})
    private_post_orderhistory = privatePostOrderHistory = Entry('orderHistory', 'private', 'POST', {'cost': 4})
    private_post_getorder = privatePostGetOrder = Entry('getOrder', 'private', 'POST', {'cost': 4})
    private_post_cancelorder = privatePostCancelOrder = Entry('cancelOrder', 'private', 'POST', {'cost': 4})
    private_post_withdrawfee = privatePostWithdrawFee = Entry('withdrawFee', 'private', 'POST', {'cost': 4})
    private_post_withdrawcoin = privatePostWithdrawCoin = Entry('withdrawCoin', 'private', 'POST', {'cost': 4})
    private_post_listdownline = privatePostListDownline = Entry('listDownline', 'private', 'POST', {'cost': 4})
    private_post_checkdownline = privatePostCheckDownline = Entry('checkDownline', 'private', 'POST', {'cost': 4})
    private_post_createvoucher = privatePostCreateVoucher = Entry('createVoucher', 'private', 'POST', {'cost': 4})
