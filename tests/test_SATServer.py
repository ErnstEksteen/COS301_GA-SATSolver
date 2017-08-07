from unittest import TestCase
from server import SATServer
from threading import Thread
import socket


class TestSATServer(TestCase):

    def test_push_to_all(self):
        print("Testing 'push_to_all'")
        # Test Message
        msg = "Test Message#"

        # Server with two clients connected
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        client1 = TesterClient()
        client1.start()
        client2 = TesterClient()
        client2.start()
        while len(server_thread.threads) < 2:
            pass
        server_thread.push_to_all(msg)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        client2_response = None
        while client2_response is None:
            client2_response = client2.received
        self.assertEqual(msg, client1_response, "Client one did not receive the correct message.")
        self.assertEqual(msg, client2_response, "Client two did not receive the correct message.")

        # Clients disconnected test send message
        server_thread.push_to_all(msg)

        # New client connects
        client3 = TesterClient()
        client3.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_all(msg)
        client3_response = None
        while client3_response is None:
            client3_response = client3.received
        self.assertEqual(msg, client3_response, "Client three did not receive the correct message.")

        server_thread.close()

        # Server with one client connected
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        client1 = TesterClient()
        client1.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_all(msg)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        self.assertEqual(msg, client1_response, "The client did not receive the correct message.")
        server_thread.close()

        # Server with no clients
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        server_thread.push_to_all(msg)
        server_thread.close()

    def test_push_to_one(self):
        print("Testing 'push_to_one'")
        # Test Messages
        msg = "Test Message#"
        msg1 = "Test Message1#"
        msg2 = "Test Message2#"
        msg3 = "Test Message3#"

        # Server with two clients connected
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        client1 = TesterClient()
        client1.start()
        client2 = TesterClient()
        client2.start()
        while len(server_thread.threads) < 2:
            pass
        server_thread.push_to_one(2, msg2)
        client2_response = None
        while client2_response is None:
            client2_response = client2.received
        server_thread.push_to_one(1, msg1)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        self.assertEqual(msg1, client1_response, "Client one did not receive the correct message.")
        self.assertEqual(msg2, client2_response, "Client two did not receive the correct message.")

        # Send message to client which does not exist.
        server_thread.push_to_one(3, msg)

        # New client connects
        client3 = TesterClient()
        client3.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_one(3, msg3)
        client3_response = None
        while client3_response is None:
            client3_response = client3.received
        self.assertEqual(msg3, client3_response, "Client three did not receive the correct message.")

        server_thread.close()

        # Server with one client connected
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        client1 = TesterClient()
        client1.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_all(msg)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        self.assertEqual(msg, client1_response, "The client did not receive the correct message.")
        server_thread.close()

    def test_address_in_use_exception(self):
        print("Testing 'address_in_use_exception'")
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        # noinspection PyUnusedLocal
        another_server_thread = SATServer("localhost", 55555, None)
        server_thread.close()

    def test_process_message_from_client(self):
        print("Testing 'process_message_from_client'")
        # Test message
        msg = "Test Message#"
        msg_from_client = None
        # Function to get the message sent by the client

        def get_message_from_client(msg_to_process, server, client_id):
            nonlocal msg_from_client
            msg_from_client = msg_to_process
            return None

        server_thread = SATServer("localhost", 55555, get_message_from_client)
        server_thread.start()
        client1 = TesterClient(msg)
        client1.start()
        while msg_from_client is None:
            pass
        self.assertEqual(msg, msg_from_client, "The message sent by the client does not match the message received by "
                                               "the server.")
        get_message_from_client(None, None, None)
        server_thread.close()

    def test_get_port(self):
        print("Testing 'get_port'")
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        self.assertEqual(55555, server_thread.get_port(), "The get_port() function did not return the correct port "
                                                          "number")
        server_thread.close()

    def test_close(self):
        print("Testing 'close'")
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        client1 = TesterClient()
        client1.start()
        client2 = TesterClient()
        client2.start()
        client3 = TesterClient()
        client3.start()
        while len(server_thread.threads) < 3:
            pass
        server_thread.close()


class TesterClient(Thread):

    def __init__(self, msg=None, wait=False):
        Thread.__init__(self)
        self.msg = msg
        self.received = None
        self.wait = wait

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", 55555)
        sock.connect(server_address)
        try:
            if self.msg is None:
                total_msg = ""
                msg_chunk = ""
                while msg_chunk == "" or msg_chunk[-1] != '#':
                    msg_chunk = sock.recv(1024).strip().decode("utf-8").strip()
                    if msg_chunk == "":
                        break
                    total_msg += msg_chunk
                self.received = total_msg
            else:
                sock.sendall(self.msg.encode())
                if self.wait:
                    total_msg = ""
                    msg_chunk = ""
                    while msg_chunk == "" or msg_chunk[-1] != '#':
                        msg_chunk = sock.recv(1024).strip().decode("utf-8").strip()
                        if msg_chunk == "":
                            break
                        total_msg += msg_chunk
                    self.received = total_msg
        finally:
            sock.close()
