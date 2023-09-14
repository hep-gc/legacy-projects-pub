FROM local/c7-systemd

USER root

RUN yum -y install sudo && yum -y install git && yum -y install wget && yum -y install iproute

#add stack user and install devstack
RUN sudo useradd -s /bin/bash -d /opt/stack -m stack && echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
USER stack

WORKDIR /jobs
ADD . /jobs

RUN cd ~ && git clone https://git.openstack.org/openstack-dev/devstack && cd devstack && cp /jobs/local.conf .
