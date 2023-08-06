from PyPSocket.util import *
from PyPSocket.exception import *
from threading import Thread


__all__ = [
    # Classes
    "Client", "ClientEventHandler"
]


class Client:
    def __init__(self, address_info, option):
        self._address_info = address_info
        self._option = option

        self._handle = option.handler().connect(address_info)
        self._listener_process = Thread(target=self._listener, daemon=True)
        self._closed = False

        self.event = ClientEventHandler()

    @is_closed
    def _listener(self):
        while not self._closed:
            try:
                data = self._handle.receive()
                self.event.on_message(data)
            except HandleClosedException:
                return self.close(join_listener=False)
            except Exception as exception:
                self.event.on_exception(exception)

    @is_closed
    def send(self, **kwargs):
        try:
            self._handle.send(**kwargs)
        except HandleClosedException as handle_closed_exception:
            raise handle_closed_exception
        except Exception as exception:
            self.event.on_exception(exception)

    @is_closed
    def run(self):
        self._listener_process.start()
        self.event.on_connect()
        return self

    @is_closed
    def close(self, join_listener=True):
        self._closed = True
        self._handle.close()
        self._listener_process.join() if join_listener else None
        self.event.on_close()


class ClientEventHandler:
    def __init__(self):
        self.on_connect = Event(self._connect)
        self.on_message = Event(self._message)
        self.on_exception = Event(self._exception)
        self.on_close = Event(self._close)

    def _connect(self):
        [i() for i in self.on_connect]

    def _message(self, msg):
        [i(msg) for i in self.on_message]

    def _exception(self, e):
        [i(e) for i in self.on_exception]

    def _close(self):
        [i() for i in self.on_close]
