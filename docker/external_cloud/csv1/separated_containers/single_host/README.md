# External Cloud with Separated Containers on Single Host README

## Introduction

The files in this directory enable a user with access to a machine with a public IP address to run HTCondor and Cloudscheduler in two separate docker containers created on the same host machine using docker compose. One of the docker containers will be running [HTCondor](https://research.cs.wisc.edu/htcondor/description.html) to manage job submissions, and the other will run cloudscheduler to launch virtual machines VMs on external clouds.


## Prerequisites

To successfully launch VMs on external clusters from your machine, the following pre-requisites are needed:

* Root access on your machine (or sudo access, in which case all docker commands should be preceded by sudo)
* A running [docker installation](https://runnable.com/docker/install-docker-on-linux)
* A [docker compose](https://docs.docker.com/v17.09/compose/install/) installation

* The machine must have a public IP address in order to communicate with external clusters. You can determine your public IP address (if it exists) with the following command:

  ~~~~
  $ curl ipinfo.io/ip
  ~~~~

* The following ports should be open to external IPv4 traffic:

    * 9618/tcp and 9618/udp
    * 40000-50000/tcp

## Instructions

1. Edit the CENTRAL_MANAGER variable on line 140 of the cloud_scheduler/default.yaml file so it reads: 

    CENTRAL_MANAGER=[your public IP address]

    where your public IP address can be obtained from typing
    ~~~~
    $ curl ipinfo.io/ip
    ~~~~

    Also, edit the NETWORK_INTERFACE variable on line 23 of cloud_scheduler/condor_config.local so it reads:

    NETWORK_INTERFACE = [your public IP address]

2. Start the condor and cloudscheduler services using the docker-compose up command from the current (external_cloud/separated_containers/single_host) directory. Optionally, you can name the project to something other than the default single_host (the name of the current working directory). The example below sets the project name to "cs" using the -p option in docker-compose:

    ~~~~
    $ docker-compose -p cs up &
    ~~~~

    Once docker-compose has finished building and running the containers, the output should read:

      ~~~~
      Attaching to cs_cloud_scheduler_1, cs_condor_1
      cloud_scheduler_1  | Starting cloud_scheduler:				[  OK  ]
      cloud_scheduler_1  | Cloud: cc-west-a disabled.
      cloud_scheduler_1  | Cloud: otter-container enabled.
      ~~~~

    You can then hit enter to recover the bash command prompt.

    If you type

    ~~~~
    $ docker ps
    ~~~~

    The output should show two running docker containers, one named "cs_condor_1", and the other named "cs_cloud_scheduler_1". You can now submit jobs from the condor container, which the cloudscheduler container will run by launching VMs on external clouds.

4. Start a bash shell in the running cloudscheduler container:

    ~~~~
    $ docker exec -it cs_cloud_scheduler_1 /bin/bash
    ~~~~

5. The container should already be running cloudscheduler, with the otter-container cloud enabled. The computecanada west cloud is also configured in the /etc/cloudscheduler/cloud_resources.conf file. More clouds can be added to the cloud_resources.conf file as needed. 

    To see the list of available clouds, type:

    ~~~~
    $ cloud_status 
    ~~~~


      Clouds can enabled or disabled using the cloud_admin command.

      To enable:

      ~~~~
      $ cloud_admin -e [cloud name]
      ~~~~

      To disable:

      ~~~~
      $ cloud_admin -d [cloud name]
      ~~~~

      For example, the otter-container cloud can be disabled using:

      ~~~~
      $ cloud_admin -d otter-container
      ~~~~
  
    If any of the files in /etc/cloudscheduler are updated, cloudscheduler needs to be restarted for the changes to take effect:

    ~~~~
    $ /etc/init.d/cloudscheduler quickrestart
    ~~~~

    After restarting cloudscheduler, clouds may need to be disabled or re-enabled using cloud_admin to get to the original settings. For example, to get back to the default setting of having only otter-container enabled:

    ~~~~
    $ cloud_admin -d cc-west-a
    $ cloud_admin -e otter-container
    ~~~~


6. The test job try.job in the /jobs directory can be run from the condor container. 

    Either start in a new shell on the host VM, or detach from the cloud_scheduler container by typing ctrl-D. Next, start a bash shell in the container running condor:

    ~~~~
    $ docker exec -it cs_condor_1 /bin/bash
    ~~~~

    Now in the container, switch to the condor user, and submit the test job:

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

    Note that it may take ~5-10 minutes for the VM to boot from the container running cloudscheduler, and the job to start running.

    

