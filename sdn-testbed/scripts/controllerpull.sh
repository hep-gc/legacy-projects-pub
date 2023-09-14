#!/bin/sh

#
# cron script that will automatically pull in the correct
# to use it put the following in the crontab:
#
# */15 * * * * (cd /var/home/username; sh controllerpull.sh)
#
# where username is the name of an administrative user. The 
# above will run every 15 minutes

{
	echo "file copy http://sdnfiles.hepnetcanada.ca/sdn-testbed/conf/default-controller-replace ."
	echo "configure"
	echo "load replace default-controller-replace"
	echo "commit check"
	echo "commit"
} | /usr/sbin/cli
