import socket
import tempfile
from os import unlink
from os.path import abspath, join, exists
from Constants import MESSAGE_SOCKET_FILE_NAME
from threading import Thread


class MessagesSocketServer:
    _messages_socket_file = abspath(join(tempfile.gettempdir(), MESSAGE_SOCKET_FILE_NAME))

    def __init__(self):
        self._clients = list()
        self._server = None

    def create(self):
        self._free_socket_file()
        self._initialize_socket_listening()

    def listen_to_connection(self, connection):
        while True:
            data = connection.recv(4069)
            print(data)

    def _initialize_socket_listening(self):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(self._messages_socket_file)
            sock.listen(5)

            while True:
                connection, client_address = sock.accept()
                listener = Thread(target=self.listen_to_connection, args=(connection,))
                listener.start()

        except Exception as error_message:
            print("Failed to initialize socket listening:")
            print(error_message)
        
    def _free_socket_file(self):
        if not exists(self._messages_socket_file):
            print("Socket file doesn't exist yet.")
            return True
        try:
            print("Unlink {}".format(self._messages_socket_file))
            unlink(self._messages_socket_file)
            return True
        except Exception as error_message:
            print("Something went wrong: {}".format(error_message))
        return False


class MessagesTransporter:
    pass


if __name__ == "__main__":
    msg_socket_server = MessagesSocketServer()
    if not msg_socket_server.create():
        exit(1)
