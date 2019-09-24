#! /bin/bash


# Use  the default environment defined TUFFIXYML_SRC
# (see bash (1) Parameter Expansion)
TUFFIXYML_SRC=${TUFFIXYML_SRC:-"https://raw.githubusercontent.com/kevinwortman/tuffix/master/tuffix.yml"}

TUFFIXYML=/tmp/tuffix.$$.yml

if (( EUID == 0 )); then
    echo "error: do not run tuffixize.sh as root"
    exit 1
fi

MAJOR_RELEASE=`lsb_release -r | cut -f 2 | cut -f 1 -d.`
MINOR_RELEASE=`lsb_release -r | cut -f 2 | cut -f 2 -d.`
if [ ${MAJOR_RELEASE} -lt 19 ]; then
  echo "error: this is meant for Ubuntu 19.04 and later. Your release information is:"
  lsb_release -a
  exit 1
fi


VMUSER=${USER}

if [ "${VMUSER}x" == "x" ]; then
  echo "Environment missing USER variable; using student."
  VMUSER=student
fi

sudo apt --yes install ansible wget

REGEX='(https?)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'

if [[ $TUFFIXYML_SRC =~ $REGEX ]]; then
  wget -O ${TUFFIXYML} ${TUFFIXYML_SRC}
else
  cp ${TUFFIXYML_SRC} ${TUFFIXYML}
fi

sudo ansible-playbook --extra-vars="login=${VMUSER}" --inventory localhost, --connection local ${TUFFIXYML}

rm -f ${TUFFIXYML}
