#!/bin/sh

/usr/bin/systemctl start libvirtd

/usr/bin/systemctl start condor

while true; do sleep 1; done 
