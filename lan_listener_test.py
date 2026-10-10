# lan_listener_test.py

import socket

DISCOVERY_PORT = 55556

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.bind(
    ("", DISCOVERY_PORT)
)

print("Listening...")

while True:

    data, address = sock.recvfrom(1024)

    print(
        "Received:",
        data.decode(),
        "from",
        address
    )