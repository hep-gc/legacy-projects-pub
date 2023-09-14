<b> Containerized Cloud Scheduler </b>

The Dockerfile and other necessary files for creating a containerized version of cloud_scheduler. Runs on CentOS 7, with systemd enabled and neccesary requirements already installed.
Includes configuration files for condor and cloud_scheduler

To use, pull the image from docker hub

docker pull twgibbons/centos-cloud:cloud_scheduler

For information on how to run it with an external cloud see external_cloud

For running this container with a internally created devstack cloud, see containerized-cloud
