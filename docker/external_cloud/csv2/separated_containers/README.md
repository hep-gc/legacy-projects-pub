# csv2 to Run Jobs on an External Cloud from Separate csv2 and Condor containers with Private Web README

## Introduction

The files in this directory currently enable a user with access to both the elephant06.heprc.uvic.ca and htc-dev.heprc.uvic.ca computers to create two docker CENTOS 7 containers, one of which runs [HTCondor](https://research.cs.wisc.edu/htcondor/description.html), and the other runs cloudscheduler version 2 to launch virtual machines (VMs) and run the HTCondor jobs on external clusters. Once the csv2 image is created and pushed to the docker hub, the user can pull the image and have a running csv2 container, which communicates with a container running condor on either the same or another machine. 

## Prerequisites

To successfully create and set up the csv2 and condor containers from scratch, the following pre-requisites are needed:

* Root access to the elephant06.heprc.uvic.ca and htc-dev.heprc.uvic.ca VMs

* The csv2_default password to access the csv2 website at https://htc-dev.heprc.uvic.ca

* The following ports on htc-dev should be open to external IPv4 traffic and not in use:

    * 80/tcp
    * 947/tcp
    * 3306/tcp
    * 443/tcp
    * 9618/tcp
    * 40000-40500/tcp

## Instructions

1. ssh onto the htc-dev computer:

    ~~~~
    $ ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 3121 [your_username]@htc-dev.heprc.uvic.ca
    ~~~~

2. Starting in the ansible_setup (separated_containers/single_host/ansible_setup) directory, use docker-compose to build and run the cloudscheduler and condor containers

    ~~~~
    $ cd ansible_setup
    $ docker-compose up&
    ~~~~
    
3. Run ansible from elephant06 to set up csv2 on the running cloudscheduler container

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

    Make sure the 'container' and 'local_web' variables are both set to True in htc-dev-vars.yaml, and the running_condor variable is set to False:
    
    ~~~~
    container: True
    local_web: True
    running_condor: False
    ~~~~
    
    Run ansible on the docker container running on htc-dev. Eg.
    
    ~~~~
    $ cd /home/danikam1/Git/Inventory/heprc
    $ .bin/db_util sync
    $ .bin/ansible_util htc-dev
    ~~~~

    The ansible_util should take ~30-40 minutes to complete. Once the ansible script has finished running, csv2 should be accessible at https://htc-dev.heprc.uvic.ca (or at https://localhost on the VM itself), and the phpmyadmin webpage should be accessible from a web browser running on the htc-dev VM at https://localhost:444/phpmyadmin. 
    
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

    switch to the condor user and launch a test job, located in the /jobs directory

    ~~~~
    $ su condor
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

    Note that it may take ~5-10 minutes for the VM to boot on otter and the job to start running.
    
7. Save the running csv2 container as a docker image

    The docker image can be saved to your docker hub account by first logging into docker hub at https://hub.docker.com (can create an account if needed), and creating a new repo called, eg. csv2_private_web. 

    Next, stop the running docker container and log into docker on htc-dev:
    
    ~~~~
    $ docker-compose stop
    $ docker login --username=[your docker hub username]
    ~~~~
    
    Lastly, commit the docker container to a new image named [your docker hub username]/csv2_private_web, and push it to the docker repo. You will need the full name of the running docker container (ansible_setup_cloud_scheduler_1). 

    Run the following commands to commit and push the container to the csv2_private_web repo:    

    ~~~~
    $ docker commit ansible_setup_cloud_scheduler_1 [your docker hub username]/csv2_separate_condor:[some unique tag if desired]
    $ docker push [your docker hub username]/csv2_separate_condor:[some unique tag if desired]
    ~~~~
    
    Note that if you don't include a unique tag, the container pushed to docker hub will overwrite any existing container with the same tag. If the tag isn't specified, it defaults to 'latest'.
    
8. Follow the instructions in the run_csv2 directory's README to pull and run the csv2 image on another machine, with condor running on either the same or another machine.
