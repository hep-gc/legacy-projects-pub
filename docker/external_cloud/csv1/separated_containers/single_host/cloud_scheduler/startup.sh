#!/bin/sh

# start libvirtd
/usr/bin/systemctl start libvirtd

# start cloudscheduler, disable container-cloud, and enable cc-west cloud
/etc/init.d/cloud_scheduler start

# sleep for 2s while cloud scheduler starts
sleep 2

# disable the cc-west cloud and enable the otter-container cloud
cloud_admin -d cc-west-a
cloud_admin -e otter-container

while true; do sleep 1; done 
