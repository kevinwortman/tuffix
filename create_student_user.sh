#! /bin/sh

sudo adduser --disabled-password --gecos "" student
sudo passwd student <<EOF
student
student
EOF
usermod -aG sudo student
