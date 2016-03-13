#!/bin/bash

n=`basename $1`;

/data/Dropbox/programs/4auto/parses $1 /tmp/$n all;
cut -d ';' -f 2-3 /tmp/${n}_part_00 > $2; 
