FROM centos:7

USER root

RUN yum -y install sudo virt-install openssh wget unzip gcc python-devel net-tools less libvirt qemu-kvm libvirt-devel mkisofs

WORKDIR /jobs
ADD . /jobs

ADD systemctl.py /usr/bin/systemctl
RUN chmod +x /usr/bin/systemctl

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install --upgrade -r requirements.txt

#condor installation
RUN cd /etc/yum.repos.d && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor && rpm --import RPM-GPG-KEY-HTCondor
RUN yum -y install condor
RUN cp condor_config.local /etc/condor/

#setup cs conf for pipeline
RUN mkdir /etc/cloudscheduler && cp /jobs/cloud_resources.conf /etc/cloudscheduler && cp /jobs/cloud_scheduler.conf /etc/cloudscheduler && cp /jobs/default.yaml /etc/cloudscheduler && mkdir /usr/local/share/cloud-scheduler && cp /jobs/defaults.cfg /usr/local/share/cloud-scheduler
RUN cd /srv && mkdir userdata && cp /jobs/benchmark.yaml /srv/userdata/ && cp /jobs/verifycs.yaml /srv/userdata/

#qemu conf
RUN cp qemu.conf /etc/libvirt/

#configure ssh keys
RUN ssh-keygen -q -f /root/.ssh/id_rsa -N "" && python generate-keyfile.py && cp auth-key.yaml /etc/cloudscheduler/auth-key.yaml 

#make the directories for images
RUN mkdir -p /jobs/instances/base && useradd hep && chmod +x startup.sh

CMD ./startup.sh
