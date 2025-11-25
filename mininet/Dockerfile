FROM iwaseyusuke/mininet

RUN apt update && \
    apt install -y hping3 tshark python3-numpy && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /home/mininet

WORKDIR /home/mininet

CMD ["./bin/bash", "server"]
