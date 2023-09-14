FROM centos:7

USER root

RUN yum -y install mariadb sudo virt-install openssh wget unzip gcc python-devel net-tools less libvirt qemu-kvm libvirt-devel mkisofs

WORKDIR /jobs
ADD . /jobs

ADD systemctl.py /usr/bin/systemctl
RUN chmod +x /usr/bin/systemctl

#install pip for python2
RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install pip==9.0.3 && pip install  -r requirements-python2.txt

#install python3
RUN yum-builddep -y python && curl -O https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz && tar xf Python-3.5.0.tgz && cd Python-3.5.0 && ./configure && make && make install
RUN pip3.5 install --upgrade pip && pip install --upgrade -r requirements-python3.txt

#condor installation
RUN cd /etc/yum.repos.d && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor && rpm --import RPM-GPG-KEY-HTCondor
RUN yum -y install condor
RUN cp condor_config.local /etc/condor/

#qemu conf
RUN cp qemu.conf /etc/libvirt/

#make the directories for images
RUN mkdir -p /jobs/instances/base && useradd hep && chmod +x startup.sh

CMD ./startup.sh
