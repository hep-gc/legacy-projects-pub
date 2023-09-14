Cloud Scheduler Munin Plugins
=============================

A few Munin plugins that are useful for monitoring condor and cloud scheduler. They assume you have condor_q, condor_status, and cloud_status in your path.

Install
=======

    curl -L https://github.com/hep-gc/Cloud-Scheduler-Munin-Plugins/tarball/master | tar xz
    cd hep-gc-Cloud-Scheduler-Munin-Plugins-*
    cp plugins/* /etc/munin/plugins/
    /etc/init.d/munin-node reload
