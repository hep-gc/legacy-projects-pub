#!/bin/bash
	virt-install \
		--debug \
		--connect qemu:///system \
		--accelerate \
		--name perfsonar-dev \
		--arch i386 \
		--ram 2048 \
		--disk path=/opt/qemu/perfsonar-dev.img,size=10,sparse=true \
		--network bridge:br0 \
		--cdrom='/tmp/perfsonar/pS-Performance_Toolkit-NetInstall-3.2.1.1.iso' \
		--vnc \
		--os-type=linux \
		--os-variant=virtio26 
#		--extra-args="console=ttyS0"


#		--mac DE:AD:BE:EF:53:23 \
#		--nographics \
#		--extra-args="serial console=tty0 console=ttyS0,115200" \

