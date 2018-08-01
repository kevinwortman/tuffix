#! /bin/bash

TUFFIXYML_SRC="https://raw.githubusercontent.com/mshafae/tuffix/package-changes-mshafae/tuffix.yml"

TUFFIXYML=/tmp/tuffix.$$.yml

if (( EUID == 0 )); then
    echo "error: do not run tuffixize.sh as root"
    exit 1
fi

if [ $# > 0 ]; then
  VMUSER=student
else
  VMUSER=${USER}
fi

VMUSER=${USER}

if [ "${VMUSER}x" == "x" ]; then
  echo "Environment missing USER variable; using student."
  VMUSER=student
fi


sudo apt --yes install ansible wget

ANSIBLE_MAJOR_RELEASE=`ansible --version | head -1 | cut -f 2 -d\  | cut -f 1 -d.`
ANSIBLE_MINOR_RELEASE=`ansible --version | head -1 | cut -f 2 -d\  | cut -f 2 -d.`

# The tuffix YAML file requires Ansible version 2.1 or later.
if [ ${ANSIBLE_MAJOR_VERSION} -le 2 -a ${ANSIBLE_MINOR_RELEASE} -lt 1 ]; then
  # Old version of Ansible; install
  sudo apt-get --yes update
  sudo apt-get install --yes software-properties-common
  sudo apt-add-repository --yes ppa:ansible/ansible
  sudo apt-get --yes update
  sudo apt-get install --yes ansible
fi

wget -O ${TUFFIXYML} ${TUFFIXYML_SRC}

sudo ansible-playbook --extra-vars=\"login=${VMUSER}\" --inventory localhost, --connection local ${TUFFIXYML}

#rm -f ${TUFFIXYML}
