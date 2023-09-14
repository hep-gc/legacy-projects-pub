# shoal-server Dockerfile

This Dockerfile triggers an autobuild on the Docker Hub Registery for an image containing the shoal-server component of the [Shoal](https://github.com/hep-gc/shoal) web cache publishing system. For details of how shoal works checkout the [Shoal GitHib Page](https://github.com/hep-gc/shoal).

##Configuration

Edit the configuration file /etc/shoal/shoal_server.conf

The RabbitMQ server can be installed by running yum install rabbitmq Alternately there is a Docker Container with RabbitMQ already installed uvichep/shoal-server-rabbitmq

##Running Container 

Expose port 80 - HTTP, 5671 & 5672 - AMQP with and without TLS

##DockerHub

All docker images are autobuilt on DockerHub from a CentOS 6 base. See the  [uvichep docker page](https://registry.hub.docker.com/repos/uvichep/).


##GitHub

The shoal-server Docker image is autobuilt from the [shoal-server Dockerfile](https://github.com/hep-gc/docker-shoal/blob/master/shoal-server/Dockerfile) on GitHub.
