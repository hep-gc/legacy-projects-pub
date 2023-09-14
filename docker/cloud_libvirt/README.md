## Cloud Type LocalHost

A fully container cloudscheduler environment which simulates a cloud using libvirt. This allows cloudscheduler to launch VM's
inside of a container and run condor jobs without access to an external cloud. 

### To Use:

Launch a cloud-libvrt container with the --privileged flag. This is needed to launch local VM's using libvirt. Then add your 
localhost to the cloud resources file and start cloudscheduler with /etc/init.d/cloudscheduler. For an example cloud_resources file
in the container look at /jobs/cloud_resources.conf
