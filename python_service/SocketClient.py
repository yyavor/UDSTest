import time
import socket
import tempfile
from threading import Thread
from os.path import abspath, join
from Constants import MESSAGE_SOCKET_FILE_NAME


def test_send_message(socket_client, sec):
    """
    :param socket_client: SocketClient
    :return:
    """
    assert (isinstance(socket_client, SocketClient))
    while True:
        time.sleep(sec)
        socket_client.send_message(bytearray("{} {}".format(socket_client.name, time.strftime("%H:%M:%S")), 'utf8'))


class SocketClient(Thread):
    _messages_socket_file = abspath(join(tempfile.gettempdir(), MESSAGE_SOCKET_FILE_NAME))

    def __init__(self, name):
        Thread.__init__(self)
        self._socket = None
        self._name = name

    @property
    def name(self):
        return self._name

    def connect_to_server(self):
        self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            self._socket.connect(self._messages_socket_file)
            self.send_message(b"Connect me")
        except Exception as error_message:
            print("Failed to connect to {}".format(self._messages_socket_file))
            print("Reason: {}".format(error_message))

    def send_message(self, message):
        self._socket.sendall(message)

    def listen_for_income_messages(self):
        print("--- Start Listening {}".format(self._name))
        self.start()

    def run(self):
        while True:
            income_message = self._socket.recv(4096)
            print("{} got message:".format(self._name))
            print(income_message)


if __name__ == "__main__":
    socket_client1 = SocketClient("Client1")
    socket_client1.connect_to_server()
    socket_client1.listen_for_income_messages()

    socket_client2 = SocketClient("Client2")
    socket_client2.connect_to_server()
    socket_client2.listen_for_income_messages()

    sender1 = Thread(target=test_send_message, args=(socket_client1, 5))
    sender2 = Thread(target=test_send_message, args=(socket_client2, 2))
    sender1.start()
    sender2.start()

    sender1.join()
    sender2.join()
    socket_client1.join()
    socket_client2.join()

