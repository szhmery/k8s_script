#!/bin/bash
 

echo "docker ps"
PODS=`docker ps -a | grep Exited`
PODS_ID=`docker ps -a | grep Exited | awk '{print $1}' > pods.txt`
echo "we will delete $PODS" 
for x in ` awk '{print $1}' pods.txt `  
{  
	echo "docker rm $x"  
	docker rm $x
}
#for i in `$(docker ps -a | grep Exited | awk '{print $1}')`;
#do
#	echo $i
#	echo `$(docker rm $i)`
#done


