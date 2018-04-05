FROM ubuntu:16.04
LABEL maintainer "Peter Gusev <peter@remap.ucla.edu>"
ARG VERSION_CXX=master
ARG VERSION_NFD=master

# install tools
RUN  apt-get update \
     && apt-get install -y git build-essential

# install ndn-cxx and NFD dependencies
RUN apt-get install -y python libsqlite3-dev libboost-all-dev libssl-dev pkg-config libssl-dev libpcap-dev

# install ndn-cxx
RUN git clone https://github.com/named-data/ndn-cxx.git \
    && cd ndn-cxx \
    && git checkout $VERSION_CXX \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf ndn-cxx \
    && ldconfig

# install NFD
RUN git clone --recursive https://github.com/named-data/NFD \
    && cd NFD \
    && git checkout $VERSION_NFD \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf NFD

# install ndn-tools
RUN git clone --recursive https://github.com/named-data/ndn-tools.git \
    && cd ndn-tools \
    && ./waf configure \
    && ./waf \
    && ./waf install \
    && cd .. \
    && rm -Rf ndn-tools

# initial configuration
RUN cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf \
    && ndnsec-keygen /`whoami` | ndnsec-install-cert - \
    && mkdir -p /usr/local/etc/ndn/keys \
    && ndnsec-cert-dump -i /`whoami` > default.ndncert \
    && mv default.ndncert /usr/local/etc/ndn/keys/default.ndncert

RUN mkdir /share \
    && mkdir /logs

# cleanup
RUN apt autoremove \
    && apt-get remove -y git build-essential python pkg-config

EXPOSE 6363/tcp
EXPOSE 6363/udp

ENV CONFIG=/usr/local/etc/ndn/nfd.conf
ENV LOG_FILE=/logs/nfd.log

CMD /usr/local/bin/nfd -c $CONFIG > $LOG_FILE 2>&1