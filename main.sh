#!/bin/bash

ssh_public_key='/home/templeton/Cluster_Cloud_Computing/assignmnet2'
#Creating Instances, attaching volumes
#echo "Calling boto script"
#python boto_main.py
#echo "Init done!"

#Installing, configuring packages
#Checking if ansible exists or not
command -v ansible-playbook >/dev/null && continue || { echo "ansible-playbook command not found."; exit 1;}

ansible-playbook *.yml



