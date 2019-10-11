#!/bin/bash
NGROK_AUTHTOKEN=""
IFACE=""
while getopts ":a:i:h" opt; do
      case $opt in
        a ) NGROK_AUTHTOKEN="$OPTARG";;
        i ) IFACE="$OPTARG";;
        h )
            echo "Usage:"
            echo "    deploy.sh -h               Display this help message."
            echo "    deploy.sh -a               Authtoken given for the ngrok service, you must register berfore"
            echo "    deploy.sh -i               Interface used in the OWL communication"
            exit 0
            ;;
        \?) echo "Invalid option: -"$OPTARG"" >&2
            exit 1;;
        : ) echo "Option -"$OPTARG" requires an argument." >&2
            exit 1;;
      esac
    done

# Check ngrok
if [ "$NGROK_AUTHTOKEN" == "" ] 
then
    echo "Error, you must pass an ngrok authtoken, you can get one in https://ngrok.com"
    exit 1
fi

# Check iface
if [ "$IFACE" == "" ] 
then
    echo "Error, you must provide a valid interface"
    exit 1
fi

# Check root user
if [ $EUID -ne 0 ]
then
   echo "This script must be run as root" 
   exit 1
fi
echo "Configuring Apple Ble dependencies...."

#Install Linux dependencies
apt-get update
apt-get install -y --no-install-recommends bluez libpcap-dev libev-dev libnl-3-dev libnl-genl-3-dev libnl-route-3-dev cmake libbluetooth-dev git wireless-tools net-tools aircrack-ng curl
apt-get install -y --no-install-recommends && apt-get install -y python3-pip python3-dev  && cd /usr/local/bin && ln -s /usr/bin/python3 python && pip3 install --upgrade pip

# Install OWL
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

# Install ngrok
mkdir ngrok
cd ./ngrok
if [ ${PWD##*/} == "ngrok" ] 
then
    echo "Installing ngrok..."
    wget "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip" && unzip ngrok-stable-linux-amd64.zip && rm ngrok-stable-linux-amd64.zip
    ./ngrok authtoken $NGROK_AUTHTOKEN
    cd ..
fi


# Change iface
cd ./src
sed -i "s/IFACE=\"\"/IFACE=\"$IFACE\"/g" views.py
cd ..


# Create virtual environment
read  -p "Do you want to create a virtual environment? (y/n): " follow

if [ "$follow" == "y" ]
then
    echo="installing virtualenv...."
    pip3 install virtualenv
    virtualenv -p python3 airCrazy
    source airCrazy/bin/activate
fi

# Instal python dependencies
echo "Installing python libraries..."
# Install Python dependencies
sudo pip3 install --no-cache-dir -r ./requirements.txt
echo "Done!"

if [ "$follow" == "y" ]
then
    echo "To activate virtualenv use: source airCrazy/bin/activate"
    echo "To exit: deactivate"
fi
