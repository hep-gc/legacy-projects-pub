virt-install \
        --debug \
        --connect qemu:///system \
        --accelerate \
        --name perfsonar-dashboard-sl6 \
        --arch x86_64 \
        --ram 2048 \
        --disk path=/opt/qemu/perfsonar-dashboard-sl6.img,size=20,sparse=true \
        --network bridge:br0 \
	--location='http://mirror.cpsc.ucalgary.ca/mirror/scientificlinux.org/6.3/x86_64/os/' \
        --os-type=linux \
        --os-variant=virtio26 \
	--nographics \
	--extra-args="console=ttyS0"
        #--vnc \
        #--location='/tmp/ubuntu/ubuntu-11.10-alternate-amd64.iso' \
	#--location='http://ftp.ubuntu.com/ubuntu/dists/oneiric/main/installer-amd64/' \
