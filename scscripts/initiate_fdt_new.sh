#!/bin/bash

fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd1/   /bulk/ssd1/100Gfile.dat &> /root/log/fdt1.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd2/   /bulk/ssd2/100Gfile.dat &> /root/log/fdt2.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd3/   /bulk/ssd3/100Gfile.dat &> /root/log/fdt3.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd4/   /bulk/ssd4/100Gfile.dat &> /root/log/fdt4.log &
fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd5/   /bulk/ssd5/100Gfile.dat &> /root/log/fdt5.log &

fdtClient -c 10.20.3.245  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd6/   /bulk/ssd6/100Gfile.dat &> /root/log/fdt1.log &
fdtClient -c 10.20.3.245  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd7/   /bulk/ssd7/100Gfile.dat &> /root/log/fdt2.log &
fdtClient -c 10.20.3.245  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd8/   /bulk/ssd8/100Gfile.dat &> /root/log/fdt3.log &
fdtClient -c 10.20.3.245  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd9/   /bulk/ssd9/100Gfile.dat &> /root/log/fdt4.log &
fdtClient -c 10.20.3.245  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd10/   /bulk/ssd10/100Gfile.dat &> /root/log/fdt5.log &

fdtClient -c 10.20.3.246  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd11/   /bulk/ssd11/100Gfile.dat &> /root/log/fdt1.log &
fdtClient -c 10.20.3.246  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd12/   /bulk/ssd12/100Gfile.dat &> /root/log/fdt2.log &
fdtClient -c 10.20.3.246  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd13/   /bulk/ssd12/100Gfile.dat &> /root/log/fdt3.log &
fdtClient -c 10.20.3.246  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd14/   /bulk/ssd14/100Gfile.dat &> /root/log/fdt4.log &

#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd7/  /bulk/ssd7/ &> /root/log/fdt7.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd8/  /bulk/ssd8/ &> /root/log/fdt8.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd9/  /bulk/ssd9/ &> /root/log/fdt9.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd10/  /bulk/ssd10/ &> /root/log/fdt10.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd11/  /bulk/ssd11/ &> /root/log/fdt11.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /lustre/ddn12k/wan-1/ssd12/  /bulk/ssd12/ & > /root/log/fdt12.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /bulk/ssd13/  /bulk/ssd13/ &> /root/log/fdt13.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /bulk/ssd14/  /bulk/ssd14/ &> /root/log/fdt14.log &
#fdtClient -c 10.20.3.244  -rCount 8 -d  /bulk/ssd15/  /bulk/ssd15/ &> /root/log/fdt15.log &
