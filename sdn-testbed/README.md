SDN Testbed Files
=================

The files in this git repo can used to configure your EX4550 to work with the SDN Testbed.


Setting up users
---------------

Users can be granted access using ssh keys. To load the set of keys from the cli do the following.

    file copy http://sdnfiles.hepnetcanada.ca/sdn-testbed/conf/sdn-user-replace .
    edit
    load replace sdn-user-replace
    commit check
    commit
    

Switching controllers
----------------------

You can switch between the available configure controllers by loading any of the 
[controller replace files][1] by doing the following. For example:

    file copy http://sdnfiles.hepnetcanada.ca/sdn-testbed/conf/floodlight-controller-replace .
    edit 
    load floodlight-controller-replace
    commit check
    commit

The above example depends on the OF switch being called SDNTestbed


Automating Controller Config
----------

You can configure the switch to pull the controller config automatically from
the web whenever a change is made to [default-controller-replace][2]. In order to do this 
you establish a conjob on the switch that will and update and commit the configuration when
the config stored in github is changed. 

    start shell
    mkdir sdn-pull
    cd sdn-pull
    curl http://sdnfiles.hepnetcanada.ca/sdn-testbed/scripts/checknewcontroller.sh -o checknewcontroller.sh

now edit the contab entry to run this script every 5 minutes

    crontab -e 
    ### insert the line:
    */5 * * * * (cd /var/home/username/sdn-pull; sh checknewcontroller.sh)

make sure to replace `username`

Pushing a new Controller Config with Git
--------------------

All the switches configured to pull the controller config via the cron job can be pointed to a 
new controller by making a git commit to the [default-controller-replace][2]. You can do this by
cloning the repository making a modification and pushing the results back to github. For example

    git clone git@github.com:hep-gc/sdn-testbed.git
    cd sdn-testbed
    vim default-controller-replace
    git commit -a -m "changing the default controller"
    git push origin master

A repository post commit [webhook][4] will copy the configuration files to [sdnfiles.hepnetcanada.ca][3]. 
Within 5 minutes all the switches pulling the configuration will change to the new controller.


[1]:https://github.com/hep-gc/sdn-testbed/tree/master/conf
[2]:https://github.com/hep-gc/sdn-testbed/blob/master/conf/default-controller-replace
[3]:http://sdnfiles.hepnetcanada.ca/
[4]:http://developer.github.com/webhooks/
    




