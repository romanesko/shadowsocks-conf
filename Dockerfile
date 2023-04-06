FROM ubuntu:22.04
RUN apt update -y 
RUN apt install shadowsocks-libev -y
RUN apt install python3 -y
WORKDIR /app
COPY shadowsocks_manager.py /app
RUN chmod a+x shadowsocks_manager.py
ENV PATH="$PATH:/app"
ENTRYPOINT [ "ss-manager","-k","d160e035-41e2-47c3-9a2f-8a8193298af5", "-m","aes-256-gcm", "-u", "--fast-open", "--reuse-port", "--manager-address", "/var/run/ss-manager.socks"]
