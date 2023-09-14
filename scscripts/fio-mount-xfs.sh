#!/bin/bash

for i in `seq 1 12`;
do
    mount -t xfs -o nobarrier,noatime -L fusion$i /bulk/fusion$i;
done


