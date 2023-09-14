##shoal-server-rabbitmq Dockerfile

This Dockerfile triggers an autobuild on the Docker Hub Registery for an image containing the shoal-server-rabbitmq component of the [Shoal](https://github.com/hep-gc/shoal) web cache publishing system. For details of how shoal works checkout the [Shoal GitHib Page](https://github.com/hep-gc/shoal).

##Configuration

Edit the configuration file /etc/shoal/shoal_server.conf

##Running Container 

Expose port 80 - HTTP, 5671 & 5672 - AMQP with and without TLS

##DockerHub

All docker images are autobuilt on DockerHub from a CentOS 6 base. See the  [uvichep docker page](https://registry.hub.docker.com/repos/uvichep/).


##GitHub

The shoal-server-rabbitmq Docker image is autobuilt from the [shoal-server-rabbitmq Dockerfile](https://github.com/hep-gc/docker-shoal/blob/master/shoal-server-rabbitmq/Dockerfile) on GitHub.
