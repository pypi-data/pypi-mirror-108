import logging

from btse_futures.ws.connection import WebsocketConnection
from btse_futures.ws.request import WebsocketRequestManager


class WebsocketClient:

    def __init__(self, **kwargs):
        """
        Websocket client to subscribe to updates and notifications from the server.

        ...

        Attributes
        ----------

        kwargs: Options available when connecting via websockets.
            credentials: Credentials
                BTSE api_key and secret
            url: str
                BTSE websocket URL
            auto_connect: bool 
                Reconnect automatically on loss of connection. Connection loss could be due to any of the following:
                              -- Network problem
                              -- Connection closed by the server (triggered after every 24 hours of continuous connection)
                              -- Connection closed due to inactivity (triggered after every 60 seconds of inactivity)
                              -- No message can be received from the server within a specified time. See receive_limit_ms
            receive_limit_ms: int
                Connection is terminated if no message is received within this time limit 
            connection_delay_failure: int
                Delay time before a reconnect attempt is made. Relevant if auto connect is enabled
        """

        if "credentials" in kwargs:
            self._credentials = kwargs["credentials"]
        self.websocket_request_manager = WebsocketRequestManager(
            self._credentials)
        self.connections = list()
        self.auto_connect = True
        self.receive_limit_ms = 60000
        self.connection_delay_failure = 1
        if "url" in kwargs:
            self.url = kwargs["url"]
        if "auto_connect" in kwargs:
            self.auto_connect = kwargs["auto_connect"]
        if "receive_limit_ms" in kwargs:
            self.receive_limit_ms = kwargs["receive_limit_ms"]
        if "connection_delay_failure" in kwargs:
            self.connection_delay_failure = kwargs["connection_delay_failure"]
        # TODO: add watcher to keep connections alive
        self.watcher = None
        self.logger = logging.getLogger("btse-futures")

    def __create_connection(self, request):
        connection = WebsocketConnection(
            self._credentials, self.url, self.watcher, request)
        self.connections.append(connection)
        connection.connect()

    def unsubscribe_all(self):
        for conn in self.connections:
            conn.close()
        self.connections.clear()

    def subscribe_orderbook_level1(self, instrument: str, grouping: int, callback, error_handler=None):
        """
        Orderbook
        https://www.btse.com/apiexplorer/futures/?python#wsorderbook
        """
        request = self.websocket_request_manager.subscribe_orderbook_level1(
            instrument, grouping, callback, error_handler)
        self.__create_connection(request)

    def subscribe_orderbook_level2(self, instrument: str, level: int, callback, error_handler=None):
        """
        Orderbook
        https://www.btse.com/apiexplorer/futures/?python#wsorderbook
        """
        request = self.websocket_request_manager.subscribe_orderbook_level2(
            instrument, level, callback, error_handler)
        self.__create_connection(request)

    def subscribe_trades(self, instrument: str, callback, error_handler=None):
        """
        Trades
        https://www.btse.com/apiexplorer/futures/?python#wstrades
        """
        request = self.websocket_request_manager.subscribe_trades(
            instrument, callback, error_handler)
        self.__create_connection(request)

    def subscribe_user_trade_notifications(self, topic: str, callback, error_handler=None):
        """
        User Trade Notification v2
        https://www.btse.com/apiexplorer/futures/?python#wsnotifications2
        """
        request = self.websocket_request_manager.subscribe_user_trade_notifications(
            topic, callback, error_handler)
        self.__create_connection(request)
