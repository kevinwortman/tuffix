#! /bin/bash

URL="https://raw.githubusercontent.com/kevinwortman/tuffix/master/tuffix.yml"

ANSIBLE="ansible-playbook --inventory localhost, --connection local"

if (( EUID == 0 )); then
    echo "error: do not run tuffixize.sh as root"
    exit 1
fi

sudo apt --yes install ansible wget

wget $URL | sudo $ANSIBLE

sudo chown -R $USER:$USER ~/.atom
