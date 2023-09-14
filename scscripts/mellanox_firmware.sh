#!/bin/bash
# NEVER run this. Reference only

cd mft-2.7.1-7
./install.sh 
cd ..
mst start
ethtool -i ethmlx
flint -d /dev/mst/mt4099_pci_cr0 query
flint -d /dev/mst/mt4099_pci_cr0  -i fw-ConnectX3-rel-2_11_0500-MCX313A-BCB_A4-A5-Flexboot-3.4.000.bin burn
