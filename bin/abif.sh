#!/bin/bash

if(( $# != 1 )); then
	echo " usage : $0 <auto.log>";
	exit -1;
fi

bifs="HB LP";

while true; do
	for bif in $bifs; do
		grep -F "$bif" $1;
	done
	sleep 5;
	echo '--------------------------------------'
done
