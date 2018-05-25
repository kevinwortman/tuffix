#! /bin/bash

if (( EUID == 0 )); then
    echo "error: do not run tuffixize.sh as root"
    exit 1
fi

sudo apt --yes install ansible wget

wget https://raw.githubusercontent.com/kevinwortman/tuffix/master/tuffix.yml

sudo ansible-playbook --inventory localhost, --connection local

rm -f tuffix.yml

sudo chown -R $USER:$USER ~/.atom
