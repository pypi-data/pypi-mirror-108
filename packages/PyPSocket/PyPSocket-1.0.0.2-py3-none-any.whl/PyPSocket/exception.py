from socket import error


__all__ = [
    # Classes
    "ObjectDisposedException",
    "OutOfRangeAddressInfoException",
    "HandleClosedException",
    "HandlerClosedException",
    "SocketConnectionError",
]


SocketConnectionError = (error,
                         ConnectionError,
                         BrokenPipeError,
                         ConnectionResetError,
                         ConnectionAbortedError,
                         ConnectionRefusedError
                         )


class ObjectDisposedException(Exception):
    def __init__(self, obj, msg="Cannot access a disposed object."):
        self._disposed_obj = obj
        super().__init__(msg)

    @property
    def disposed_object(self):
        return self._disposed_obj


class HandleClosedException(ObjectDisposedException):
    def __init__(self, handle):
        super(HandleClosedException, self).__init__(handle, "Cannot access the handle.")


class HandlerClosedException(ObjectDisposedException):
    def __init__(self, handle):
        super(HandlerClosedException, self).__init__(handle, "Cannot access the handler.")


class OutOfRangeAddressInfoException(Exception):
    def __init__(self, addr):
        self.__address = addr

    @property
    def address4_max(self):
        return 255

    @property
    def address4_min(self):
        return 0

    @property
    def address6_max(self):
        return 65535

    @property
    def address6_min(self):
        return 0

    @property
    def port_max(self):
        return 65535

    @property
    def port_min(self):
        return 0
