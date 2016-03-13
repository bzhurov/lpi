#!/bin/bash
prefix=$RANDOM;
for f in $@; do
	n=`basename $f`;
	/data/Dropbox/programs/4auto/parses.sh $f /tmp/0_0_${prefix}__${n};
done

/data/Dropbox/programs/scripts/xpaste /tmp/0_0_${prefix}__*;
	
