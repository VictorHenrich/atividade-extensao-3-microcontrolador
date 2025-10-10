from socket import socket, AF_INET, SOCK_STREAM
import _thread as threading
import json
from utils.abstract_class import AbstractClass
from core.settings import (
    CLIENT_SOCKET_HOST,
    CLIENT_SOCKET_PORT,
    SERVER_SOCKET_HOST,
    SERVER_SOCKET_PORT,
)


class AbstractStreamServerHandler(AbstractClass):
    def __init__(self, socket, address):
        super().__init__(AbstractStreamServerHandler)

        self.__socket = socket

        self.__address = address

    @property
    def socket(self):
        return self.__socket

    @property
    def address(self):
        return self.__address

    @AbstractClass.abstract_method
    def on_receive(self, data): ...

    def __repr__(self):
        return f"{self.__class__.__name__} address={self.__address} />"


class StreamServer(socket):
    def __init__(
        self,
        socket_connection_class,
        host=SERVER_SOCKET_HOST,
        port=SERVER_SOCKET_PORT,
        family=AF_INET,
        type=SOCK_STREAM,
    ):
        super().__init__(family, type)

        self.__socket_connection_class = socket_connection_class

        self.__host = host

        self.__port = port

        self.__connections = []

    def __handle_client_connection(self, client_connection):
        while True:
            received_data = client_connection.socket.recv(1024)

            client_connection.on_receive(received_data)

    def __perform_loop(self):
        client_socket, address = self.accept()

        client_connection = self.__socket_connection_class(client_socket, address)

        print(f"Client Connected: {client_connection}")

        self.__connections.append(client_connection)

        threading.start_new_thread(
            self.__handle_client_connection, (client_connection,)
        )

    def start(self):
        self.bind((self.__host, self.__port))

        self.listen()

        print(f"Start StreamServer: HOST={self.__host} PORT={self.__port}")

        while True:
            self.__perform_loop()


class AbstractStreamClientHandler(AbstractClass):
    def __init__(self):
        super().__init__(AbstractStreamClientHandler)

    @AbstractClass.abstract_method
    def on_receive(self, data): ...


class StreamClient(socket):
    def __init__(
        self,
        socket_handler_class,
        host=CLIENT_SOCKET_HOST,
        port=CLIENT_SOCKET_PORT,
        family=AF_INET,
        type=SOCK_STREAM,
    ):
        super().__init__(family, type)

        self.__socket_handler_class = socket_handler_class

        self.__host = host

        self.__port = port

    def __perform_loop(self):
        while True:
            data = self.recv(1024)

            socket_handler = self.__socket_handler_class()

            threading.start_new_thread(socket_handler.on_receive, (data,))

    def start(self):
        self.connect((self.__host, self.__port))

        print(f"Start StreamClient: HOST={self.__host} PORT={self.__port}")

        threading.start_new_thread(self.__perform_loop, ())

    def send_data(self, data):
        body = data

        if isinstance(data, str):
            body = data.encode("utf-8")

        if isinstance(data, (dict, list)):
            body = json.dumps(data).encode("utf-8")

        self.sendall(body)
