FROM centos:7

USER root

RUN yum -y install virt-install && yum install -y openssh && yum -y install wget && yum -y install unzip && yum -y install gcc && yum -y install python-devel && yum -y install net-tools && yum -y install less && yum -y install libvirt && yum -y install qemu-kvm && yum -y install libvirt-devel && yum -y install mkisofs && yum -y install emacs && yum -y install sudo && yum -y install mlocate && yum -y install git && yum -y install libguestfs-tools

WORKDIR /jobs
ADD . /jobs

ADD systemctl.py /usr/bin/systemctl
RUN chmod +x /usr/bin/systemctl

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install --upgrade -vvv --ignore-installed -r requirements.txt

# Expose needed ports
EXPOSE 947 9618
EXPOSE 40000-40500

#condor installation
RUN cd /etc/yum.repos.d && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor && rpm --import RPM-GPG-KEY-HTCondor
RUN yum -y install condor
RUN cp condor_config.local /etc/condor/

#install cloudscheduler
RUN wget https://github.com/hep-gc/cloud-scheduler/archive/dev.zip && unzip dev.zip && rm dev.zip
RUN cd cloud-scheduler-dev && python setup.py install

RUN cp /jobs/cloud-scheduler-dev/scripts/cloud_scheduler.init.d /etc/init.d/cloud_scheduler && cp /jobs/cloud-scheduler-dev/scripts/cloud_scheduler.sysconf /etc/sysconfig/cloud_scheduler && mkdir /etc/cloudscheduler && cp /jobs/cloud_resources.conf /etc/cloudscheduler && cp /jobs/cloud_scheduler.conf /etc/cloudscheduler && cp /jobs/default.yaml /etc/cloudscheduler && cp /jobs/cloud-scheduler-dev/cloudscheduler/defaults.cfg /etc/cloudscheduler

RUN cd /srv && mkdir userdata && cp /jobs/benchmark.yaml /srv/userdata/ && cp /jobs/verifycs.yaml /srv/userdata/

#configure ssh keys
RUN ssh-keygen -q -f /root/.ssh/id_rsa -N "" && python generate-keyfile.py && cp auth-key.yaml /etc/cloudscheduler/auth-key.yaml

# copy the custom qemu.conf file to /etc/libvirt/ 
RUN cp qemu.conf /etc/libvirt/qemu.conf

#make the directories for local images
RUN mkdir -p /jobs/instances/base 

# make the condor user accessible
RUN chsh -s /bin/bash condor

# create a log directory for the condor user
RUN mkdir /var/lib/condor/logs && chown condor /var/lib/condor && chown condor /var/lib/condor/logs

# Run the startup.sh script
RUN chmod +x startup.sh
CMD ./startup.sh
