from PyPSocket.util import *
from PyPSocket.exception import *
from threading import Thread, Lock
from hashlib import sha256


__all__ = [
    # Classes
    "Server", "ServerEventHandler"
]


class Server:
    def __init__(self, address_info, option):
        self._address_info = address_info
        self._option = option

        self._handler = option.handler().serve(address_info)
        self._clients = {}
        self._processes = {}
        self._gateway_process = Thread(target=self._gateway, daemon=True)
        self._joiner_process = Thread(target=self._process_joiner, daemon=True)
        self._gateway_locker = Lock()
        self._joiner_locker = Lock()
        self._closed = False

        self.event = ServerEventHandler()
        self.client = ServerClientHandler(self)

    @staticmethod
    def _create_cid(object_):
        return sha256(str(id(object_)).encode("utf-8")).hexdigest().upper()

    @is_closed
    def _gateway(self):
        while not self._closed:
            try:
                handle = self._handler.accept()
                cid = self._create_cid(handle)
                process = Thread(target=self._listener, args=(cid,), daemon=True)
                process.start()
                self._gateway_locker.acquire()
                self._clients[cid] = handle
                self._processes[cid] = process
                self._gateway_locker.release()
                self.event.on_connect(cid)
            except HandlerClosedException as handler_closed_exception:
                return handler_closed_exception
            except Exception as exception:
                return self.event.on_gateway_broken(exception)

    @is_closed
    def _process_joiner(self):
        while not self._closed:
            try:
                processes_id = list(self._processes.copy().items())
                for cid, process in processes_id:
                    if not process.is_alive():
                        self._joiner_locker.acquire()
                        self.disconnect(cid)
                        self._joiner_locker.release()
            except Exception as exception:
                return self.event.on_joiner_broken(exception)

    @is_closed
    def _listener(self, cid):
        while not self._closed:
            try:
                data = self._clients[cid].receive()
                self.event.on_message(cid, data)
            except HandleClosedException as handle_closed_exception:
                return handle_closed_exception
            except Exception as exception:
                self.event.on_exception(cid, exception)

    @is_closed
    def send(self, cid, **kwargs):
        try:
            self._clients[cid].send(**kwargs)
        except HandleClosedException as handle_closed_exception:
            raise handle_closed_exception
        except Exception as exception:
            self.event.on_exception(cid, exception)

    @is_closed
    def broadcast(self, **kwargs):
        cids = self._clients.copy()
        for cid in cids.keys():
            try:
                self.send(cid, **kwargs)
            except HandleClosedException:
                pass

    @is_closed
    def disconnect(self, cid):
        self._processes[cid].join()
        self._clients[cid].close()
        del self._clients[cid], self._processes[cid]
        self.event.on_disconnect(cid)

    @is_closed
    def run(self):
        self._gateway_process.start()
        self._joiner_process.start()
        return self

    @is_closed
    def close(self):
        self._closed = True
        self._handler.close()
        [self.disconnect(i) for i in self._clients.keys()]
        self._gateway_process.join()
        self._joiner_process.join()
        self.event.on_close()


class ServerClientHandler:
    def __init__(self, parent):
        self._parent = parent

    def _get_client(self):
        return getattr(self._parent, "_clients")

    def get_buffer_size(self, cid):
        return self._get_client()[cid].buffer_size

    def set_buffer_size(self, cid, size):
        self._get_client()[cid].buffer_size = size


class ServerEventHandler:
    def __init__(self):
        self.on_connect = Event(self._connect)
        self.on_message = Event(self._message)
        self.on_exception = Event(self._exception)
        self.on_disconnect = Event(self._disconnect)
        self.on_close = Event(self._close)
        self.on_gateway_broken = Event(self._gateway_broken)
        self.on_joiner_broken = Event(self._joiner_broken)

    def _connect(self, cid):
        [i(cid) for i in self.on_connect]

    def _message(self, cid, msg):
        [i(cid, msg) for i in self.on_message]

    def _exception(self, cid, e):
        [i(cid, e) for i in self.on_exception]

    def _disconnect(self, cid):
        [i(cid) for i in self.on_disconnect]

    def _close(self):
        [i() for i in self.on_close]

    def _gateway_broken(self, e):
        [i(e) for i in self.on_gateway_broken]

    def _joiner_broken(self, e):
        [i(e) for i in self.on_joiner_broken]
