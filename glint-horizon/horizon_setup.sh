#!/bin/bash

#set the url to the glint service location
GLINT_URL="localhost"

#list of package requirements needed by horizon-glint
declare -a rh_libs=("libxml2-devel" "libxslt-devel" "openssl-devel")


#check and yum or apt install libxml2-devel and libxslt-devel and python paste is installed
IS_RH=`ls /etc | grep redhat`
IS_DEB=`ls /etc | grep debian`

if [ "$IS_DEB" != "" ]; then
	echo "this is debian $IS_DEB use dpkg to check for installed package requirements"
	
elif [ IS_RH != "" ]; then
	echo "this is redhat $IS_RH use rpm to check for installed package requirements"
	
else
	echo "unable to check for system package requirements ... lets hope they are there already and carry on with this!"
fi

#set SETUP_METHOD to either "V_ENV" or "GLOBAL"
#V_VENV will create a virtual environment and install requirement in the .venv directory which can easily be
#manually deleted from the system. GLOBAL will install in the python site-packages directory
SETUP_METHOD="V_ENV"

#runsetup or create venv for horizon according to config file
if [ "$SETUP_METHOD" = "V_ENV" ]; then
    echo "Setup for Python Virtual Environment"
	echo "using: python tools/install_venv.py"
	python tools/install_venv.py
else
	echo "Setup for Global install"
	echo "python setup.py install"
fi



