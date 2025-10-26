FROM debian:13

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:${PATH}

RUN apt update
RUN apt install -y openjdk-21-jdk
RUN apt install -y curl

RUN curl -o /home/karaf.tar.gz https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.22.0/karaf-0.22.0.tar.gz
RUN tar xzf /home/karaf.tar.gz --strip-components=1 -C /home/

EXPOSE 6633 6653 8080 8181

CMD ["bin/bash"]
