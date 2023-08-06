class Trade:
    """
    Class to represent a Trade  

    ...

    Attributes
    ----------
    symbol : str
        symbol. e.g. "BTCPFC"
    size : int
        number of contracts. e.g. 100
    price : float
        price. e.g. 10290.5
    side : str
        side, which could be "BUY" or "SELL
    tradeId : str
        trade id. e.g. 91152933
    timestamp : int
        timestamp e.g. 1565135165600

    Documentation: https://www.btse.com/apiexplorer/futures/?python#wstrades  

    """

    def __init__(self) -> None:
        self.symbol = ''
        self.size = 0
        self.price = 0.0
        self.side = ''
        self.trade_id = 0
        self.timestamp = 0

    @staticmethod
    def from_json(data):
        trade = Trade()
        trade.symbol = data.get('symbol')
        trade.size = data.get('size')
        trade.price = data.get('price')
        trade.side = data.get('side')
        trade.trade_id = data.get('tradeid')
        trade.timestamp = data.get('timestamp')
        return trade


class TradeNotification:
    """
    Class to represent a Trade Notification

    ...

    Attributes
    ----------
    symbol : str
        market symbol. e.g. "BTCPFC"
    order_id : int
        BTSE internal order ID.
    side : str
        side, which could be "BUY" or "SELL"
    type : int
        type. 76 (Limit) | 77 (Market) | 80 (Peg)
    tx_type : str
        txType. STOP | TAKE_PROFIT
    price: float
        order or transacted price. e.g. 10290.5
    size : int
        contract size
    original_size: int
        originalSize. e.g. 5
    trigger_price: float
        triggerPrice
    peg_price_deviation: float
        peg price deviation
    stealth: str
        only valid for iceberg orders
    status: str
        status
    timestamp : int
        timestamp e.g. 1565135165600
    average_fill_price: float
        average fill price
    fill_size: str
        fillSize
    client_order_id: str
        client order ID
    maker: bool
        maker flag, if true indicates that trade is a maker trade
    remaining_size: int
        remaining size on the order
    time_in_force: str
        time when this order is valid


    Documentation: https://www.btse.com/apiexplorer/futures/?python#wstrades

    Sample response:
    {
    "topic": "notificationApiV2",
    data: {
      {
        "symbol": "Market symbol (eg. BTCPFC)",
        "orderID": "BTSE internal order ID",
        "side": "BUY",
        "type": 76 | 77 | 80,
        "txType": STOP | TAKE_PROFIT,
        "price": <Order or transacted price>,
        "size": <Contract size>,
        "originalSize": 5,
        "triggerPrice": <Trigger Price>,
        "pegPriceDeviation": <Peg price deviation>,
        "stealth": <Only valid for iceberg orders>,
        "status": <Refer to status enum>,
        "timestamp": <Trade timestamp>,
        "avgFillPrice": <Average fill price>,
        "fillSize": <Fill size>,
        "clOrderID": "<Client order ID>",
        "maker": "<Maker flag, if true indicates that trade is a maker trade>",
        "remainingSize": "<Remaining size on the order>",
        "time_in_force": "<Time where this order is valid>"
        }
      }
    }  

    """

    def __init__(self) -> None:
        self.symbol = ''
        self.order_id = 0
        self.side = ''
        self.type = None
        self.tx_type = None
        self.price = 0.0
        self.size = 0
        self.original_size = 0
        self.trigger_price = 0.0
        self.peg_price_deviation = 0.0
        self.stealth = ''
        self.status = ''
        self.timestamp = 0
        self.average_fill_price = 0.0
        self.fill_size = ''
        self.client_order_id = ''
        self.maker = None
        self.remaining_size = 0
        self.time_in_force = ''

    def __str__(self) -> str:
        object_dict = self.__dict__
        return str(object_dict.items())

    @staticmethod
    def from_json(data):
        trade_notification = TradeNotification()
        trade_notification.symbol = data.get('symbol')
        trade_notification.order_id = data.get('orderID')
        trade_notification.side = data.get('side')
        trade_notification.type = data.get('type')
        trade_notification.tx_type = data.get('txType')
        trade_notification.price = data.get('price')
        trade_notification.size = data.get('size')
        trade_notification.original_size = data.get('originalSize')
        trade_notification.trigger_price = data.get('triggerPrice')
        trade_notification.peg_price_deviation = data.get('pegPriceDeviation')
        trade_notification.stealth = data.get('stealth')
        trade_notification.status = data.get('status')
        trade_notification.timestamp = data.get('timestamp')
        trade_notification.average_fill_price = data.get('avgFillPrice')
        trade_notification.fill_size = data.get('fillSize')
        trade_notification.client_order_id = data.get('clOrderID')
        trade_notification.maker = data.get('maker')
        trade_notification.remaining_size = data.get('remainingSize')
        trade_notification.time_in_force = data.get('time_in_force')
        return trade_notification
