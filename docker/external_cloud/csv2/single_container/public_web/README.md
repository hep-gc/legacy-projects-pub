# External Cloud in a Single Container Running csv2 with Public Web README

## Introduction

The files in this directory currently enable a **member of the UVic heprc group** to create a docker container on the htc-dev.heprc.uvic.ca VM which which runs csv2, and can submit and run condor jobs. Any user with the csv2_default password can access the public csv2 web page.

## Prerequisites

To successfully set up and run the container, and launch condor jobs from the container, the following pre-requisites are needed:

* Root access to the htc-dev.heprc.uvic.ca VM

* The csv2_default password to access the csv2 website at https://htc-dev.heprc.uvic.ca

* The following ports should be open to external IPv4 traffic on the htc-dev VM:

    * 80/tcp
    * 947/tcp
    * 3306/tcp
    * 443/tcp
    * 9618/tcp
    * 40000-40500/tcp

    Can double-check that these are currently open on htc-dev with

    ~~~~
    $ firewall-cmd --list-all | grep ports
    ~~~~

## Instructions

1. ssh onto the htc-dev computer:

    ~~~~
    $ ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 3121 [your_username]@htc-dev.heprc.uvic.ca
    ~~~~

2. Starting in the current (external_cloud/single_container) directory, use docker-compose to build and run the cloudscheduler container

    ~~~~
    $ docker-compose up&
    ~~~~
    
3. Run ansible to set up csv2 on the running container

    ~~~~
    $ ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 3121 [your_username]@elephant06.heprc.uvic.ca
    ~~~~

    clone the ansible-systems and Inventory directories to the same location on elephant06. Eg. 

    ~~~~
    $ mkdir Git
    $ cd Git
    $ git clone https://github.com/hep-gc/Inventory
    [enter git heprc credentials]
    $ git clone https://github.com/hep-gc/ansible-systems
    [enter git heprc credentials]
    ~~~~

    open the htc-dev-vars.yaml file in ansible-systems/heprc/staticvms/vars. Eg.

    ~~~~
    emacs /home/danikam1/Git/ansible-systems/heprc/staticvms/varsh/htc-dev-vars.yaml
    ~~~~
    
    
    Make sure the 'container' variable is set to True in htc-dev-vars.yaml, 'local_web' is set to False, and running_condor is set to True:
    
    ~~~~
    container: True
    local_web: False
    running_condor: True
    ~~~~

    Run ansible on the docker container running on htc-dev:
    
    ~~~~
    $ .bin/db_util sync
    $ .bin/ansible_util htc-dev
    ~~~~

    The ansible_util should take ~30-40 minutes to complete.

4. Add the otter testing cloud using the csv2 website

Open a web browser, and go to https://htc-dev.heprc.uvic.ca. You will be asked to enter a username and password - use the csv2_default username and password. 

To add the otter testing cloud, press the "Clouds" tab at the top left of the page, then press the "+" button that appears at the top left. Enter the following information:

* Cloud name: otter-container
* URL: https://otter.heprc.uvic.ca:15000/v3
* Project: testing
* Username: [your_otter_username]
* Password: [your_otter_password]
* CA certificate: /etc/ssl/certs/ca-bundle.crt
* Region: Victoria
* User domain name: Default
* Project domain name: default
* Cloud type: openstack

Press 'Add Cloud', then refresh the page. Two new rows should appear with a grey background named "Cores" and "RAM". Set these to:

Cores: 5 / 20
RAM: 20000 / 51200

Now, press to the "Defaults" tab at the top of the page (between "Clouds" and "Images"), and add the following info:

VM Flavour: s1
VM Image: cernvm3-micro-3.0-6.hdd
VM Network: glint_net

and click "Update Group". The otter cloud should now be ready to launch VMs to run condor jobs.

5. Launch a test job from htc-dev.

    ssh into the running docker container as follows:

    ~~~~
    $ ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 947 root@htc-dev.heprc.uvic.ca
    [password: supersecret]
    ~~~~

    switch to the condor user, make a 'logs' directory, and launch a test job, located in the /jobs directory

    ~~~~
    $ su condor -s /bin/bash
    $ cd
    $ mkdir logs
    $ cd /jobs
    $ condor_submit job.sh
    ~~~~

    Press ctl-D to switch back to the root user. The job should appear on the cloud status webpage (https://htc-dev.heprc.uvic.ca/cloud/status/), and cloudscheduler will launch VMs to run the job. The VM should boot and start running the test job after ~5-10 minutes. 

    The status of the job can be checked using condor_q

    ~~~~
    $ condor_q
    ~~~~

    For more information, use the better-analyze option

    ~~~~
    $ condor_q -better-analyze
    ~~~~

6. The test job try.job in the /jobs directory can be run by switching to condor user, and using the condor_submit command:

    ~~~~
    $ su condor
    $ cd /jobs
    $ condor_submit try.job
    ~~~~

    To switch back to root user, type ctrl-D.

    To check the status of your job in the condor q type:

    ~~~~
    $ condor_q
    ~~~~

    For more information, use the better-analyze option

    ~~~~
    $ condor_q -better-analyze
    ~~~~

    Note that it may take ~5-10 minutes for the VM to boot and the job to start running.

    

