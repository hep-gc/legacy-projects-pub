#!/bin/bash


mkfs.xfs -f -L fusion1 /dev/fioa
mkfs.xfs -f -L fusion2 /dev/fiob
mkfs.xfs -f -L fusion3 /dev/fioc
mkfs.xfs -f -L fusion4 /dev/fiod
mkfs.xfs -f -L fusion5 /dev/fioe
mkfs.xfs -f -L fusion6 /dev/fiof
mkfs.xfs -f -L fusion7 /dev/fiog
mkfs.xfs -f -L fusion8 /dev/fioh
mkfs.xfs -f -L fusion9 /dev/fioi
mkfs.xfs -f -L fusion10 /dev/fioj
mkfs.xfs -f -L fusion11 /dev/fiok
mkfs.xfs -f -L fusion12 /dev/fiol


for i in `seq 1 12`;
do
    mount -t xfs -L fusion$i /bulk/fusion$i;
done

#mount -t xfs -L slot1 /bulk/ssd1
#mount -t xfs -L slot2 /bulk/ssd2
#mount -t xfs -L slot3 /bulk/ssd3
#mount -t xfs -L slot4 /bulk/ssd4
#mount -t xfs -L slot5 /bulk/ssd5
#mount -t xfs -L slot6 /bulk/ssd6
#mount -t xfs -L slot7 /bulk/ssd7

#mount -t xfs -L slot8 /bulk/ssd8
#mount -t xfs -L slot9 /bulk/ssd9
#mount -t xfs -L slot10 /bulk/ssd10
#mount -t xfs -L slot11 /bulk/ssd11
#mount -t xfs -L slot12 /bulk/ssd12
#mount -t xfs -L slot13 /bulk/ssd13
#mount -t xfs -L slot14 /bulk/ssd14
#mount -t xfs -L slot15 /bulk/ssd15
