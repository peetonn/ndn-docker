#!/bin/bash

echo "Starting ndnrtc-client with command-line arguments:"
echo "\tconfig file: $CONFIG_FILE"
echo "\tsigning identity: $SIGNING_IDENTITY"
echo "\tpolicy file: $POLICY_FILE"
echo "\truntime: $RUNTIME"
echo "\tinstance name: $INSTANCE_NAME"
echo "\tstatistics sampling: $STAT_SAMPLING"

./ndnrtc-client -c ${CONFIG_FILE} -s ${SIGNING_IDENTITY} -p ${POLICY_FILE} -t ${RUNTIME} -i ${INSTANCE_NAME} -n ${STAT_SAMPLING} -v