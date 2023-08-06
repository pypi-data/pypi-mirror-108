from PyPSocket.util import *
from PyPSocket.exception import *
from socket import *
from json import dumps, loads
from base64 import b64encode, b64decode


__all__ = [
    # Class
    "TCPHandle",
    "TCPHandler"
]


class TCPHandle(Handle):
    def __init__(self, socket_, address_info):
        self._socket = socket_
        self.address = address_info

    @staticmethod
    def add_escape(data):
        escapes = (
            (b"\\", b"\\\\"),
            (b"\"", b"\\\""),
            (b"'", b"\\'"),
        )
        for i in escapes:
            data = data.replace(*i)
        return data

    @is_handle_closed
    def pack(self, size, data):
        packet = []
        cur, idx = 0, 0
        buff_sz = self._buffer_size
        while size - 1 > cur:
            temp = (b"[{\"size\":%d,\"sequence\":%d},\"" % (size, idx))
            sliced_data = data[cur:cur + buff_sz - len(temp) - 2]
            temp += sliced_data + b"\"]"
            temp += b" " * (buff_sz - len(temp))
            packet.append(temp)
            cur, idx = cur + len(sliced_data), idx + 1
        return b"".join(packet)

    @is_handle_closed
    def unpack(self, data):
        data = loads("".join(data))
        for i in data.keys():
            try:
                temp = b64decode(data[i])
                if temp:
                    data[i] = temp
                    continue
            except Exception:
                pass
        return data

    @is_handle_closed
    def send(self, **kwargs):
        try:
            # pack data
            [kwargs.update(**{key: b64encode(kwargs[key]).decode("utf-8")})
                for key in kwargs.keys() if isinstance(kwargs[key], bytes)]
            kwargs = dumps(kwargs, ensure_ascii=False).encode("utf-8")
            size, temp = len(kwargs), self.add_escape(kwargs)
            data = self.pack(size, temp)
            # send data
            self._socket.sendall(data)

        except SocketConnectionError:
            self._closed = True
            raise HandleClosedException(self)

    @is_handle_closed
    def receive(self):
        try:
            buffer = ""
            size = -1
            while size != len(buffer.encode("utf-8")):
                temp = b""
                while len(temp) != self._buffer_size:
                    temp += self._socket.recv(
                        self._buffer_size - len(temp) % self._buffer_size
                    )
                data = loads(temp)
                size = data[0]["size"] if size < 0 else size
                buffer += data[1]
            return self.unpack(buffer)

        except SocketConnectionError:
            self._closed = True
            raise HandleClosedException(self)


class TCPHandler(Handler):
    def serve(self, address_info):
        self._socket = socket(address_info.version, SOCK_STREAM)
        self._socket.bind((address_info.address, address_info.port))
        self._socket.listen()
        return self

    def connect(self, address_info):
        self._socket = socket(address_info.version, SOCK_STREAM)
        self._socket.connect((address_info.address, address_info.port))
        return TCPHandle(self._socket, address_info)

    @is_handler_closed
    def accept(self):
        try:
            sock, address = self._socket.accept()
            return TCPHandle(sock, AddressInfo(*address))
        except SocketConnectionError:
            self.close()
            raise HandlerClosedException(self)
