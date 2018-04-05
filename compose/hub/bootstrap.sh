#!/bin/bash

echo "" > $BOOTSTRAP_LOG

NFD_START_FG_CMD="nfd > ${LOG_FILE} 2>&1"
NFD_START_BG_CMD="nfd > ${LOG_FILE} 2>&1 &"
nfdBackground="yes"
register=$REGISTER
execute=$ENTRYPOINT

function log {
    echo $1 >> $BOOTSTRAP_LOG
    echo $1
}

while getopts ":r:e:b:" opt; do
  case $opt in
    r) register="$OPTARG"
    ;;
    e) execute="$OPTARG"
    ;;
    b) nfdBackground="$OPTARG"
    ;;
    \?) log "Invalid option -$OPTARG" >&2
    ;;
  esac
done

function runCmd() {
    log "$1"
    eval $1 >> $BOOTSTRAP_LOG 2>&1
}

function registerPrefix() {
    host=$1
    route=$2

    faceId=`nfdc face create udp://$host | sed "s/^face-created id=\([0-9][0-9]*\) .*$/\1/g"`
    log "registering $route towards $host (face id $faceId)"
    runCmd "nfdc route add $route $faceId"
}

function startNfd() {
    runCmd "$NFD_START_BG_CMD"
}

log "Bootstrapping."
log "Register: $register"
log "Execute: $execute"
log "NFD background: $nfdBackground"

log "staring NFD..."
startNfd
sleep 2
log "NFD started"

if [[ ! -z $register ]]; then
    OLDIFS=$IFS
    for p in $register; do IFS=':';
        set -- $p;
        IFS=$OLDIFS;
        registerPrefix "$1" "$2"
    done; IFS=$OLDIFS
fi

if [[ ! -z "$execute" ]]; then
    runCmd "$execute"
fi

if [ "$nfdBackground" == "no" ]; then
    runCmd "tail -f ${LOG_FILE}"
fi

