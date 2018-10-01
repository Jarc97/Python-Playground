"""
Server Docstring
Current version: 0.1 (pre-alpha)
Made by Julio Rodriguez

This module implements a basic threaded server using the sockets.

"""
import os
import time
from sys import argv
import socket
import threading

# Global Variables
server_host = "localhost"
server_port = 9999
pid = 0
connected_users = 0
server_shutdown = False


class Server:
    def __init__(self, host, port):
        # Instance variables
        self.host = host
        self.port = port

        # Create a socket object and bound it to the address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def start_listening(self):
        global server_shutdown, connected_users
        # start listening for client connections
        self.sock.listen(5)
        # loop on the main thread to listen for
        # incoming clients
        while not server_shutdown:
            client_connection, client_address = self.sock.accept()
            print("Connection Accepted! :D")
            connected_users += 1
            client_connection.settimeout(5)

            print(threading.active_count())
            # Create a new thread with our subclass
            new_thread = ConnectionHandler(client_connection, client_address)
            new_thread.daemon = True
            new_thread.start()      # call run() from Thread


class ConnectionHandler(threading.Thread):
    # Class variables
    def __init__(self, client_connection, client_address):
        super().__init__()
        self.client_connection = client_connection
        self.client_address = client_address


    def run(self):
        self.handle()

    def handle(self):
        global connected_users
        buffer_size = 1024  # in bytes
        while True:
            try:
                data = self.client_connection.recv(buffer_size)
                if data:
                    # Set the response to echo back the received data
                    response = data
                    self.client_connection.send(response)
                else:
                    pass
                    # raise error('Client disconnected')
            except:
                self.client_connection.close()
                connected_users -= 1
                return False


# this class will give a CLI for server stats
class ServerManager:
    def __init__(self):
        pass

    def get_stats(self):
        global pid
        print("[Server Stats]")
        print("PID: " + str(pid))
        print("Users Connected: " + str(connected_users))
        print(threading.enumerate())


# Called from the Server Instance Thread
def start_server():
    # Create and configure server
    server_instance = Server(server_host, server_port)
    server_instance.start_listening()


def main():
    # Server information
    #global server_host, server_port

    # Create and start the server instance thread
    server_thread = threading.Thread(name="Server Instance Thread",
                                     target=start_server,
                                     daemon=True)
    server_thread.start()

    # Create the ServerManager instance
    # used to input commands and get stats
    manager = ServerManager()
    while True:
        time.sleep(1)
        manager.get_stats()
        os.system("cls")


if __name__ == "__main__":
    print("Launching Server...")
    # get script variables (wip)
    pid = os.getpid()
    print(threading.active_count())
    main()
    print("Server Ended")