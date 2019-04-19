#!/bin/bash

readonly PROGNAME=$(basename $0)
readonly PROGDIR=$(readlink -m $(dirname $0))
readonly ARGS="$@"

cmdline() {
    local arg=
    for arg
    do
        local delim=""
        case "$arg" in
            --enable)               args="${args}-e ";;
            --disable)              args="${args}-d ";;
            *) [[ "${arg:0:1}" == "-" ]] || delim="\""
                args="${args}${delim}${arg}${delim} ";;
        esac
    done
 eval set -- $args

 while getopts "hde" OPTION
    do
         case $OPTION in
         h)
             usage
             exit 0
             ;;
         e)
             readonly OPERATION="enable"
             ;;

         d)
             readonly OPERATION="disable"
             ;;
         \?)
             echo "Invalid option: $OPTARG"
             usage
             exit 0
             ;;

        esac
    done
    shift $((OPTIND -1))
}

usage() {
    cat <<- EOF

  usage: $PROGNAME [-h]
  usage: $PROGNAME OPTIONS

  This script will help to enable or disable cmts-rt-usscheduler debug log.

  -h --help                        show this help

  OPTIONS:
     -e --enable                 enable debug
     -d --disable                disable debug


  Examples:
     ./$PROGNAME -e
     ./$PROGNAME -d

EOF
}

main() {
    local rc=0
    cmdline ${ARGS}

    echo "Start to get usscheduler IP!"
    echo "kubectl get pods -o wide | grep ussche"
    USSCHEDULER_IP=`kubectl get pods -o wide | grep ussche | awk '{print $6}'`
    echo "usscheduler IP address is  $USSCHEDULER_IP"

    # enable debug for bwr
    if [ -n "$OPERATION" ]
    then
    if [ $OPERATION == "enable" ]
        then

        curl -X PUT -d 'ON'   --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/bwr
        echo "open debug bwr"
        curl -X PUT -d 'ON'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/rtt
        echo "open debug rtt"
        curl -X PUT -d 'OFF'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/grant
        echo "disable debug grant"
        curl -X PUT -d 'ON'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/api
        echo "open debug api"
        #curl -X PUT -d 'ON'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/lld
        #echo "enable debug lld"
        curl -X PUT -d 'ON'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/error
        echo "open debug error"
        curl -X PUT -d 'DEBUG' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/level
        echo "debug level: DEBUG"
        curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/TELEMETRY
        echo "TELEMETRY debug level: ERROR"
        curl -X PUT -d 'DEBUG' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/UMP
        echo "UMP debug level: DEBUG"
        curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/MAPBD
        echo "MAPBD debug level: ERROR"
        curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/KAFKA
        echo "KAFKA debug level: ERROR"

        echo "Open usscheduler debug finished!"

    fi


    if [ $OPERATION == "disable" ]
        then

        curl -X PUT -d 'OFF'   --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/bwr
        echo "disable debug bwr"
        curl -X PUT -d 'OFF'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/rtt
        echo "disable debug rtt"
        curl -X PUT -d 'OFF'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/grant
        echo "disable debug grant"
        curl -X PUT -d 'OFF'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/api
        echo "disable debug api"
        curl -X PUT -d 'ON'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/error
        echo "enable debug error"
        curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/level
        echo "debug level: ERROR"
        curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/TELEMETRY
        echo "TELEMETRY debug level: ERROR"
        curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/UMP
        echo "UMP debug level: ERROR"
        curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/MAPBD
        echo "MAPBD debug level: ERROR"
        curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/KAFKA
        echo "KAFKA debug level: ERROR"

        echo "Disable usscheduler debug finished!"


    fi
  fi
  rc=$(($rc+$?))
  result=$?
  return $result
}

main
