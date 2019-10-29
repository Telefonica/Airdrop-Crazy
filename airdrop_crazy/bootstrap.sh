#!/bin/bash
if [ ! -d "airNope" ]; then
  read  -p "Virtual Environment not created, do you want to create it (y/n)?: " follow
    if [ "$follow" == "y" ]
    then
        pip3 install virtualenv
        virtualenv -p python3 airNope
        source airNope/bin/activate
        echo "Installing python libraries..."
        pip3 install --no-cache-dir -r ./requirements.txt
    fi
else
  source airNope/bin/activate
fi


python3 app.py