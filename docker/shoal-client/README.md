# shoal-client Dockerfile

This Dockerfile triggers an autobuild on the Docker Hub Registery for an image containing the shoal-client component of the [Shoal](https://github.com/hep-gc/shoal) web cache publishing system. For details of how shoal works checkout the [Shoal GitHib Page](https://github.com/hep-gc/shoal).

##Configuration

Edit the configuration file /etc/shoal/shoal-client.conf

##Commands

shoal-client --dump to show what would have been written to the CVMFS config file

##DockerHub

All docker images are autobuilt on DockerHub from a CentOS 6 base. See the  [uvichep docker page](https://registry.hub.docker.com/repos/uvichep/).


##GitHub

The shoal-client Docker image is autobuilt from the [shoal-client Dockerfile](https://github.com/hep-gc/docker-shoal/blob/master/shoal-client/Dockerfile) on GitHub.

