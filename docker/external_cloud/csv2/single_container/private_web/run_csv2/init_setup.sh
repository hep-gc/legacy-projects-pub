#!/bin/bash

# Add localhost to the /etc/hosts file
LINE='172.28.5.1      localhost'; FILE=/etc/hosts; grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"

# Replace NETWORK_INTERFACE line in condor_config.local with the current host's IP address
public_ip=$(curl -s http://whatismyip.akamai.com/)
sed -i '/^NETWORK_INTERFACE =/ d' /etc/condor/condor_config.local
LINE="NETWORK_INTERFACE = $public_ip"; FILE=/etc/condor/condor_config.local; grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"

# Replace line in defaults.yaml.j2 where the public IP needs to be specified
#grep -q "^        CONDOR_HOST=" /opt/cloudscheduler/default.yaml.j2 && sed "s/^        CONDOR_HOST=.*/        CONDOR_HOST=$public_ip/" -i /opt/cloudscheduler/default.yaml.j2 || sed "$ a\        CONDOR_HOST=$public_ip" -i /opt/cloudscheduler/default.yaml.j2
