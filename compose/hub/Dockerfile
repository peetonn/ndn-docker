FROM peetonn/ndn-docker:latest
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
ENV ENTRYPOINT=""

WORKDIR /
CMD bootstrap.sh -b $NFD_BACKGROUND -r $REGISTER -e "${ENTRYPOINT}"