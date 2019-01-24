#!/bin/bash
 
echo "Start to get usscheduler IP!"
echo "kubectl get pods -o wide | grep ussche"
USSCHEDULER_IP=`kubectl get pods -o wide | grep ussche | awk '{print $6}'`
echo "usscheduler IP address is  $USSCHEDULER_IP" 

curl -X PUT -d 'ON'   --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/bwr
echo "open debug bwr"
curl -X PUT -d 'ON'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/rtt
echo "open debug rtt"
curl -X PUT -d 'ON'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/grant
echo "open debug grant"
curl -X PUT -d 'ON'   --noproxy  $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/api
echo "open debug api"
curl -X PUT -d 'DEBUG' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/level
echo "debug level: DEBUG"
curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/TELEMETRY 
echo "TELEMETRY debug level: ERROR"
curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/UMP
echo "UMP debug level: ERROR"
curl -X PUT -d 'ERROR' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/MAPBD
echo "MAPBD debug level: ERROR"
curl -X PUT -d 'DEBUG' --noproxy $USSCHEDULER_IP $USSCHEDULER_IP:8080/debug/sublevel/KAFKA
echo "KAFKA debug level: DEBUG"

echo "Open usscheduler debug finished!"
