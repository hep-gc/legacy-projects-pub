#!/bin/sh

#
# cron script that will automatically pull in the correct
# to use it put the following in the crontab:
#
# */15 * * * * (cd /var/home/username; sh controllerpull.sh)
#
# where username is the name of an administrative user. The 
# above will run every 15 minutes

curl http://sdnfiles.hepnetcanada.ca/sdn-testbed/conf/default-controller-replace -o default-controller-new > /dev/null 2>&1
if ! diff default-controller-replace default-controller-new > /dev/null ; then
	cp default-controller-new default-controller-replace
{
	echo "configure"
	echo "load replace default-controller-replace"
	echo "commit check"
	echo 'commit comment "automated replacement of the OF controller address"'
} | /usr/sbin/cli
fi
