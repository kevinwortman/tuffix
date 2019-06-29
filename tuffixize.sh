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
  echo "error: this is meant for Ubuntu 18.04 and later. Your release information is:"
  lsb_release -a
  exit 1
fi


VMUSER=${USER}

if [ "${VMUSER}x" == "x" ]; then
  echo "Environment missing USER variable; using student."
  VMUSER=student
fi

# Set desktop background to Tuffix wallpaper.
TUFFIX_WALLPAPER_BUCKET="https://storage.googleapis.com/csufcs/"
TUFFIX_WALLPAPER_FILENAME="Tuffix_Background_V2_1920x1080_JeffreyLo.png"
XUBUNTU_BACKDROPS_DIRECTORY="/usr/share/xfce4/backdrops/"
sudo wget ${TUFFIX_WALLPAPER_BUCKET}${TUFFIX_WALLPAPER_FILENAME} \
     -P ${XUBUNTU_BACKDROPS_DIRECTORY}
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path \
             -s ${XUBUNTU_BACKDROPS_DIRECTORY}${TUFFIX_WALLPAPER_FILENAME}
xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image \
             -s ${XUBUNTU_BACKDROPS_DIRECTORY}${TUFFIX_WALLPAPER_FILENAME}

# This was for installing the latest version of Ansible.
#sudo apt-get --yes update
#sudo apt-get install --yes software-properties-common
#sudo apt-add-repository --yes ppa:ansible/ansible
#sudo apt-get --yes update
#sudo apt-get install --yes ansible
#sudo apt-get install --yes wget

sudo apt --yes install ansible wget

wget -O ${TUFFIXYML} ${TUFFIXYML_SRC}

sudo ansible-playbook --extra-vars="login=${VMUSER}" --inventory localhost, --connection local ${TUFFIXYML}

rm -f ${TUFFIXYML}
