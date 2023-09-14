# shoal-agent Dockerfile

This Dockerfile triggers an autobuild on the Docker Hub Registery for an image containing the shoal-agent component of the [Shoal](https://github.com/hep-gc/shoal) web cache publishing system. For details of how shoal works checkout the [Shoal GitHib Page](https://github.com/hep-gc/shoal).

##Run Docker Image

docker run -d uvichep/shoal-agent {IP address of AMQP Server} {external IP address of host}

##Configuration

Edit the configuration file /etc/shoal/shoal_agent.conf

##Commands

service shoal-agent [start | stop | reload | status | force restart]


##DockerHub

All docker images are autobuilt on DockerHub from a CentOS 6 base. See the  [uvichep docker page](https://registry.hub.docker.com/repos/uvichep/).


##GitHub

The shoal-agent Docker image is autobuilt from the [shoal-agent Dockerfile](https://github.com/hep-gc/docker-shoal/blob/master/shoal-agent/Dockerfile) on GitHub.
