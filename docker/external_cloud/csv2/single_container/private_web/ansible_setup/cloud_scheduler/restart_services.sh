#!/bin/sh

# Make sure mysql service is down
pkill -9 mysql

# Start all services
systemctl restart ntpd
systemctl restart mariadb
systemctl restart httpd
systemctl restart csv2-*
systemctl restart condor
