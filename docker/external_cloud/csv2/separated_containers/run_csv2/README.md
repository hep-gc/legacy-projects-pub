# Run Jobs on an External Cloud from a Single Container with private web using csv2 container README

## Introduction

This README describes how to use the code in this directory - along with the csv2 container produced using the code in ../ansible_setup as described in the README in the separated_containers directory (one directory up from here) - to pull and run a container running csv2 on your host machine, and run a condor container on either the same or another machine that submits jobs to the csv2 container.

## Pre-requesites

NOTE: The csv2 container will not currently be able to run condor jobs on a mac because [docker for mac currently cannot route external traffic to docker containers](https://docs.docker.com/docker-for-mac/networking/#httphttps-proxy-support).

To successfully pull and run the csv2 container on your host machine, the following pre-requisites are needed:

* Root or sudo access on the host machine
* A running [docker](https://runnable.com/docker/install-docker-on-linux) installation and a [docker-compose](https://docs.docker.com/v17.09/compose/install/) installation
* At least 6GB of RAM allocated to docker containers. On a mac, for example, this can be set in the advanced docker preferences. For linux machines, docker appears to allocate the full system memory by default, so as long as the host VM has well over 6GB of RAM, it should be ok. 
* The following ports must be open to external IPv4 traffic and not in use:
  * 3306
  * 80
  * 443, 444
  
  These ports are open by default on a mac (because mac doesn't run a firewall by default). The ports can be opened on a centos 7 machine, for example, using the following command:
  ~~~~
  $ firewall-cmd --permanent --add-port=9168/tcp
  $ firewall-cmd --reload
  ~~~~
  and repeating for the other ports and port ranges.
  
* Access to a web browser to view the csv2 webpage
  
To successfully run the condor container, the machine on which it will run should have the following ports open to external IPv4 traffic:

  * 9168 
  * 40000-40500

## Pulling and running the csv2 container

1. Pull the csv2 docker image from github:

   If you created your own image following the instructions in the private_web README (one directory up from here), pull the image from the docker hub account:

  ~~~~
  $ docker pull danikam/csv2_separate_condor
  ~~~~
  
  This pull should take ~5-15 minutes depending on your internet speed.
  
  If you saved the container to your own repo, or want to pull with a specific tag (eg. danikam/csv2_private_web:190109), pull that image instead. 
  
2. Start up the csv2 container using docker-compose. Note: the docker-compose command must be run from the cloud_scheduler directory (i.e. the directory containing the docker-compose.yml file for csv2).

If you pulled the container image from another repo, or used a specific tag, you'll need to update the first line of the Dockerfile to use the correct image name and tag. The csv2 container can then be started using:

  ~~~~
  $ cd cloud_scheduler
  $ docker-compose up&
  ~~~~
  
  It should take ~2-5 minutes for the container to get up and running.
  
3. Access the csv2 web interface with your web browser.

Once the container is up and running, you should be able to see the csv2 web interface by typing https://localhost into your local web browser. 

Alternatively (if the container is running on a remote machine), you can access the browser from a local machine using port forwarding as follows: open a port on the machine running the container (e.g. 1234), then create an ssh tunnel as follows:

~~~~
$ ssh -L 1234:localhost:443 root@[IP or FQDN of machine running container]
~~~~

Then open the browser on your local machine and type in https://localhost:1234.

The webpage (at least on firefox, and likely others) will come up with a security warning due to the self-signed ssl certificate, and ask if you want to add an exception - add the security exception to continue to the csv2 webpage. You will then be asked to input a username and password. These are:

Username: csv2_default
Password: csv2_pass

  The container is currently set up to run jobs on the otter testing cloud, but you can add or remove other clouds by pressing the "Clouds" tab at the top left of the csv2 web page, then pressing the "+" button that appears at the top left of the Clouds page.
  
4. Start up the condor container using docker-compose. 

   First, ssh onto the machine on which you want to run condor (unless using the same machine as for csv2). If needed, clone this repo:
   
   git clone https://github.com/hep-gc/docker
   
   Next, cd into the condor directory and run docker-compose up. Eg.
   
   ~~~~
   $ cd docker/external_cloud/csv2/separated_containers/run_csv2/condor
   $ docker-compose up&
   ~~~~

5. If needed update the Condor Central Manager for csv2-group on the csv2 webpage by navigating to the Groups page (using 'Groups' tab in upper right-hand corner). This should be the domain name of the machine running condor. 

   Right now, it's also necessary to update the defaults.yaml.j2 file by navigating to hte Defaults page using the 'Defaults' tab (upper left on the webpage), clicking on the 'Metadata' tab under csv2-group, then clicking on default.yaml.j2 and setting the CONDOR_HOST on line 24 to either the domain name or public IP address of the machine running condor. Note that this step should no longer be necessary once csv2 is updated to allow custom schedd names.

4. Start a bash shell in the running condor container and submit a sample job to condor.

  First, determine the name of the running condor container on the machine running condor by typing:
  
  ~~~~
  $ docker ps
  ~~~~
  
  Use the following command to start an interactive bash shell in the condor container:
  
  ~~~~
  $ docker exec -it [name of running condor container] /bin/bash
  ~~~~
  
  Once in the container, switch to the condor user to submit the sample job job.sh in the /jobs directory:
  
  ~~~~
  $ su condor
  $ cd /jobs
  $ condor_submit job.sh
  ~~~~
  
   Press ctrl-D to switch back to the root user. The job should appear on the cloud status webpage (https://htc-dev.heprc.uvic.ca/cloud/status/), and cloudscheduler will launch VMs to run the job. The VM should boot and start running the test job after ~5-10 minutes. 

  The status of the job can be checked using condor_q

  ~~~~
  $ condor_q
  ~~~~

  For more information, use the better-analyze option
  ~~~~
  $ condor_q -better-analyze
  ~~~~

  Note that it may take ~5-10 minutes for the VM to boot on otter and the job to start running.
