import json
import logging
import time

from btse_futures.auth import Credentials, _signature
from btse_futures.model.orderbook import OrderBook
from btse_futures.model.trade import Trade, TradeNotification


class WebsocketRequest:

    def __init__(self) -> None:
        self.subscription_handler = None
        self.error_handler = None
        self.json_parser = None
        self.update_callback = None


class WebsocketRequestManager:

    def __init__(self, credentials: Credentials) -> None:
        self._credentials = credentials
        self.logger = logging.getLogger("btse-futures")

    def subscribe_orderbook_level1(self, instrument, grouping, callback, error_handler=None):

        def subscription_handler(connection):
            topic = f'orderBookApi:{instrument}_{grouping}'
            data = {"op": "subscribe", "args": [topic]}
            connection.send(data)
            time.sleep(0.01)

        def json_parse(json_payload):
            json_dict = json.loads(json_payload)
            order_book = None
            if json_dict.get('topic') == 'orderBookApi':
                order_book = OrderBook.from_json(json_dict)
                self.logger.info(f'orderbook: {order_book}')
            return order_book

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_orderbook_level2(self, instrument, level, callback, error_handler=None):

        def subscription_handler(connection):
            topic = f'orderBookL2Api:{instrument}_{level}'
            data = {"op": "subscribe", "args": [topic]}
            connection.send(data)
            time.sleep(0.01)

        def json_parse(json_payload):
            json_dict = json.loads(json_payload)
            order_book = None
            if json_dict.get('topic') == 'orderBookApi':
                order_book = OrderBook.from_json(json_dict)
                self.logger.info(f'orderbook: {order_book}')
            return order_book

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_trades(self, instrument, callback, error_handler=None):

        def subscription_handler(connection):
            data = {"op": "subscribe", "args": [
                f'tradeHistoryApi:{instrument}']}
            connection.send(data)
            time.sleep(0.01)

        def json_parse(json_payload):
            json_dict = json.loads(json_payload)
            trades = None
            if json_dict.get('topic') == 'tradeHistory':
                data = json_payload.get('data')
                trades = [Trade.from_json(trade_json) for trade_json in data]
                self.logger.info(f'trades: {trades}')
            return trades

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_user_trade_notifications(self, topic, callback, error_handler=None):

        def subscription_handler(connection):
            authentication_data = self._authentication_message()
            connection.send(authentication_data)
            time.sleep(1)
            data = {
                "op": "subscribe",
                "args": [f'{topic}']
            }
            connection.send(data)
            time.sleep(0.01)

        def json_parse(json_payload):
            json_dict = json.loads(json_payload)
            self.logger.info(f'json_dict: {json_dict}')
            trade_notifications = None
            if json_dict.get('topic') == 'notificationApiV2':
                data = json_dict.get('data')
                trade_notifications = [TradeNotification.from_json(
                    trade_notification_json) for trade_notification_json in data]
                for tn in trade_notifications:
                    self.logger.info(f'tn: {tn}')
            return trade_notifications

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def _authentication_message(self):
        nonce = str(int(time.time()*1000))
        path = f'/futures/api/topic{nonce}'
        signature = _signature(self._credentials, path)
        authentication_data = {"op": "authKeyExpires",
                               "args": [self._credentials.api_key, nonce, signature]}
        return authentication_data
