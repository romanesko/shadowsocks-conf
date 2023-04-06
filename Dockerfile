FROM ubuntu:22.04
RUN apt-get update -y 
RUN apt-get install shadowsocks-libev -y
RUN apt-get install python3 -y
RUN apt-get install uuid-runtime -y
RUN apt-get install python3-pip -y
RUN pip3 install redis
WORKDIR /app
COPY shadowsocks_manager.py /app
RUN chmod +x /app/shadowsocks_manager.py
COPY entrypoint.sh /app
COPY worker.py /app
RUN chmod +x /app/entrypoint.sh
ENV PATH="$PATH:/app"
ENTRYPOINT [ "./entrypoint.sh"]
