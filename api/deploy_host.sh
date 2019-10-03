#!bin/bash
WORKING_DIR="AirdropDeploy"
if [ -d "$WORKING_DIR" ]; then rm -Rf $WORKING_DIR; fi
unzip $WORKING_DIR.zip
echo "Killing..."
if [ $(sudo docker ps -q) ]; then sudo docker kill $(sudo docker ps -q); fi
echo "Starting docker..."
cd $WORKING_DIR
sudo docker-compose up --build