#! /bin/bash

# Use  the default environment defined TUFFIXYML_SRC
# (see bash (1) Parameter Expansion)
TUFFIXYML_SRC=${TUFFIXYML_SRC:-"https://raw.githubusercontent.com/kevinwortman/tuffix/master/tuffix.yml"}

TUFFIXYML=/tmp/tuffix.$$.yml

test_dns_web ( ){
  TARGET="http://www.fullerton.edu"
  RV=`wget -q --timeout=2 --dns-timeout=2 --connect-timeout=2 --read-timeout=2 -S -O /dev/null ${TARGET} 2>&1 | grep "^\( *\)HTTP" | tail -1 | awk '{print $2}'`
  if [ "${RV}x" != "200x" ]; then
    echo "The network is down or slow; check to make sure are connected to your network. If connecting to Eduroam, seek assistance."
      exit 1
  fi
}

overide_apt_sources ( ){
  HOSTURL=${1}
  CODENAME=${2}
  NOW=`date +%Y%m%d%H%M%S`
  OG="/etc/apt/sources.list"
  BAK="${OG}.${NOW}"
  cp ${OG} ${BAK}
  cat > ${OG} << EOF
deb ${HOSTURL} ${CODENAME} main restricted
deb ${HOSTURL} ${CODENAME}-updates main restricted
deb ${HOSTURL} ${CODENAME} universe
deb ${HOSTURL} ${CODENAME}-updates universe
deb ${HOSTURL} ${CODENAME} multiverse
deb ${HOSTURL} ${CODENAME}-updates multiverse
deb ${HOSTURL} ${CODENAME}-backports main restricted universe multiverse
deb ${HOSTURL} ${CODENAME}-security main restricted
deb ${HOSTURL} ${CODENAME}-security universe
deb ${HOSTURL} ${CODENAME}-security multiverse
EOF
  echo ${BAK}
}

MAJOR_RELEASE=`lsb_release -r | cut -f 2 | cut -f 1 -d.`
MINOR_RELEASE=`lsb_release -r | cut -f 2 | cut -f 2 -d.`
if [ ${MAJOR_RELEASE} -lt 19 ]; then
  echo "Warning: this is meant for Ubuntu 19.04 and later. Your release information is:"
  lsb_release -a
fi


VMUSER=${USER}

if [ "${VMUSER}x" == "x" ]; then
  echo "Environment missing USER variable; using student."
  VMUSER=student
elif [ ${EUID} -eq 0 ]; then
  echo "Warning: you are running this script as root. This is not advisable."
  echo "Push ctrl-c to exit. You have 5 seconds."
  sleep 5
fi

test_dns_web

REGEX='(https?)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'

# If TUFFIX_APT_SOURCES_HOST is defined, rewrite /etc/apt/sources.list
if [ ${TUFFIX_APT_SOURCES_HOSTURL}"x" != "x" ]; then
  echo "Overriding /etc/apt/sources.list with ${TUFFIX_APT_SOURCES_HOSTURL}"
  if [[ $TUFFIX_APT_SOURCES_HOSTURL =~ $REGEX ]]; then
    CODENAME=`lsb_release -c | cut -f 2`
    ORIGINAL_APT_SOURCES=`overide_apt_sources  ${TUFFIX_APT_SOURCES_HOSTURL} ${CODENAME}`
  else
    echo "$TUFFIX_APT_SOURCES_HOSTURL is not a valid URL"
  fi
fi

sudo apt update
sudo apt --yes install ansible wget aptitude python python3-distutils

if [[ $TUFFIXYML_SRC =~ $REGEX ]]; then
  wget -O ${TUFFIXYML} ${TUFFIXYML_SRC}
else
  # Useful for debugging
  echo "Overriding TUFFIXYML_SRC: ${TUFFIXYML_SRC}"
  cp ${TUFFIXYML_SRC} ${TUFFIXYML}
fi

sudo ansible-playbook --extra-vars="login=${VMUSER}" --inventory localhost, --connection local ${TUFFIXYML}

if [ ${TUFFIX_APT_SOURCES_HOST_PERMANENT}"x" != "YESx" -a ${TUFFIX_APT_SOURCES_HOSTURL}"x" != "x" ]; then
  echo "Returning /etc/apt/sources.list to original state"
  mv ${ORIGINAL_APT_SOURCES} /etc/apt/sources.list
fi

rm -f ${TUFFIXYML}

