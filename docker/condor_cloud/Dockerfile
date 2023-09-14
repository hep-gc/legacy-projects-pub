FROM centos7_sysd

USER root

RUN yum -y install wget && yum -y install unzip && yum -y install gcc && yum -y install python-devel && yum -y install net-tools && yum -y install less

WORKDIR /jobs
ADD . /jobs

#install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install --upgrade -r requirements.txt

#condor installation
RUN cd /etc/yum.repos.d && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor && rpm --import RPM-GPG-KEY-HTCondor
RUN yum -y install condor
RUN cp condor_config.local /etc/condor/ && systemctl enable condor

#install cloudscheduler
RUN wget https://github.com/hep-gc/cloud-scheduler/archive/dev.zip && unzip dev.zip && cd cloud-scheduler-dev && python setup.py install
RUN cp /jobs/cloud-scheduler-dev/scripts/cloud_scheduler.init.d /etc/init.d/cloud_scheduler && cp /jobs/cloud-scheduler-dev/scripts/cloud_scheduler.sysconf /etc/sysconfig/cloud_scheduler && mkdir /etc/cloudscheduler && cp /jobs/cloud-scheduler-dev/cloud_resources.conf /etc/cloudscheduler && cp /jobs/cloud_scheduler.conf /etc/cloudscheduler && cp /jobs/cloud-scheduler-dev/default.yaml /etc/cloudscheduler
RUN mkdir /srv/userdata && cp benchmark.yaml /srv/userdata/ && cp verifycs.yaml /srv/userdata/
