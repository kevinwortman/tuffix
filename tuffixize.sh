#! /bin/bash

TUFFIX_YML_URL=https://raw.githubusercontent.com/kevinwortman/tuffix/master/tuffix.yml

ANSIBLE_COMMAND=ansible-playbook --inventory localhost, --connection local

if (( EUID == 0 )); then
    echo "error: do not run tuffixize.sh as root"
    exit 1
fi

apt --yes install ansible wget

wget $(TUFFIX_YML_URL) | sudo $(ANSIBLE_COMMAND)

sudo chown -R $USER:$USER ~/.atom
