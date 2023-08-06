from PyPSocket.protocols.tcp import *
from PyPSocket.exception import *
from abc import ABC, abstractmethod
from ipaddress import ip_address
from socket import AF_INET, AF_INET6
import functools


__all__ = [
    # Classes
    "AddressInfo", "HandlerType", "Option", "Event", "Handle", "Handler",
    # Functions
    "is_closed",
    "is_handle_closed",
    "is_handler_closed",
]


def is_closed(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._closed:
            raise ObjectDisposedException(self)
        return func(self, *args, **kwargs)
    return wrapper


def is_handle_closed(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._closed:
            raise HandleClosedException(self)
        return func(self, *args, **kwargs)
    return wrapper


def is_handler_closed(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._closed:
            raise HandlerClosedException(self)
        return func(self, *args, **kwargs)
    return wrapper


def ip_valid_check(address):
    try:
        ip_address(address)
        return address
    except Exception:
        raise OutOfRangeAddressInfoException(address)


def port_valid_check(port):
    if port <= 65535:
        return port
    else:
        raise OutOfRangeAddressInfoException(port)


class HandlerType:
    @property
    def TCP(self):
        return TCPHandler


class AddressInfo:
    def __init__(self, address, port=80):
        self.address = ip_valid_check(address)
        self.port = port

    @property
    def version(self):
        ver = ip_address(self.address).version
        return AF_INET if ver == 4 else AF_INET6 if ver == 6 else None


class Option:
    def __init__(self, handler, *args, **kwargs):
        self.handler = handler
        self.args = args
        self.kwargs = kwargs


class Event:
    def __init__(self, func):
        self._event_handlers = []
        self._func = func

    def __iadd__(self, other):
        self._event_handlers.append(other)
        return self

    def __isub__(self, other):
        self._event_handlers.remove(other)
        return self

    def __iter__(self):
        return iter(self._event_handlers)

    def __call__(self, *args, **kwargs):
        self._func(*args, **kwargs)


class Handle(ABC):
    _socket = None
    _opened = False
    _closed = False
    _buffer_size = 8192

    def open(self, socket):
        self._socket = socket
        self._opened = True

    @abstractmethod
    def pack(self, size, data):
        pass

    @abstractmethod
    def unpack(self, data):
        pass

    @abstractmethod
    def send(self, **kwargs):
        pass

    @abstractmethod
    def receive(self):
        pass

    def close(self):
        self._socket.close()
        self._closed = True
        self._opened = False

    @property
    def buffer_size(self):
        return self._buffer_size

    @buffer_size.setter
    def buffer_size(self, size):
        i = 1
        kb = 1024
        while True:
            if kb * i >= size:
                self._buffer_size = kb * i
                break
            i += 1


class Handler(ABC):
    _socket = None
    _opened = False
    _closed = False

    @abstractmethod
    def serve(self, address_info):
        pass

    @abstractmethod
    def connect(self, address_info):
        pass

    @abstractmethod
    def accept(self):
        pass

    def close(self):
        self._socket.close()
        self._closed = True
        self._opened = False
