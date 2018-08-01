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

wget -O ${TUFFIXYML} ${TUFFIXYML_SRC}

sudo ansible-playbook --extra-vars=\"login=${VMUSER}\" --inventory localhost, --connection local ${TUFFIXYML}

rm -f ${TUFFIXYML}
