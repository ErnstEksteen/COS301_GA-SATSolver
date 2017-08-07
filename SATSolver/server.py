"""
    Module: server
    Description: defines a tcp server through which simple push and pull
                 operation are possible.
"""
import socket
from threading import Thread
from threading import Lock


class ClientThread(Thread):
    """
    Defines a client thread that will facilitate communication between client and server.
    """

    def __init__(self, conn, thread_id, server_thread):
        Thread.__init__(self)
        self.conn = conn
        self.open = True
        self.thread_id = thread_id
        self.read_thread = None
        self.server_thread = server_thread
        self.peer_name = conn.getpeername()

    def run(self):
        """
        Creates a thread that will read data sent by the client and pass it to the server thread for processing.
        """

        self.read_thread = Thread(self.recv_from_client(), self)

    def recv_from_client(self):
        """
        Reads data sent by the client and pass it to the DSL
        interpreter(or whatever the correct term for it is).
        """

        try:
            while self.open:
                msg_chunk = ""
                total_msg = ""
                while msg_chunk == "" or msg_chunk[-1] != '#':
                    msg_chunk = self.conn.recv(1024).strip().decode("utf-8").strip()
                    if msg_chunk == "":
                        self.kill()
                    total_msg += msg_chunk
                self.server_thread.process_message_from_client(msg_chunk, self.thread_id)
        except socket.error:
            return

    def send_to_client(self, msg):
        """
        Sends a msg to the client.
        :param msg: The data to be sent
        """

        self.conn.sendall(msg.encode())

    def kill(self):
        """
        Closes the connection with client.
        """

        print(BColors.FAIL + '[-]' + BColors.ENDC + ' Client disconnected: ' + '{0}'.format(self.peer_name[0])
              + ':{0}'.format(self.peer_name[1]))
        self.server_thread.remove_thread(self.thread_id)
        self.conn.close()


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SATServer(Thread):

    """
    Defines a SAT server. The server listens for new incoming connections and creates a new thread for each new
    connection. A higher module can request this server to broadcast data to all connected clients or send data to a
    single client. Clients can also send requests which will then be passed to a higher module.
    """

    def __init__(self, host, port, message_decoder):
        super(SATServer, self).__init__()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((host, port))
            self.socket.listen(5)
            print("Server listening on port: " + str(port))
        except socket.error:
            print('Address already in use.')
            return
        self.thread_id_iter = 1
        self.lock = Lock()
        self.threads = []
        self.message_decoder = message_decoder

    def run(self):
        """
        Listens for new connections and creates a ClientThread when a client connects and appends it to the threads
        array.
        """

        try:
            while True:
                client_connection, address = self.socket.accept()
                self.lock.acquire()
                try:
                    new_thread = ClientThread(client_connection, self.thread_id_iter, self)
                    self.thread_id_iter += 1
                    new_thread.start()
                    self.threads.append(new_thread)
                finally:
                    self.lock.release()
                print(BColors.OKGREEN + '[+]' + BColors.ENDC + ' Client connected: {0}'.format(address[0]) +
                      ':{0}'.format(address[1]))
        except ConnectionAbortedError:
            return

    def push_to_all(self, msg):
        """
        Broadcasts a message to all connected clients.
        :param msg: The data that will be broadcast.
        """

        for thread in self.threads:
            if thread:
                thread.send_to_client(msg)

    def push_to_one(self, thread_id, msg):
        """
        Sends a message to a single client provided the thread's id on which the connection to the client
        is open.
        :param thread_id: The ID of the thread that has the socket to which the client is connected.
        :param msg: The data that will be sent to the client.
        """

        self.lock.acquire()
        try:
            index = 0
            while (index < len(self.threads)) and (self.threads[index].thread_id != thread_id):
                index += 1
            if (index < len(self.threads)) and (self.threads[index]):
                self.threads[index].send_to_client(msg)
        finally:
            self.lock.release()

    def process_message_from_client(self, msg, client_thread_id):
        """
        Passes a message to the DSL interpreter(or whatever the correct term for it is) to be interpreted.
        :param msg: Data sent by a client.
        :param client_thread_id: The ID of the thread to which the client is connected.
        """

        print(BColors.OKBLUE + "> " + BColors.ENDC + "Processing message from client with thread-ID: "
              + str(client_thread_id))
        handle_thread = Thread(target=self.message_decoder, args=(msg, self, client_thread_id))
        handle_thread.start()

    def get_port(self):
        """
        Returns the port on which the server is running on.
        :return: The port the server is running on.
        """

        return self.socket.getsockname()[1]

    def remove_thread(self, thread_id):
        """
        Sets a thread given its thread_id in the threads array to None to mark it as closed.
        :param thread_id: The ID of the thread that needs to be removed.
        """

        self.lock.acquire()

        try:
            index = 0
            while (index < len(self.threads)) and (self.threads[index].thread_id != thread_id):
                index += 1
            if (index < len(self.threads)) and (self.threads[index]):
                self.threads.remove(self.threads[index])
        finally:
            self.lock.release()

    def close(self):
        """
        Terminates server operation.
        """

        while len(self.threads) > 0:
            self.threads[0].kill()
        self.socket.close()
        print("Server closed.")
        