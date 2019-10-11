# Aidrop API

## Prerequisites

* To make this server works you need to install first:
        * Python3 (https://www.python.org/download/releases/3.0/)

## Installation

* sudo docker-compose up --build


## Deployment

### First step

* The funcion ```generate_hashes()``` in src/views.py is responsible for the number generation, adapt it to conform your country

### In host
* sudo bash deploy.sh
* scp ./"DIRECTORY".zip user@dir:/usr/src

### In server
* ssh user@dir
* cd /usr/src
* sudo bash deploy_host.sh

## Authors
Work of the team 'Ideas Locas' (Area CDO of Telefonica):

* Pablo González Pérez (@pablogonzalezpe)
* Lucas Fernández Aragón (@lucferbux)