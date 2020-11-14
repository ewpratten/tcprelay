import argparse
import socket
from threading import Thread
from typing import *

class TCPRelay(Thread):

    client: socket.socket
    server: socket.socket
    buf_size: int
    name: str
    running = True

    def __init__(self, client: socket.socket, server: socket.socket, buf_size: Optional[int] = 1024, name: Optional[str] = "Unknown"):
        super().__init__()

        self.client = client
        self.server = server

        self.buf_size = buf_size
        self.name = name

    def stop(self):
        self.running = False

    def run(self):

        while self.running:

            data = self.client.recv(self.buf_size)

            if not data:
                print("No data")
                break

            print(f"[{self.name}]: {data}")

            self.server.send(data)
        
        print("Relay closed")

def main() -> int:

    ap = argparse.ArgumentParser(prog="tcprelay")
    ap.add_argument("rhost", help="remote host")
    ap.add_argument("rport", help="remote port", type=int)
    ap.add_argument("lport", help="local port", type=int)
    args = ap.parse_args()

    # Configure the server
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("0.0.0.0", args.lport))
    server_sock.listen(1)
    print(f"Listening for connections on 0.0.0.0:{args.lport}")

    # Wait for an incoming connection
    incoming_connection, incoming_address = server_sock.accept()
    print(f"Got incoming connection from: {incoming_address}")

    # Connect to the server
    remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_sock.connect((args.rhost, args.rport))
    print(f"Dialing: {(args.rhost, args.rport)}")

    # Relay data
    client_to_server_relay = TCPRelay(incoming_connection, remote_sock, name="Client")
    server_to_client_relay = TCPRelay(remote_sock, incoming_connection, name="Server")

    # Begin server-to-client
    server_to_client_relay.start()

    # Begin and join client
    client_to_server_relay.start()
    client_to_server_relay.join()

    # Cleanup
    print("Cleaning up")
    client_to_server_relay.stop()
    server_to_client_relay.stop()

    return 0

if __name__ == "__main__":
    exit(main())