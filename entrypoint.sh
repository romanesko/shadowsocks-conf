#!/usr/bin/env bash
ss-manager -k `uuidgen` -m aes-256-gcm -u --fast-open --reuse-port --manager-address /var/run/ss-manager.socks
