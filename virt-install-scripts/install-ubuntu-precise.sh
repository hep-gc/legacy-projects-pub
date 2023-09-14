virt-install \
        --debug \
        --connect qemu:///system \
        --accelerate \
        --name mchester-ubuntu-1204 \
        --arch x86_64 \
        --ram 1024 \
        --disk path=/opt/qemu/mchester-ubuntu-1204.img,size=20,sparse=true \
        --network bridge:br0 \
	--location='http://mirror.cpsc.ucalgary.ca/mirror/ubuntu.com/packages/dists/precise/main/installer-amd64/' \
        --os-type=linux \
        --os-variant=virtio26 \
	--nographics \
	--extra-args="console=ttyS0"
        #--vnc \
        #--location='/tmp/ubuntu/ubuntu-11.10-alternate-amd64.iso' \
	#--location='http://ftp.ubuntu.com/ubuntu/dists/oneiric/main/installer-amd64/' \
