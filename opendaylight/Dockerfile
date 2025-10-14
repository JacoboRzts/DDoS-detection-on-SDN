FROM debian:13

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:${PATH}

RUN apt update
RUN apt install -y openjdk-21-jdk

COPY karaf-0.22.0.tar.gz /home/
RUN tar xzf /home/karaf-0.22.0.tar.gz --strip-components=1 -C /home/

EXPOSE 6633 6653 8080 8181

CMD ["bin/bash"]
