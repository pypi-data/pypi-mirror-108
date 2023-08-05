class Quote:
    """
    Class to represent a Quote  

    ...

    Attributes
    ----------
    size : int  
        order quantity or size. e.g. 1  
    price : float  
        price. e.g. 7000.0

    Documentation: https://www.btse.com/apiexplorer/futures/?python#wsorderbook  

    """

    def __init__(self, price, size) -> None:
        assert(isinstance(price, float))
        assert(isinstance(size, int))

        self.price = price
        self.size = size


class OrderBook:
    """
    Class to represent an OrderBook  

    ...

    Attributes
    ----------
    buyQuote : List[Quote]  
        list of buy quotes. e.g. 
        "buyQuote":
        [
          {
            "price": 0,
            "size": 0
          }
        ]  
    sellQuote : List[Quote]  
        list of sell quotes. e.g.
        "sellQuote":
        [
          {
            "price": 0,
            "size": 0
          }
        ]
    symbol : str  
        symbol. e.g. BTCPFC
    timestamp : int  
        timestamp. e.g. 1565135165600

    Documentation: https://www.btse.com/apiexplorer/futures/?python#wsorderbook  

    """

    def __init__(self) -> None:
        self.buyQuote = None
        self.sellQuote = None
        self.symbol = ''
        self.timestamp = 0

    @staticmethod
    def from_json(json_payload):
        data = json_payload.get('data')
        order_book = OrderBook()
        order_book.buyQuote = [Quote(float(quote.get('price')), int(
            quote.get('size'))) for quote in data.get('buyQuote')]
        order_book.sellQuote = [Quote(float(quote.get('price')), int(quote.get('size')))
                                for quote in data.get('sellQuote')]
        order_book.symbol = data.get('symbol')
        order_book.timestamp = data.get('timestamp')
        return order_book
