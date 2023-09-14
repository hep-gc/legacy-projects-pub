#!/bin/bash

for i in `seq 1 10`;
do
    mount -t xfs -L fusion$i /bulk/fusion$i;
done


