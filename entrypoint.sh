#!/usr/bin/env bash
nohup ss-manager -k `uuidgen` -m aes-256-gcm -u --fast-open --reuse-port --manager-address /var/run/ss-manager.socks &
python3 worker.py

