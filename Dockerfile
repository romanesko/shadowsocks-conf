FROM ubuntu:22.04
RUN apt update -y 
RUN apt install shadowsocks-libev -y
RUN apt install python3 -y
RUN apt install uuid-runtime
RUN apt install pip3
RUN pip3 install redis
WORKDIR /app
COPY shadowsocks_manager.py /app
RUN chmod +x /app/shadowsocks_manager.py
COPY entrypoint.sh /app
RUN chmod +x /app/entrypoint.sh
ENV PATH="$PATH:/app"
ENTRYPOINT [ "./entrypoint.sh"]
