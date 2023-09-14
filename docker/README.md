#Shoal Docker Repository

This repository contains the Docker files for packaging the various components of the [Shoal](https://github.com/hep-gc/shoal)
web cache publishing system. For details of how shoal works checkout the [Shoal GitHib Page](https://github.com/hep-gc/shoal)


## Available Dockers

[**shoal-server**](shoal-server) maintains the list of running squids. It uses RabbitMQ to handle incoming AMQP messages from 
squid servers. It provides a REST interface for programatically retrieving a json formatted ordered list of squids.
It also provides a web interface for viewing the list.

[**shoal-agent**](shoal-agent) runs on squid servers and publishes the load and IP of the squid server to the shoal-server using 
a json formatted AMQP message at regular intervals. This agent is designed to be trivially installed in a
few seconds with python's pip tool.

[**shoal-client**](shoal-client) is a reference client that can be used to contact the REST interface of the shoal-server.

[**condor_cloud**](condor_cloud) is a fully contained cloud scheduler environment which can be configured to connect to external cloud for running condor jobs.

[**devstack**](devstack) is a test container which runs a full Openstack instance using devstack.

[**cloud_libvirt**](cloud_libvirt) is a cloud scheduler environment which simulates an internal cloud using libvirt.

## DockerHub

All docker images are autobuilt on DockerHub from a CentOS 6 base. See the  [uvichep docker page](https://registry.hub.docker.com/repos/uvichep/).


