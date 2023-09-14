#!/bin/bash

fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd1/  -fl /bulk/ssd1/smallfiles.txt &> /root/log/fdt1.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd2/  -fl /bulk/ssd2/smallfiles.txt &> /root/log/fdt2.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd3/  -fl /bulk/ssd3/smallfiles.txt &> /root/log/fdt3.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd4/  -fl /bulk/ssd4/smallfiles.txt &> /root/log/fdt4.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd5/  -fl /bulk/ssd5/smallfiles.txt &> /root/log/fdt5.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd6/  -fl /bulk/ssd6/smallfiles.txt &> /root/log/fdt6.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd7/  /bulk/ssd7/ &> /root/log/fdt7.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd8/  /bulk/ssd8/ &> /root/log/fdt8.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd9/  /bulk/ssd9/ &> /root/log/fdt9.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd10/  /bulk/ssd10/ &> /root/log/fdt10.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd11/  /bulk/ssd11/ &> /root/log/fdt11.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd12/  /bulk/ssd12/ & > /root/log/fdt12.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /bulk/ssd13/  /bulk/ssd13/ &> /root/log/fdt13.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /bulk/ssd14/  /bulk/ssd14/ &> /root/log/fdt14.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /bulk/ssd15/  /bulk/ssd15/ &> /root/log/fdt15.log &
