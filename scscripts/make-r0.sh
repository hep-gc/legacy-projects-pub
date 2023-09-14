#!/bin/bash
#MegaCli -CfgLdDel -L1 -a0

#MegaCli -CfgLdAdd -r0 [252:1] WT NORA DIRECT -strpsz 1024 -a0
for i in `seq 1 7`;
do
    MegaCli -CfgLdAdd -r0 [252:$i] WT NORA DIRECT -strpsz 1024 -a0;
done

#MegaCli -CfgLdAdd -r0 [62:0] WT NORA DIRECT -strpsz 64 -a1
for i in `seq 0 7`;
do
    MegaCli -CfgLdAdd -r0 [62:$i] WT NORA DIRECT -strpsz 64 -a1;
done



mkfs.xfs -f -L slot1 /dev/sdb
mkfs.xfs -f -L slot2 /dev/sdc
mkfs.xfs -f -L slot3 /dev/sdd
mkfs.xfs -f -L slot4 /dev/sde
mkfs.xfs -f -L slot5 /dev/sdf
mkfs.xfs -f -L slot6 /dev/sdg
mkfs.xfs -f -L slot7 /dev/sdh

mkfs.xfs -f -L slot8 /dev/sdi
mkfs.xfs -f -L slot9 /dev/sdj
mkfs.xfs -f -L slot10 /dev/sdk
mkfs.xfs -f -L slot11 /dev/sdl
mkfs.xfs -f -L slot12 /dev/sdm
mkfs.xfs -f -L slot13 /dev/sdn
mkfs.xfs -f -L slot14 /dev/sdo
mkfs.xfs -f -L slot15 /dev/sdp


for i in `seq 1 15`;
do
    mount -t xfs -L slot$i /bulk/ssd$i;
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
