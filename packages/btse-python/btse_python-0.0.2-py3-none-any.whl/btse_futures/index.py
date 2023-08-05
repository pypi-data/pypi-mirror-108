class PriceIndex:
    """
    Class to represent price index  

    ...

    Attributes
    ----------
    symbol: str  
        instrument symbol. e.g. BTCPFC  
    indexPrice : float  
        index price. e.g. 7217.1109184696
    lastPrice : float  
        last price. e.g. 7215.5
    markPrice : float  
        mark price. e.g. 7216.117928865

    Documentation: https://www.btse.com/apiexplorer/futures/?python#price-index  

    """

    def __init__(self) -> None:
        self.symbol = ''
        self.indexPrice = 0.0
        self.lastPrice = 0.0
        self.markPrice = 0.0

    @staticmethod
    def from_dict(data):
        price_index = PriceIndex()
        price_index.symbol = data.get('symbol')
        price_index.indexPrice = data.get('indexPrice')
        price_index.lastPrice = data.get('lastPrice')
        price_index.markPrice = data.get('markPrice')
        return price_index
