import tempfile
from os.path import abspath, join, exists

class MessagesSocketServer:
    _messages_socket_file = abspath(join(tempfile.gettempdir(), "imp_msg.sock"))

    def __init__(self):
        self._clients = {}
        self._server = None

    def start(self):
        if not self._free_socket_file():
            return False
        self._initialize_socket_listening()
        return True
        

    def _initialize_socket_listening(self):
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.listen(1)

            while True:
                # Wait for a connection
                connection, client_address = sock.accept()
                try:
                    data = connection.recv(4096)
                        
                finally:
                    # Clean up the connection
                    connection.close()  
        except Exception as error_message:
            print("Failed to initialize socket listening:")
            print(error_message)
        
    def _free_socket_file(self):
        if not exists(self._messages_socket_file):
            print("Socket file doesn't exist yet.")
            return True
        try:
            print("Unlink {}".format(self._messages_socket_file))
            os.unlink(server_address)
            return True
        except Exception as error_message:
            print("Something went wrong: {}".format(error_message))
        return False

    

class MessagesTransporter:
    pass

if __name__ == "__main__":
    msg_socket_server = MessagesSocketServer()
    if not msg_socket_server.start():
        exit(1)
