<b>Containerized Devstack </b>

For the ready to use docker image

docker pull twgibbons/centos-cloud:devstack

Devstack will then need to be restacked, the neccessary dependancies are already present, so run with OFFLINE=True to speed up the process. The stack file exists in /opt/stack/devstack, as well as the conf file. When stopping the container make sure to first run unstack.sh or everything will not be properly shutdown by docker and can cause conflict problems for future stack instances.

For an example of using this image with a containerized cloud scheduler for a testing enviroment, see condor_cloud/containerized-cloud

This image is built using a CentOS 7 base, with systemd enabled. The Dockerfile for this image exists in condor_cloud/c7_base. To build this image you will need to first built the c7_base, and then use that as the base image for devstack.
