FROM peetonn/ndnrtc:apiv3
LABEL maintainer "Peter Gusev <peter@remap.ucla.edu>"

COPY bootstrap.sh /usr/bin
RUN mkdir -p /configs /generated \
    && cp /usr/local/etc/ndn/nfd.conf /configs \
    && chmod +x /usr/bin/bootstrap.sh

ENV BOOTSTRAP_LOG=/generated/bootstrap.log
ENV ENTRYPOINT_LOG=/generated/entrypoint.log
ENV LOG_FILE=/generated/nfd.log
ENV NFD_BACKGROUND=yes
ENV REGISTER=""

COPY producer.cfg /configs/
COPY consumer.cfg /configs/
COPY run.sh /ndnrtc/cpp
RUN chmod +x /ndnrtc/cpp/run.sh

ENV CONFIG_FILE=/configs/producer.cfg
ENV ENTRYPOINT="./run.sh"

WORKDIR /ndnrtc/cpp
CMD bootstrap.sh -b $NFD_BACKGROUND -e "${ENTRYPOINT}" -r $REGISTER
