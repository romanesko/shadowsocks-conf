#!/usr/bin/env python3
import sys
import socket, os,sys, json

SERVER_SOCK = '/var/run/ss-manager.socks'
CLIENT_SOCK = '/tmp/shadowsocks-client.sock'


data = None
try:
  data = json.loads(sys.argv[1])
except Exception as e:
  print("""Wrong or missing data param. Expecting: '[[[8138,"passwd"],[8139,"passwd"]],[8140,8141]]'""",file=sys.stderr)
  exit(1)

items_to_add = []
items_to_remove = []

try:
  assert len(data) ==2, 'Wrong data, expecting array of two elements (add/remove) items'

  items_to_add = data[0]
  items_to_remove = data[1]

  for item in items_to_add:
    assert type(item) == list, 'Wrong data in items to add (expceting array)'
    assert len(item) == 2, 'Wrong data in items to add (should be [port, "password"] value)'

  for item in items_to_remove:
    assert type(item) == int, f'Wrong data in items to remove: expceting number got «{item}»'

except AssertionError as e:
  print(e,file=sys.stderr)
  exit(1)

if not items_to_add and not items_to_remove:
  print('Nothing to do',file=sys.stderr)
  exit(1)

try:
  os.unlink(CLIENT_SOCK)
except:
  pass

with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(CLIENT_SOCK)  
  s.connect(SERVER_SOCK)  

  def send(cmd:str):
    s.send(cmd.encode("utf-8"))
    resp = s.recv(1506).decode("utf-8")
    if resp != 'ok':
      print('ERROR:', file=sys.stderr)
      exit(1)

  for item in items_to_add:
    print('+',item[0])
    cmd = f"remove: {json.dumps({'server_port':item[0]})}"
    send(cmd)
    cmd = f"add: {json.dumps({'server_port':item[0],'password':item[1]})}"
    send(cmd)
    
  for item in items_to_remove:
    print('-',item)
    cmd = f"remove: {json.dumps({'server_port':item})}"
    send(cmd)

  s.shutdown(socket.SHUT_RDWR)
  os.unlink(CLIENT_SOCK)

