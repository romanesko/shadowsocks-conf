#!/usr/bin/env bash
apt update -y
apt install git docker docker-compose -y
cd ~
git clone https://github.com/romanesko/shadowsocks-conf
cd shadowsocks-conf
docker-compose up --build