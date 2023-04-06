# !/usr/bin/env python3
import json
import os
import socket
import sys
from time import sleep

import redis

SERVER_SOCK = '/var/run/ss-manager.socks'
CLIENT_SOCK = '/tmp/shadowsocks-client.sock'


def sync(items_to_add, items_to_remove):
    try:
        for item in items_to_add:
            assert type(item) == list, 'Wrong data in items to add (expceting array)'
            assert len(item) == 2, 'Wrong data in items to add (should be [port, "password"] value)'

        for item in items_to_remove:
            assert type(item) == int, f'Wrong data in items to remove: expceting number got «{item}»'

    except AssertionError as e:
        print(e, file=sys.stderr)
        exit(1)

    if not items_to_add and not items_to_remove:
        print('Nothing to do', file=sys.stderr)
        exit(1)

    try:
        os.unlink(CLIENT_SOCK)
    except:
        pass

    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(CLIENT_SOCK)
        s.connect(SERVER_SOCK)

        def send(cmd: str):
            print(cmd)
            s.send(cmd.encode("utf-8"))
            resp = s.recv(1506).decode("utf-8")
            if resp != 'ok':
                print('ERROR:', file=sys.stderr)
                exit(1)

        for item in items_to_add:
            print('+', item[0])
            cmd = f"remove: {json.dumps({'server_port': item[0]})}"
            send(cmd)
            sleep(1)
            cmd = f"add: {json.dumps({'server_port': item[0], 'password': item[1]})}"
            send(cmd)

        for item in items_to_remove:
            print('-', item)
            cmd = f"remove: {json.dumps({'server_port': item})}"
            send(cmd)

        s.shutdown(socket.SHUT_RDWR)
        os.unlink(CLIENT_SOCK)


def main():
    print('starting')
    redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    while True:
        print('waiting for next message')
        with redis.Redis(connection_pool=redis_pool) as r:
            name, val = r.blpop('QUEUE')
            action, port, password = json.loads(val)

            def answer():
                print('answering', json.dumps([action, port]))
                r.rpush('RESPONSE', json.dumps([action, port]))

            if action == 'ADD':
                sync([[port, password]], [])
                print('add', port, password)
                answer()
            else:
                print('remove', port)
                sync([], [port])
                answer()

        sleep(0.1)


if __name__ == '__main__':
    while True:
      try:
        main()
      except Exception as e:
          print(e)

