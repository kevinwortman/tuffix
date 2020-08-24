#!/usr/bin/env bash

# Run the script with safe mode.
set -e

exists() { command -v "$@" > /dev/null; }
stderr() { echo "$@" 1>&2; }
fatal()  { stderr "$@"; exit 1; }

test_url() {
	# wget the given URL. Method HEAD prevents the server from sending any
	# request body.
	HEADERS="$(wget -qS --timeout=2 --method HEAD "$1" 2>&1)"

	# Check if the response contains a 200 OK code.
	[[ "$HEADERS" =~ 200\ OK ]]
	return $?
}

override_apt_sources() {
	HOSTURL="$1"
	CODENAME="$2"

	printf -v NOW "%(%Y%m%d%H%M%S)T"

	OG="/etc/apt/sources.list"
	BAK="$OG.$NOW"

	cp "$OG" "$BAK"

	cat > "$OG" << EOF
deb $HOSTURL $CODENAME main restricted
deb $HOSTURL $CODENAME-updates main restricted
deb $HOSTURL $CODENAME universe
deb $HOSTURL $CODENAME-updates universe
deb $HOSTURL $CODENAME multiverse
deb $HOSTURL $CODENAME-updates multiverse
deb $HOSTURL $CODENAME-backports main restricted universe multiverse
deb $HOSTURL $CODENAME-security main restricted
deb $HOSTURL $CODENAME-security universe
deb $HOSTURL $CODENAME-security multiverse
EOF

	echo -n "$BAK"
}

# Check that apt is present.
if ! exists apt; then
	fatal "apt not found. Make sure you're on Ubuntu or a Debian-based distro."
fi


# Prefer the default environment defined $TUFFIXYML_SRC.
# (see bash (1) Parameter Expansion)
TUFFIXYML_SRC=${TUFFIXYML_SRC:-"https://raw.githubusercontent.com/kevinwortman/tuffix/master/tuffix.yml"}
TUFFIXYML=/tmp/tuffix.$$.yml

if [[ "$(lsb_release -r)" =~ ([[:digit:]]+).([[:digit:]]+) ]]; then
	MAJOR_RELEASE="${BASH_REMATCH[1]}"
	# Unused.
	# MINOR_RELEASE="${BASH_REMATCH[2]}"

	if (( MAJOR_RELEASE < 19 )); then
		stderr "Warning: this is meant for Ubuntu 19.04 and later."
		stderr "Your release information is: $(lsb_release -a)."
	fi
else
	stderr "Warning: this is meant for Ubuntu 19.04 and later."
	stderr "Failed to parse lsb_release."
fi

VMUSER="$USER"

if [[ ! "$VMUSER" ]]; then
	stderr 'Environment missing USER variable; using "student".'
	VMUSER="student"

elif (( EUID == 0 )); then
	stderr "Warning: you are running this script as root. This is not advisable."
	stderr "Push ctrl-c to exit. You have 5 seconds before continuing."
	sleep 5
fi

# Test the connection to ensure that everything is running.
if ! test_url "http://www.fullerton.edu"; then
	fatal "The network is down or slow; check to make sure are connected to your network. If connecting to Eduroam, seek assistance."
fi

# Regex constant to check for a valid URL.
URL_REGEX='(https?)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'

# If TUFFIX_APT_SOURCES_HOST is defined, rewrite /etc/apt/sources.list
if [[ "$TUFFIX_APT_SOURCES_HOSTURL" ]]; then
	stderr "Overriding /etc/apt/sources.list with $TUFFIX_APT_SOURCES_HOSTURL."

	if [[ "$TUFFIX_APT_SOURCES_HOSTURL" =~ $URL_REGEX ]]; then
		read -r _ CODENAME < <(lsb_release -c)
		ORIGINAL_APT_SOURCES="$(overide_apt_sources "$TUFFIX_APT_SOURCES_HOSTURL" "$CODENAME")"
	else
		stderr "Warning: $TUFFIX_APT_SOURCES_HOSTURL is not a valid URL"
	fi
fi

sudo apt update
sudo apt --yes install ansible wget aptitude python python3-distutils

if [[ "$TUFFIXYML_SRC" =~ $URL_REGEX ]]; then
	wget -qO "$TUFFIXYML" "$TUFFIXYML_SRC"
else
	# Useful for debugging
	stderr "Overriding TUFFIXYML_SRC: $TUFFIXYML_SRC."
	cp "$TUFFIXYML_SRC" "$TUFFIXYML"
fi

sudo ansible-playbook --extra-vars "login=$VMUSER" --inventory localhost, --connection local "$TUFFIXYML"

# If we're not applying apt sources permanently and we have succesfully parsed
# apt host URLs before, then we should restore them.
if [[ "$TUFFIX_APT_SOURCES_HOST_PERMANENT" != "YES" && "$TUFFIX_APT_SOURCES_HOSTURL" ]]; then
	stderr "Returning /etc/apt/sources.list to original state."
	mv "$ORIGINAL_APT_SOURCES" /etc/apt/sources.list
fi

rm -f "$TUFFIXYML"
