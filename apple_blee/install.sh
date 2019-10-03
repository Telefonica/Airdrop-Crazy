#!/bin/bash

echo "Configuring Apple Ble dependencies...."

#Install Linux dependencies
apt-get update
apt-get install -y --no-install-recommends bluez libpcap-dev libev-dev libnl-3-dev libnl-genl-3-dev libnl-route-3-dev cmake libbluetooth-dev git wireless-tools net-tools
apt-get install -y --no-install-recommends && apt-get install -y python3-pip python3-dev  && cd /usr/local/bin && ln -s /usr/bin/python3 python && pip3 install --upgrade pip

git clone https://github.com/seemoo-lab/owl.git
cd ./owl

if [ ${PWD##*/} == "owl" ] 
then
    echo "Installing owl..."
    git submodule update --init
    mkdir build
    cd build
    cmake ..
    make
    sudo make install
    cd ../..
    rm -r owl
fi

read  -p "Do you want to create a virtual environment? (y/n): " follow

if [ "$follow" == "y" ]
then
    sudo pip3 install virtualenv
    sudo virtualenv appleBle
    source appleBle/bin/activate
fi
echo "Installing python libraries..."
# Install Python dependencies
sudo pip3 install --no-cache-dir -r ./requirements.txt  -q &> /dev/null
echo "Done!"

if [ "$follow" == "y" ]
then
    echo "To activate virtualenv use: source appleBle/bin/activate"
    echo "To exit: deactivate"
fi