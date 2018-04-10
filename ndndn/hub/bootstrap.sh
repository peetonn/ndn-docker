#!/bin/bash

echo "" > $ENTRYPOINT_LOG
echo "" > $BOOTSTRAP_LOG

NS_RULE=10
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

function resolveHost() {
    ip=`host ${1} | awk '/has address/ { print $4 }'`
    echo $ip
}

function getTupleVal() {
    tuple=$1
    name=$2
    val=""

    idx=0
    for el in $tuple; do
        let idx=idx+1
        if [ "$idx" == $name ]; then
            val=$el
            break
        fi
    done;

    echo $val
}

NS_RULE=1
function shapeNetwork() {
    # https://stackoverflow.com/a/615757/846340
    # removing rules:
    # tc qdisc del dev eth0 handle ${handle}:${handle} root
    has_rule="no"
    handle=$NS_RULE
    lat=$NS_LATENCY
    loss=$NS_LOSS
    rate=$NS_BW
    target=$NS_TARGET

    runCmd "tc filter add dev eth0 protocol ip parent 1: prio ${NS_RULE} u32 match ip dst ${target} match ip dport 6363 0xffff flowid 1:${NS_RULE}"

    if [ ! "$lat" == "0" ]; then
        runCmd "tc qdisc add dev eth0 parent 1:${NS_RULE} handle ${NS_RULE}0: netem delay ${lat}ms"
        has_rule=yes
    fi

    if [ ! "$loss" == "0" ]; then
        if [ "$has_rule" == "no" ]; then
            runCmd "tc qdisc add dev eth0 parent 1:${NS_RULE} handle ${NS_RULE}0: netem loss ${loss}%"
        else
            runCmd "tc qdisc change dev eth0 parent 1:${NS_RULE} handle ${NS_RULE}0: netem loss ${loss}%"
        fi
        has_rule=yes
    fi

    if [ ! "$rate" == "0" ]; then
        if [ "$has_rule" == "no" ]; then
            runCmd "tc qdisc add dev eth0 parent 1:${NS_RULE} handle ${NS_RULE}0: netem rate ${rate}kbit"
        else
            runCmd "tc qdisc change dev eth0 parent 1:${NS_RULE} handle ${NS_RULE}0: netem rate ${rate}kbit"
        fi
    fi

    let NS_RULE=NS_RULE+1
}

################################################################################
## NFD STARTUP
log "Bootstrapping."
log "Register: $register"
log "Execute: $execute"
log "NFD background: $nfdBackground"

log "Starting NFD..."
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

################################################################################
## NETWORK SHAPING
## https://serverfault.com/questions/906458/network-shaping-using-tc-netem-doesnt-seem-to-work/906499#906499
if [[ ! -z $NETWORK_SHAPE ]]; then
    runCmd "tc qdisc add dev eth0 root handle 1: prio bands 8"

    OLDIFS=$IFS
    for p in $NETWORK_SHAPE; do IFS=':';
        set -- $p;
        IFS=$OLDIFS;

        NS_TARGET=`resolveHost "$1"`
        shapeTuple=${2//[-]/" "}
        NS_LATENCY=`getTupleVal "$shapeTuple" 1`
        NS_LOSS=`getTupleVal "$shapeTuple" 2`
        NS_BW=`getTupleVal "$shapeTuple" 3`

        if [[ ! -z $NS_TARGET ]]; then
            log "$1 has address $NS_TARGET"
            shapeNetwork
        else
            log "Couldn't resolve hostname $1"
        fi
    done; IFS=$OLDIFS

    runCmd "tc filter add dev eth0 protocol all parent 1: prio 8 u32 match ip dst 0.0.0.0/0 flowid 1:8"
    runCmd "tc filter add dev eth0 protocol all parent 1: prio 8 u32 match ip protocol 1 0xff flowid 1:8"
    runCmd "tc qdisc add dev eth0 parent 1:8 handle 999: sfq"
fi

################################################################################
## ENTRYPOINT
if [[ ! -z "$execute" ]]; then
    eval "$execute"  >> $ENTRYPOINT_LOG 2>&1
fi

################################################################################
## NO ENTRY POINT
if [ "$nfdBackground" == "no" ]; then
    eval "tail -f ${LOG_FILE}" >> $ENTRYPOINT_LOG 2>&1
fi