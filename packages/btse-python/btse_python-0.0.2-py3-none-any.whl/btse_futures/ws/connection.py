import json
import logging
import ssl
import threading
import time

import websocket
from btse_futures.auth import Credentials
from btse_futures.util import get_current_timestamp

# key: ws, value: connection
websocket_connection_handler = dict()

connection_id = 0


class WebsocketAgent:

    def __init__(self) -> None:
        print('WebsocketAgent instantiated')

    def on_message(self, ws, message):
        #print(f'message: {message}')
        global websocket_connection_handler
        self.websocket_connection = websocket_connection_handler[ws]
        self.websocket_connection.on_message(message)
        return

    def on_error(self, ws, error):
        print(f'error: {error}')
        global websocket_connection_handler
        self.websocket_connection = websocket_connection_handler[ws]
        self.websocket_connection.on_failure(error)

    def on_close(self, ws):
        print(f'on_close')
        global websocket_connection_handler
        self.websocket_connection = websocket_connection_handler[ws]
        self.websocket_connection.on_close()

    def on_open(self, ws):
        print('in on_open')
        global websocket_connection_handler
        self.websocket_connection = websocket_connection_handler[ws]
        self.websocket_connection.on_open(ws)

    def _websocket(self, *args):
        print(f'_websocket called')
        global websocket_connection_handler
        self.connection_instance = args[0]
        print(f'connection_instance.url: {self.connection_instance.url}')
        self.connection_instance.ws = websocket.WebSocketApp(self.connection_instance.url,
                                                             on_message=self.on_message,
                                                             on_error=self.on_error,
                                                             on_close=self.on_close)
        websocket_connection_handler[self.connection_instance.ws] = self.connection_instance
        print(f'self.connection_instance.ws: {self.connection_instance.ws}')
        print(f'self.connection_instance: {self.connection_instance}')
        self.connection_instance.logger.info(
            f'{str(self.connection_instance.id)} Connecting...')
        self.connection_instance.delay_in_second = -1
        self.connection_instance.ws.on_open = self.on_open
        self.connection_instance.ws.run_forever(
            sslopt={"cert_reqs": ssl.CERT_NONE})
        self.connection_instance.logger.info(
            f'{str(self.connection_instance.id)} Connection event loop down')
        if self.connection_instance.state == ConnectionState.CONNECTED:
            self.connection_instance.state = ConnectionState.IDLE


class ConnectionState:
    IDLE = 0
    CONNECTED = 1
    CLOSED_ON_ERROR = 2


class WebsocketConnection:

    def __init__(self, credentials: Credentials, url, watcher, request):
        self.credentials = credentials
        self.url = url
        self.watcher = watcher
        self.request = request

        self.__thread = None
        self.delay_in_second = -1
        self.ws = None
        self.last_receive_time = 0
        self.state = ConnectionState.IDLE
        global connection_id
        connection_id += 1
        self.id = connection_id
        self.logger = logging.getLogger("btse-futures")

    def connect(self):
        print(f'websocket url: {self.url}')
        print(
            f'in connect method of WebsocketConnection with state: {self.state}')
        if self.state == ConnectionState.CONNECTED:
            self.logger.info(
                f'Already connected. Connection id: {str(self.id)}')
        else:
            websocket_agent = WebsocketAgent()
            self.__thread = threading.Thread(
                target=websocket_agent._websocket, args=[self])
            self.__thread.start()

    def send(self, data):
        json_data = json.dumps(data)
        print(f'send called with data: {data}')
        print(f'self.ws: {self.ws}')
        self.ws.send(json_data)

    def close(self):
        self.ws.close()
        del websocket_connection_handler[self.ws]
        self.watcher.on_connection_closed(self)
        self.logger.error(
            f'Closing connection, identified by connection id: {str(self.id)}')

    def on_open(self, ws):
        print('in websocket connection on_open')
        print(f'connection id: {self.id}')
        self.logger.info(f'Connected to server. Connection id: {str(self.id)}')
        self.ws = ws
        self.last_receive_time = get_current_timestamp()
        self.state = ConnectionState.CONNECTED
        # self.watcher.on_connection_created(self)
        if self.request.subscription_handler is not None:
            self.request.subscription_handler(self)
        return

    def on_error(self, error_message):
        self.logger.error(f'error message: {error_message}')

    def on_failure(self, error):
        self.on_error(f'Error: {str(error)}')
        self.close_on_error()

    def on_message(self, message):
        self.last_receive_time = get_current_timestamp()
        self._parse_response_invoke_callback(message)

    def _parse_response_invoke_callback(self, message):
        response = None
        try:
            if self.request.json_parser is not None:
                response = self.request.json_parser(message)
                print(f'response: {response}')
        except Exception as e:
            self.on_error(f'failed to parse the response: {str(e)} ')

        try:
            if self.request.update_callback is not None:
                self.request.update_callback(response)
        except Exception as e:
            self.on_error(f'callback invocation error: {str(e)}')

        if self.request.auto_close:
            self.close()

    def close_on_error(self):
        if self.ws is not None:
            self.ws.close()
            self.state = ConnectionState.CLOSED_ON_ERROR
            self.logger.error(
                f'Connection, identified by connection id: {str(self.id)}, is closing due to error')
