FROM debian:13
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:${PATH}

# Instalar java
RUN apt update && \
    apt install -y openjdk-21-jdk curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar ODL
RUN curl -o /tmp/karaf.tar.gz https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.22.0/karaf-0.22.0.tar.gz && \
    tar xzf /tmp/karaf.tar.gz --strip-components=1 -C /home/ && \
    rm /tmp/karaf.tar.gz

WORKDIR /home

EXPOSE 6633 6653 8080 8181

CMD ["./bin/karaf", "server"]

# Entry the container: ssh -p 8101 karaf@[conainer_ip]
