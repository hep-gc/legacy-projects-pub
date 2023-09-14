#!/bin/bash

for i in `seq 1 12`;
do
#echo "java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion$i/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion$i.txt";
( java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/mnt/ramdisk/045Gfile.dat of=/bulk/fusion$i/045Gfile.dat bs=10M count=10240 rformat=M > /root/results/test2/fusion$i.txt & );
done

