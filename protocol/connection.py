"""
This module contains the Connection class.
"""

import socket
import threading

from .counter import Counter


class Connection:
    """
    The Connection class is used to store and group information about a connection to a peer.
    """

    ip: str
    """
    The IP address of the peer.
    """

    port: int
    """
    The port used for the connection.
    """

    sock: socket.socket
    """
    The socket used for the connection.
    """

    sock_lock: threading.Lock
    """
    A lock used to synchronize access to the socket.
    """
    
    counter: Counter
    """
    """

    def __init__(self, ip: str, port: int, sock: socket.socket, sock_lock: threading.Lock):
        self.ip = ip
        self.port = port
        self.sock = sock
        self.sock_lock = sock_lock
        self.counter = Counter()
