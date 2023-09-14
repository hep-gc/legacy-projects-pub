FROM centos:7

USER root

RUN yum -y install virt-install && yum install -y openssh && yum -y install wget && yum -y install unzip && yum -y install gcc && yum -y install python-devel && yum -y install net-tools && yum -y install less && yum -y install libvirt && yum -y install qemu-kvm && yum -y install libvirt-devel && yum -y install mkisofs && yum -y install emacs && yum -y install sudo && yum -y install mlocate && yum -y install git

WORKDIR /jobs
ADD . /jobs

ADD systemctl.py /usr/bin/systemctl
RUN chmod +x /usr/bin/systemctl

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install --upgrade -vvv --ignore-installed -r requirements.txt

#condor installation
RUN cd /etc/yum.repos.d && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor && rpm --import RPM-GPG-KEY-HTCondor
RUN yum -y install condor-all fetch-crl globus-proxy-utils
RUN systemctl enable condor

COPY condor_config.local /etc/condor/
COPY default_request defrag gsi ports scaling system_hold /etc/condor/config.d/

# Add NETWORK_INTERFACE line in condor_config.local with the current host's IP address 
RUN public_ip=$(curl -s http://whatismyip.akamai.com/) && sed -i '/^NETWORK_INTERFACE =/ d' /etc/condor/condor_config.local && LINE="NETWORK_INTERFACE = $public_ip"; FILE=/etc/condor/condor_config.local; grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"

# make the condor user accessible
RUN chsh -s /bin/bash condor

# create a log directory for the condor user
RUN mkdir /var/lib/condor/logs && chown condor /var/lib/condor && chown condor /var/lib/condor/logs

# Run the startup.sh script
RUN chmod +x startup.sh
CMD ./startup.sh
